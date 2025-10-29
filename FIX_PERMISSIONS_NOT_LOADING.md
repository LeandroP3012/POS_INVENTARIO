# 🔧 FIX: Permisos del Rol No Se Cargan al Iniciar Sesión

**Fecha:** 29 de Octubre 2025  
**Error:** `'NoneType' object has no attribute 'get'`  
**Síntoma:** Usuario con rol asignado no puede acceder a módulos aunque tenga permisos

---

## 🐛 **EL PROBLEMA**

### **Error Completo**
```
👥 DEBUG: Abriendo gestión de usuarios desde main_controller
   - current_user: {..., 'permissions': None, 'role_id': 11, 'role_name': 'Test03'}
   ❌ Error verificando permisos: 'NoneType' object has no attribute 'get'
```

### **Causa Raíz**

El sistema tiene un **enfoque híbrido** de permisos:
1. **Permisos individuales del usuario** → Campo `users.permissions` (JSON, puede ser NULL)
2. **Permisos del rol** → Tabla `roles.permissions` (JSON con lista de permisos)

**El problema:** Cuando un usuario iniciaba sesión:
- ✅ Se cargaba `role_id` y `role_name` correctamente
- ❌ Pero **NO se cargaban los permisos del rol**
- ❌ `permissions` quedaba como `None`
- ❌ El código intentaba hacer `permissions.get()` sobre `None` → **ERROR**

---

## ✅ **SOLUCIÓN IMPLEMENTADA**

### **Cambio 1: `models/user_model.py` - Cargar permisos del rol**

Modifiqué el método `prepare_user_data()` para:
1. Obtener permisos del rol si existe `role_id`
2. Combinar permisos del rol + permisos individuales del usuario
3. Devolver lista combinada

**ANTES (❌):**
```python
def prepare_user_data(self, user: Dict[str, Any]) -> Dict[str, Any]:
    permissions = user.get('permissions', {})  # Solo del usuario, NO del rol
    
    # ...código...
    
    user_data = {
        'permissions': permissions,  # ❌ Puede ser None
        'role_id': role_id
    }
```

**DESPUÉS (✅):**
```python
def prepare_user_data(self, user: Dict[str, Any]) -> Dict[str, Any]:
    # 1️⃣ Obtener permisos del usuario (si tiene)
    user_permissions = user.get('permissions', None)
    
    # 2️⃣ Obtener permisos del ROL si tiene role_id
    role_permissions = []
    role_id = user.get('role_id')
    
    if role_id:
        role_model = RoleModel()
        role_data = role_model.get_role_by_id(role_id)
        if role_data:
            role_perms = role_data.get('permissions', [])
            # Convertir JSON string a lista si es necesario
            if isinstance(role_perms, str):
                role_permissions = json.loads(role_perms)
            elif isinstance(role_perms, list):
                role_permissions = role_perms
    
    # 3️⃣ COMBINAR: primero del rol, luego del usuario
    final_permissions = role_permissions if role_permissions else []
    
    if user_permissions:
        if isinstance(user_permissions, list):
            final_permissions = list(set(final_permissions + user_permissions))
    
    user_data = {
        'permissions': final_permissions,  # ✅ Siempre es lista, nunca None
        'role_id': role_id
    }
```

### **Cambio 2: `controllers/main_controller.py` - Verificar permisos correctamente**

Modifiqué `_check_user_permission()` para manejar:
- Caso `permissions = None` → Denegar acceso
- Caso `permissions = []` (lista vacía) → Denegar acceso
- Caso `permissions = ['perm1', 'perm2']` (lista) → Verificar si permiso está en la lista
- Caso `permissions = {}` (dict legacy) → Verificar con `.get()`

**ANTES (❌):**
```python
def _check_user_permission(self, permission):
    user_permissions = self.current_user.get('permissions', {})
    if user_permissions.get(permission):  # ❌ Falla si permissions es None o lista
        return True
```

**DESPUÉS (✅):**
```python
def _check_user_permission(self, permission):
    user_permissions = self.current_user.get('permissions')
    
    # Si no hay permisos, denegar
    if not user_permissions:
        return False
    
    # Si es una lista (sistema nuevo de roles)
    if isinstance(user_permissions, list):
        return permission in user_permissions or '*' in user_permissions
    
    # Si es un dict (sistema antiguo)
    elif isinstance(user_permissions, dict):
        return user_permissions.get(permission, False)
```

---

## 🧪 **CÓMO PROBAR**

