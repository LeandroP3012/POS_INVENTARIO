# 🔐 VALIDACIÓN DEL SISTEMA DE PERMISOS - MÓDULO USUARIOS

## 📋 Resumen de Cambios Implementados

### 1. Nuevas Funcionalidades Agregadas

#### ✅ Botón Activar/Desactivar Usuario
- **Ubicación**: `views/user_management_view.py` (líneas 339-353)
- **Permisos requeridos**: 
  - `users.activate` - Para activar usuarios
  - `users.deactivate` - Para desactivar usuarios
- **Comportamiento**:
  - Botón dinámico que cambia según el estado del usuario seleccionado
  - "✓ Activar" (verde) cuando el usuario está inactivo
  - "⊗ Desactivar" (naranja) cuando el usuario está activo
  - No permite cambiar el estado del propio usuario logueado

#### ✅ Botón Exportar a Excel
- **Ubicación**: `views/user_management_view.py` (líneas 355-365)
- **Permiso requerido**: `users.export`
- **Características**:
  - Exporta la lista filtrada de usuarios
  - Incluye columnas: ID, Usuario, Nombre, Email, Rol, Estado, Último Acceso, Fecha Creación
  - Formato profesional con colores según estado (verde=activo, rojo=inactivo)
  - Hoja adicional con información de exportación

#### ✅ Función toggle_user_status()
- **Ubicación**: `views/user_management_view.py` (líneas 748-800)
- **Funcionalidad**:
  - Verifica el permiso correcto (activate o deactivate)
  - Impide cambiar el estado del usuario actual
  - Solicita confirmación antes de cambiar el estado
  - Actualiza la lista automáticamente

#### ✅ Función export_users_to_excel()
- **Ubicación**: `views/user_management_view.py` (líneas 802-954)
- **Funcionalidad**:
  - Verifica permiso `users.export`
  - Usa librería `openpyxl` para generar Excel
  - Aplica formato profesional con estilos
  - Incluye metadatos de la exportación

#### ✅ Actualización de on_user_select()
- **Ubicación**: `views/user_management_view.py` (líneas 625-671)
- **Mejoras**:
  - Ahora también habilita/deshabilita el botón de activar/desactivar
  - Actualiza el texto del botón según el estado del usuario
  - Verifica permisos antes de habilitar

### 2. Actualización del Controlador

#### ✅ Método update_user_status()
- **Ubicación**: `controllers/user_controller.py` (líneas 338-340)
- **Funcionalidad**:
  - Alias para `change_user_status()`
  - Permite actualizar el estado de un usuario
  - Valida que no se desactive el último administrador

### 3. Script de Actualización de Base de Datos

#### ✅ update_permissions_db.py
- **Ubicación**: Raíz del proyecto
- **Funcionalidad**:
  - Actualiza los permisos de todos los roles
  - Define permisos para módulo de usuarios:
    - `users.view` - Ver lista de usuarios
    - `users.create` - Crear nuevos usuarios
    - `users.edit` - Editar usuarios existentes
    - `users.delete` - Eliminar usuarios
    - `users.activate` - Activar usuarios inactivos
    - `users.deactivate` - Desactivar usuarios activos
    - `users.export` - Exportar usuarios a Excel

---

## 🎯 Permisos del Módulo de Usuarios

### Matriz de Permisos por Rol

| Permiso | Super Admin | Admin | Manager | Employee | Cashier |
|---------|------------|-------|---------|----------|---------|
| users.view | ✅ | ✅ | ✅ | ❌ | ❌ |
| users.create | ✅ | ✅ | ❌ | ❌ | ❌ |
| users.edit | ✅ | ✅ | ❌ | ❌ | ❌ |
| users.delete | ✅ | ✅ | ❌ | ❌ | ❌ |
| users.activate | ✅ | ✅ | ❌ | ❌ | ❌ |
| users.deactivate | ✅ | ✅ | ❌ | ❌ | ❌ |
| users.export | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 🧪 Pasos para Validar el Sistema de Permisos

### 1. Actualizar la Base de Datos

```powershell
# Ejecutar el script de actualización
cd c:\Users\USER\Desktop\POS
python update_permissions_db.py
```

**Resultado esperado**:
- Mensaje de éxito con los roles actualizados
- Conteo de permisos por rol

### 2. Crear un Rol Personalizado

1. Iniciar la aplicación POS
2. Ir al módulo de **Gestión de Roles**
3. Crear un nuevo rol: **"Gerente de Personal"**
4. Asignar SOLO los siguientes permisos:
   - ✅ users.view
   - ✅ users.edit
   - ✅ users.activate
   - ✅ users.deactivate
