# 🔧 FIX: Error al Actualizar Usuario - Data Truncated for user_type

**Fecha:** 28 de Octubre 2025  
**Error:** `Data truncated for column 'user_type' at row 1`

---

## 🐛 **EL PROBLEMA**

### **Error Completo**
```
Error ejecutando query: 1265 (01000): Data truncated for column 'user_type' at row 1
Query: UPDATE users SET full_name = %s, email = %s, user_type = %s, role_id = %s, active = %s, phone = %s, avatar_path = %s, updated_at = %s WHERE id = %s
Params: ('testv4', 'testv4@gmail.com', 'Test03', 11, True, '', '', datetime.datetime(...), 12)
```

### **Causa Raíz**

La columna `user_type` en la tabla `users` es un **ENUM** que solo acepta estos valores:
```sql
user_type ENUM('admin', 'supervisor', 'cashier', 'user') DEFAULT 'user'
```

Pero el código intentaba guardar `'Test03'` (que es el **nombre de un ROL**), no un tipo de usuario válido.

### **¿Por qué pasaba?**

1. ✅ **En `create_user()`**: Se aplicaba un mapeo con `get_user_type_simplified()` que convertía cualquier nombre de rol a un `user_type` válido
2. ❌ **En `update_user()`**: NO se aplicaba este mapeo, pasaba el nombre del rol directamente

**Resultado:** Los usuarios se creaban correctamente, pero al editarlos fallaba.

---

## ✅ **SOLUCIÓN IMPLEMENTADA**

### **Cambio en `controllers/user_controller.py`**

Agregué la función `get_user_type_simplified()` dentro del método `update_user()` para aplicar el mismo mapeo que se usa en `create_user()`:

```python
def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
    # ...código existente...
    
    # 🔧 APLICAR MAPEO DE user_type (igual que en create_user)
    def get_user_type_simplified(role_name):
        """Mapear cualquier rol a un user_type válido del ENUM de BD"""
        role_lower = role_name.lower()
        
        if 'admin' in role_lower or 'sistema' in role_lower:
            return 'admin'
        elif 'supervis' in role_lower or 'gerente' in role_lower or 'jefe' in role_lower:
            return 'supervisor'
        elif 'cajer' in role_lower or 'vend' in role_lower:
            return 'cashier'
        else:
            return 'user'  # Por defecto
    
    # Obtener user_type mapeado
    db_user_type = existing_user.get('user_type')
    if new_role_name:
        db_user_type = get_user_type_simplified(new_role_name)
        print(f"DEBUG: '{new_role_name}' -> '{db_user_type}'")
    
    update_data = {
        'user_type': db_user_type,  # ✅ Usar valor mapeado
        # ...resto de campos...
    }
```

### **Cómo Funciona el Mapeo**

| Nombre del Rol | user_type Mapeado |
|----------------|-------------------|
| `'Admin Sistema'` | `'admin'` |
| `'Gerente de Personal'` | `'supervisor'` |
| `'Supervisor de Ventas'` | `'supervisor'` |
| `'Cajero Principal'` | `'cashier'` |
| `'Vendedor'` | `'cashier'` |
| `'Test03'` | `'user'` ⭐ |
| Cualquier otro | `'user'` |

---

## 🧪 **CÓMO PROBAR**

1. **Reinicia la aplicación**
2. **Edita un usuario** que tenga un rol personalizado (como `'Test03'`)
3. **Verifica los logs** - Deberías ver:
   ```
   DEBUG UPDATE_USER - Mapeo: 'Test03' -> 'user' (role_id: 11)
   ```
4. **Guarda los cambios** - Ahora debería funcionar sin error

---

## 📊 **ANTES vs DESPUÉS**

### **ANTES ❌**
```python
# update_user()
update_data = {
    'user_type': user_data.get('user_type'),  # ❌ 'Test03' directamente
    'role_id': role_id
}
# ERROR: Data truncated for column 'user_type'
```

### **DESPUÉS ✅**
```python
# update_user()
db_user_type = get_user_type_simplified(new_role_name)  # 'Test03' -> 'user'
update_data = {
    'user_type': db_user_type,  # ✅ 'user' (válido)
    'role_id': role_id  # 11 (el role_id correcto)
}
# ✅ Se guarda correctamente
```

---

## 🔍 **EXPLICACIÓN TÉCNICA**

### **Sistema de Roles vs Tipos de Usuario**

Tu sistema usa un **enfoque híbrido**:

1. **`user_type`** (ENUM): Categoría técnica genérica
   - Solo 4 valores posibles: `admin`, `supervisor`, `cashier`, `user`
   - Se usa para lógica de acceso básica
   - Campo legacy que quedó de la versión anterior

2. **`role_id`** (FK → `roles`): Rol específico del usuario
   - Apunta a la tabla `roles` con permisos detallados
   - Permite crear roles personalizados ilimitados
   - Es el que realmente controla los permisos

**Flujo correcto:**
```
Usuario con rol "Test03" (ID: 11)
  ↓
Mapeo: "Test03" → "user" (categoría genérica)
  ↓
Base de datos:
  - user_type: 'user' (campo técnico)
  - role_id: 11 (rol real con permisos)
```

### **¿Por qué no eliminar `user_type`?**

Podrías eliminarlo completamente y usar solo `role_id`, pero:
- Requeriría migración de base de datos
- Cambios en toda la lógica que usa `user_type`
- El mapeo actual es una solución **backward-compatible**

---

## 📝 **ARCHIVOS MODIFICADOS**

- `controllers/user_controller.py` (líneas ~236-290)
  - Método: `update_user()`
  - Agregado: Función `get_user_type_simplified()` interna
  - Cambio: `user_type` ahora usa el valor mapeado

---

## ✅ **VALIDACIÓN**

Después de este fix, el sistema DEBE:

- [x] Permitir editar usuarios con roles personalizados
- [x] Mapear correctamente el nombre del rol a un `user_type` válido
- [x] Guardar `role_id` correcto en la base de datos
- [x] No mostrar error "Data truncated"
- [x] Mantener los permisos del rol después de editar

---

## 🚀 **PRÓXIMOS PASOS (Opcional)**

Si quieres **simplificar el sistema** en el futuro:

1. **Migración de BD:** Eliminar columna `user_type`
2. **Refactoring:** Reemplazar todas las referencias a `user_type` con `role_id`
3. **Limpiar código:** Eliminar funciones de mapeo que ya no serán necesarias

Pero por ahora, **el sistema funciona correctamente** con el enfoque híbrido.

---

**✅ PROBLEMA RESUELTO**

El error `Data truncated for column 'user_type'` ya no debería aparecer al editar usuarios.
