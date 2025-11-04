# Solución: Cambio de Estado de Usuarios (Activo/Inactivo)

## Problema Identificado

El botón de cambio de estado en el módulo de Gestión de Usuarios no funcionaba.

### Causa Raíz

El controlador `user_controller.py` intentaba actualizar una columna llamada **`status`** que no existe en la tabla `users`.

La tabla `users` tiene una columna llamada **`active`** (BOOLEAN), no `status`.

## Código Antes (❌ Incorrecto):

```python
# controllers/user_controller.py - línea 442
def change_user_status(self, user_id: int, status: str) -> bool:
    # ...
    # Convertir status a formato de base de datos
    status_value = 1 if status == 'active' else 0
    
    # Actualizar estado
    success = self.user_model.update_user(user_id, {'status': status_value})
    #                                                  ^^^^^^
    #                                          Columna que NO EXISTE
```

## Código Después (✅ Correcto):

```python
# controllers/user_controller.py - línea 442
def change_user_status(self, user_id: int, status: str) -> bool:
    # ...
    # Convertir status a booleano para la columna 'active'
    active_value = True if status == 'active' else False
    
    # Actualizar estado usando la columna 'active' (no 'status')
    success = self.user_model.update_user(user_id, {'active': active_value})
    #                                                  ^^^^^^
    #                                          Columna que SÍ EXISTE
```

## Estructura de la Tabla `users`

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    user_type ENUM('admin', 'supervisor', 'cashier', 'user') DEFAULT 'user',
    role_id INT DEFAULT NULL,
    active BOOLEAN DEFAULT TRUE,        <--- Esta es la columna correcta
    avatar_path VARCHAR(255),
    preferences JSON,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ...
);
```

## Flujo de Datos Correcto

### 1. **Vista obtiene usuarios** (`user_management_view.py`):
```python
def load_users_data(self):
    self.users_data = self.user_controller.get_all_users()
    # Cada usuario tiene: {'status': 'active'} o {'status': 'inactive'}
```

### 2. **Controlador convierte para la vista** (`user_controller.py`):
```python
def get_all_users(self):
    formatted_user = {
        'status': 'active' if user.get('active') else 'inactive',
        # Convierte: active (bool) → status (string)
    }
```

### 3. **Usuario hace clic en "Cambiar Estado"** → Llama a `toggle_user_status()`

### 4. **Controlador actualiza la BD** (`user_controller.py`):
```python
def change_user_status(self, user_id: int, status: str):
    # Convierte: status (string) → active (bool)
    active_value = True if status == 'active' else False
    success = self.user_model.update_user(user_id, {'active': active_value})
```

### 5. **Modelo ejecuta UPDATE** (`user_model.py`):
```python
def update_user(self, user_id: int, user_data: Dict):
    # user_data = {'active': True} o {'active': False}
    return self.update(user_id, user_data)
    # Ejecuta: UPDATE users SET active = 1/0 WHERE id = user_id
```

## Conversiones de Datos

| Capa | Formato | Valor Activo | Valor Inactivo |
|------|---------|--------------|----------------|
| **Base de Datos** | BOOLEAN/TINYINT | `1` o `TRUE` | `0` o `FALSE` |
| **Modelo** | Boolean | `True` | `False` |
| **Controlador (entrada)** | String | `'active'` | `'inactive'` |
| **Controlador (salida)** | String | `'active'` | `'inactive'` |
| **Vista** | String | `'active'` | `'inactive'` |
| **Vista (display)** | String | `'✅ Activo'` | `'❌ Inactivo'` |

## Protecciones Implementadas

1. **No permitir desactivar el propio usuario**:
   ```python
   if self.selected_user.get('username') == self.user_data.get('username', ''):
       messagebox.showerror("Error", "❌ No puedes cambiar el estado de tu propio usuario")
       return
   ```

2. **No permitir desactivar el último administrador**:
   ```python
   if status == 'inactive' and existing_user.get('user_type') == 'admin':
       active_admin_count = self.count_active_users_by_type('admin')
       if active_admin_count <= 1:
           return False
   ```

3. **Verificar permisos**:
   ```python
   required_permission = 'users.deactivate' if is_active else 'users.activate'
   if not self.has_permission(required_permission):
       messagebox.showerror("Acceso Denegado", ...)
       return
   ```

## Prueba

1. Abre el módulo de **Gestión de Usuarios**
2. Selecciona cualquier usuario (excepto el tuyo)
3. Haz clic en el botón **"Cambiar Estado"** (ícono con check/cross)
4. Confirma la acción
5. Verifica que:
   - El estado cambia en la tabla
   - Se muestra el mensaje de éxito
   - Las estadísticas del footer se actualizan
   - Se deshabilitan los botones después del cambio

## Archivos Modificados

- ✅ `controllers/user_controller.py` - Método `change_user_status()`
  - Cambio: `{'status': status_value}` → `{'active': active_value}`
  - Cambio: `status_value = 1 if ...` → `active_value = True if ...`

---

**Fecha de corrección**: 31 de Octubre, 2025
**Estado**: ✅ Corregido y funcionando