5. **NO** asignar:
   - ❌ users.create
   - ❌ users.delete
   - ❌ users.export

### 3. Crear un Usuario de Prueba

1. Crear un nuevo usuario: **"prueba_permisos"**
2. Asignar el rol: **"Gerente de Personal"**
3. Contraseña: `1234` (o la que prefieras)
4. Guardar

### 4. Cerrar Sesión y Probar con el Usuario de Prueba

1. **Cerrar sesión** del usuario actual
2. **Iniciar sesión** con: `prueba_permisos` / `1234`
3. Ir al módulo de **Gestión de Usuarios**

### 5. Validaciones Esperadas

#### ✅ LO QUE DEBE VER Y HACER:

1. **Ver la lista de usuarios** ✓
   - Permiso: `users.view`
   - Debe ver la tabla completa con todos los usuarios

2. **Editar usuarios** ✓
   - Permiso: `users.edit`
   - Debe ver el botón "✏️ Editar"
   - Al seleccionar un usuario, el botón debe habilitarse
   - Puede abrir el formulario de edición

3. **Activar usuarios inactivos** ✓
   - Permiso: `users.activate`
   - Al seleccionar un usuario inactivo, debe ver "✓ Activar"
   - El botón debe estar habilitado
   - Puede activar el usuario

4. **Desactivar usuarios activos** ✓
   - Permiso: `users.deactivate`
   - Al seleccionar un usuario activo, debe ver "⊗ Desactivar"
   - El botón debe estar habilitado
   - Puede desactivar el usuario

#### ❌ LO QUE NO DEBE VER:

1. **Botón "➕ Nuevo Usuario"** ✗
   - Permiso faltante: `users.create`
   - El botón NO debe aparecer en la barra de herramientas

2. **Botón "🗑️ Eliminar"** ✗
   - Permiso faltante: `users.delete`
   - El botón NO debe aparecer en la barra de herramientas

3. **Botón "📄 Exportar Excel"** ✗
   - Permiso faltante: `users.export`
   - El botón NO debe aparecer en la barra de herramientas

### 6. Validación de Mensajes de Error

Si intenta acceder a una función sin permiso (por ejemplo, mediante API):

```
❌ Acceso Denegado
No tienes permisos para [acción] usuarios
```

---

## 📊 Validación Completa por Permiso

### Permiso: users.view

**Prueba 1**: Sin permiso
- ❌ No debe poder acceder al módulo
- ❌ Debe ser redirigido o mostrar error

**Prueba 2**: Con permiso
- ✅ Debe ver la lista completa de usuarios
- ✅ Debe ver el contador de usuarios
- ✅ Debe poder usar filtros y búsqueda

---

### Permiso: users.create

**Prueba 1**: Sin permiso
- ❌ Botón "➕ Nuevo Usuario" NO visible
- ❌ Si intenta acceder directo, debe mostrar error

**Prueba 2**: Con permiso
- ✅ Botón "➕ Nuevo Usuario" visible
- ✅ Puede abrir formulario de creación
- ✅ Puede guardar nuevo usuario

---

### Permiso: users.edit

**Prueba 1**: Sin permiso
- ❌ Botón "✏️ Editar" NO visible
- ❌ Doble clic en usuario no abre editor

**Prueba 2**: Con permiso
- ✅ Botón "✏️ Editar" visible
- ✅ Al seleccionar usuario, botón se habilita
- ✅ Puede abrir formulario y modificar datos

---

### Permiso: users.delete

**Prueba 1**: Sin permiso
- ❌ Botón "🗑️ Eliminar" NO visible

**Prueba 2**: Con permiso
- ✅ Botón "🗑️ Eliminar" visible
- ✅ Al seleccionar usuario, botón se habilita
- ✅ Puede eliminar usuarios (con confirmación)
- ❌ No puede eliminar su propio usuario

---

### Permiso: users.activate

**Prueba 1**: Sin permiso
- ❌ Botón "✓ Activar" deshabilitado
- ❌ Si intenta activar, muestra error de permisos

**Prueba 2**: Con permiso
- ✅ Al seleccionar usuario inactivo, botón "✓ Activar" habilitado
- ✅ Puede activar usuarios inactivos
- ✅ Actualiza tabla automáticamente

---

### Permiso: users.deactivate