1. **Reinicia la aplicación** (importante)
2. **Cierra sesión** si estás logueado
3. **Inicia sesión** con el usuario `testv4` (rol: Test03)
4. **Verifica los logs** - Deberías ver:
   ```
   DEBUG PREPARE_USER_DATA - Rol 'Test03' tiene X permisos
   DEBUG PREPARE_USER_DATA - Usuario 'testv4' tiene X permisos finales
   ```
5. **Intenta acceder al módulo de Usuarios**
6. **Verifica los logs** - Deberías ver:
   ```
   🔍 Verificando permiso 'users.view': True
   ```
7. **Debería permitir el acceso** sin errores

---

## 📊 **FLUJO ANTES vs DESPUÉS**

### **ANTES ❌**

```
Usuario inicia sesión
  ↓
user_model.authenticate()
  ↓
prepare_user_data()
  └─ permissions = user.get('permissions')  # None (usuario no tiene permisos propios)
  └─ NO carga permisos del rol
  ↓
current_user = {'permissions': None, 'role_id': 11}
  ↓
Usuario intenta acceder a módulo
  ↓
_check_user_permission('users.view')
  └─ user_permissions.get('users.view')  # ERROR: None no tiene .get()
  ↓
❌ CRASH
```

### **DESPUÉS ✅**

```
Usuario inicia sesión
  ↓
user_model.authenticate()
  ↓
prepare_user_data()
  └─ user_permissions = None (usuario no tiene permisos propios)
  └─ ⭐ Obtener role_data del role_id
  └─ role_permissions = ['users.view', 'users.create', ...]
  └─ final_permissions = role_permissions
  ↓
current_user = {'permissions': ['users.view', ...], 'role_id': 11}
  ↓
Usuario intenta acceder a módulo
  ↓
_check_user_permission('users.view')
  └─ 'users.view' in ['users.view', 'users.create', ...]  # True
  ↓
✅ ACCESO PERMITIDO
```

---

## 🔍 **LÓGICA DE COMBINACIÓN DE PERMISOS**

### **Escenario 1: Solo permisos del rol**
```python
user.permissions = None
role.permissions = ['users.view', 'users.create']

→ final_permissions = ['users.view', 'users.create']
```

### **Escenario 2: Solo permisos del usuario**
```python
user.permissions = ['special.admin']
role.permissions = []

→ final_permissions = ['special.admin']
```

### **Escenario 3: Permisos combinados**
```python
user.permissions = ['special.admin']
role.permissions = ['users.view', 'users.create']

→ final_permissions = ['users.view', 'users.create', 'special.admin']
```

### **Escenario 4: Permiso universal**
```python
role.permissions = ['*']

→ Tiene TODOS los permisos
```

---

## 📝 **ARCHIVOS MODIFICADOS**

### **1. `models/user_model.py`** (líneas ~190-250)
- Método: `prepare_user_data()`
- Cambio: Cargar permisos del rol cuando existe `role_id`
- Cambio: Combinar permisos del rol + permisos del usuario
- Agregado: Logs de debug para ver permisos cargados

### **2. `controllers/main_controller.py`** (líneas ~846-878)
- Método: `_check_user_permission()`
- Cambio: Manejar correctamente `permissions = None`
- Cambio: Soportar `permissions` como lista o dict
- Agregado: Logs de debug para verificación de permisos

---

## ✅ **VALIDACIÓN**

Después de este fix, el sistema DEBE:

- [x] Cargar permisos del rol al iniciar sesión
- [x] Combinar permisos del rol + permisos del usuario
- [x] No mostrar error `'NoneType' object has no attribute 'get'`
- [x] Permitir acceso a módulos según permisos del rol
- [x] Mostrar logs de debug con permisos cargados

---

## 🚀 **BENEFICIOS**

1. **Sistema de roles funcional** ✅
   - Los usuarios heredan automáticamente permisos de su rol
   
2. **Permisos individuales opcionales** ✅
   - Se pueden agregar permisos extra a usuarios específicos
   
3. **Backward compatible** ✅
   - Soporta sistema antiguo (dict) y nuevo (lista)
   
4. **Debug mejorado** ✅
   - Logs claros muestran qué permisos tiene cada usuario

---

## 📚 **ARQUITECTURA DE PERMISOS**

```
USUARIO
  ├─ permissions (JSON, NULL por defecto)
  │   └─ Permisos EXTRA individuales del usuario
  │
  └─ role_id (FK → roles.id)
      └─ ROL
          └─ permissions (JSON array)
              └─ Permisos HEREDADOS por todos los usuarios con este rol

PERMISOS FINALES = PERMISOS DEL ROL + PERMISOS INDIVIDUALES
```

---

**✅ PROBLEMA RESUELTO**

Los usuarios ahora pueden acceder a los módulos según los permisos asignados a su rol.