**Prueba 1**: Sin permiso
- ❌ Botón "⊗ Desactivar" deshabilitado
- ❌ Si intenta desactivar, muestra error de permisos

**Prueba 2**: Con permiso
- ✅ Al seleccionar usuario activo, botón "⊗ Desactivar" habilitado
- ✅ Puede desactivar usuarios activos
- ❌ No puede desactivar su propio usuario
- ✅ Actualiza tabla automáticamente

---

### Permiso: users.export

**Prueba 1**: Sin permiso
- ❌ Botón "📄 Exportar Excel" NO visible

**Prueba 2**: Con permiso
- ✅ Botón "📄 Exportar Excel" visible
- ✅ Puede exportar usuarios a Excel
- ✅ Archivo incluye formato profesional
- ✅ Hoja adicional con metadatos

---

## 🛠️ Troubleshooting

### Problema: Los permisos no se actualizan después de cambiar el rol

**Solución**:
1. Cerrar sesión completamente
2. Volver a iniciar sesión
3. El sistema recarga permisos en cada login

### Problema: Botones no aparecen/desaparecen correctamente

**Solución**:
1. Verificar que los permisos están correctamente asignados en la BD
2. Ejecutar: `python update_permissions_db.py`
3. Verificar en la tabla `roles` que el campo `permissions` tiene el formato JSON correcto

### Problema: Error al exportar a Excel

**Solución**:
```powershell
# Instalar openpyxl si no está instalado
pip install openpyxl
```

### Problema: Usuario puede hacer acciones sin permiso

**Solución**:
1. Verificar que el método tiene validación de permisos:
```python
if not self.has_permission('users.xxx'):
    messagebox.showerror("Acceso Denegado", ...)
    return
```
2. Verificar que el servicio de permisos está funcionando correctamente

---

## 📝 Checklist de Validación

### Pre-requisitos
- [ ] Script `update_permissions_db.py` ejecutado
- [ ] Base de datos actualizada con nuevos permisos
- [ ] Librería `openpyxl` instalada

### Validación Básica
- [ ] Rol personalizado creado ("Gerente de Personal")
- [ ] Usuario de prueba creado con rol personalizado
- [ ] Login exitoso con usuario de prueba
- [ ] Módulo de usuarios accesible

### Validación de Visibilidad de Botones
- [ ] ✅ Botón "✏️ Editar" VISIBLE
- [ ] ✅ Botón "✓ Activar" / "⊗ Desactivar" VISIBLE
- [ ] ❌ Botón "➕ Nuevo Usuario" NO VISIBLE
- [ ] ❌ Botón "🗑️ Eliminar" NO VISIBLE
- [ ] ❌ Botón "📄 Exportar Excel" NO VISIBLE

### Validación de Funcionalidad
- [ ] ✅ Puede ver lista de usuarios
- [ ] ✅ Puede editar usuarios
- [ ] ✅ Puede activar usuarios inactivos
- [ ] ✅ Puede desactivar usuarios activos
- [ ] ❌ No puede crear usuarios (botón no existe)
- [ ] ❌ No puede eliminar usuarios (botón no existe)
- [ ] ❌ No puede exportar a Excel (botón no existe)

### Validación de Seguridad
- [ ] No puede cambiar estado de su propio usuario
- [ ] Mensajes de error claros cuando falta permiso
- [ ] Cambios se reflejan inmediatamente en la tabla

---

## 🎓 Próximos Pasos

Una vez validado el módulo de usuarios, aplicar la misma metodología a los otros módulos:

1. **Módulo de Roles** (`roles.*`)
   - roles.view, roles.create, roles.edit, roles.delete

2. **Módulo de Productos/Inventario** (`inventory.*`)
   - inventory.view, inventory.create, inventory.edit, inventory.delete
   - inventory.reports, inventory.export

3. **Módulo de Ventas** (`sales.*`)
   - sales.view, sales.create, sales.edit
   - sales.reports, sales.export

4. **Módulo de Reportes** (`reports.*`)
   - reports.sales, reports.inventory, reports.users

5. **Configuración del Sistema** (`system.*`)
   - system.config, system.backup, system.reports

---

## 📞 Soporte

Si encuentras algún problema durante la validación:

1. Revisar los logs del sistema: `logs/pos_system.log`
2. Verificar permisos en la base de datos: tabla `roles`, campo `permissions`
3. Verificar sesión del usuario: tabla `user_sessions`

---

**Fecha de creación**: 2025-01-06  
**Versión**: 1.0  
**Módulo validado**: Gestión de Usuarios
