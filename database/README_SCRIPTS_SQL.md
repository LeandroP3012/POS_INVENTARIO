# 📚 Guía de Scripts SQL del Sistema POS

## 📋 Resumen de Archivos

### ✅ **ARCHIVO PRINCIPAL (Usar este)**

#### `scriptDB.txt` 
**Base de datos completa del sistema**
- ✨ **Script principal** que crea TODA la estructura de la base de datos
- 📦 **Contiene 11 tablas**: system_config, users, categories, suppliers, products, customers, sales, sale_details, stock_movements, user_sessions, activity_logs
- 🎯 **Estado**: Completo y funcional
- 🔧 **Cuándo usar**: Para crear la base de datos desde cero

---

### 🆕 **ARCHIVO COMPLEMENTARIO (Recomendado)**

#### `init_database_compatible.sql`
**Script de mejoras y sistema de roles**
- ⚡ **Propósito**: Complementa scriptDB.txt agregando funcionalidades nuevas
- 📌 **Requisito**: Ejecutar DESPUÉS de scriptDB.txt
- ✨ **Agrega**:
  - Sistema de roles y permisos (tabla `roles`)
  - Columna `role_id` en tabla `users`
  - Ampliación de enum `user_type` (agrega 'manager', 'employee')
  - Tabla opcional `units` (unidades de medida)
  - Migración automática de usuarios existentes a roles

**Características:**
- ✅ 100% compatible con scriptDB.txt
- ✅ Seguro para re-ejecutar (usa IF NOT EXISTS, INSERT IGNORE)
- ✅ No modifica datos existentes
- ✅ Verificaciones al final para confirmar éxito

---

### 📝 **ARCHIVOS ANTIGUOS (Ya unificados)**

Los siguientes archivos fueron unificados en `init_database_compatible.sql`:

#### `add_roles_system.sql`
- ❌ **No usar directamente**
- ℹ️ Sistema de roles (ahora en init_database_compatible.sql)
- 🔄 Funcionalidad integrada en el script compatible

#### `add_user_sessions_table.sql`
- ❌ **No usar** 
- ℹ️ La tabla `user_sessions` YA EXISTE en scriptDB.txt (línea 357)
- ⚠️ Ejecutar esto causaría conflicto

#### `create_products_tables.sql`
- ❌ **No usar**
- ℹ️ Las tablas de productos YA EXISTEN en scriptDB.txt
- ⚠️ **IMPORTANTE**: scriptDB.txt usa `code` no `sku` para productos
- 🔄 Funcionalidad ya incluida con la estructura correcta

#### `update_user_types.sql`
- ❌ **No usar**
- ℹ️ Actualización de tipos ya incluida en init_database_compatible.sql

---

## 🚀 Orden de Ejecución Recomendado

### Opción 1: Base de Datos Nueva (Instalación Limpia)

```sql
-- PASO 1: Crear la base de datos completa
SOURCE database/scriptDB.txt;

-- PASO 2: Agregar sistema de roles y mejoras
SOURCE database/init_database_compatible.sql;
```

### Opción 2: Base de Datos Existente (Solo agregar roles)

```sql
-- Solo ejecutar el script complementario
SOURCE database/init_database_compatible.sql;
```

---

## 📊 Estructura de la Base de Datos

### Tablas Principales (scriptDB.txt)

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `system_config` | Configuraciones del sistema | config_key, config_value, category |
| `users` | Usuarios del sistema | username, password_hash, **user_type**, email |
| `categories` | Categorías de productos | name, color, icon, parent_id |
| `suppliers` | Proveedores | code, name, contact_person |
| `products` | Productos inventario | **code** (no sku), name, barcode, sale_price |
| `customers` | Clientes | code, document_number, name |
| `sales` | Ventas realizadas | sale_number, customer_id, total_amount |
| `sale_details` | Detalle de ventas | sale_id, product_id, quantity |
| `stock_movements` | Movimientos inventario | product_id, movement_type, quantity |
| `user_sessions` | Sesiones activas | user_id, login_time, is_active |
| `activity_logs` | Logs de actividad | user_id, activity_type, description |

### Tablas Agregadas (init_database_compatible.sql)

| Tabla | Descripción | Campos Clave |
|-------|-------------|--------------|
| `roles` | **NUEVO** - Sistema de roles | code, name, permissions (JSON) |
| `units` | **OPCIONAL** - Unidades medida | symbol, name, type |

### Modificaciones en Tablas Existentes

**Tabla `users`:**
- ➕ Campo nuevo: `role_id INT` (FK a tabla roles)
- 🔄 Enum modificado: `user_type` ahora incluye 'manager', 'employee'

---

## ⚠️ Diferencias Importantes con scriptDB.txt

### 1. **Tabla Products**
```sql
-- ❌ NO USAR 'sku' - scriptDB.txt usa 'code'
-- En create_products_tables.sql (antiguo):
sku VARCHAR(50) NOT NULL

-- ✅ USAR 'code' - como en scriptDB.txt:
code VARCHAR(50) UNIQUE NOT NULL
```

### 2. **Tabla Categories**
```sql
-- scriptDB.txt tiene campos adicionales que NO están en create_products_tables.sql:
parent_id INT         -- Para categorías anidadas
color VARCHAR(7)      -- Color de la categoría
icon VARCHAR(50)      -- Icono de la categoría
sort_order INT        -- Orden de visualización
```

### 3. **Movimientos de Stock**
```sql
-- ❌ NO usar 'product_movements'
-- ✅ Usar 'stock_movements' (nombre correcto en scriptDB.txt)
```

---

## 🎯 Roles Predefinidos

El sistema incluye 5 roles predefinidos:

| ID | Código | Nombre | Descripción |
|----|--------|--------|-------------|
| 1 | `super_admin` | Super Admin | Acceso completo ["*"] |
| 2 | `admin` | Administrador | Acceso a la mayoría de funciones |
| 3 | `manager` | Gerente | Reportes y supervisión |
| 4 | `employee` | Empleado | Acceso básico para ventas |
| 5 | `cashier` | Cajero | Solo ventas y caja |

### Migración Automática de user_type a roles

```sql
admin      → role_id = 2 (Administrador)
supervisor → role_id = 3 (Gerente)
manager    → role_id = 3 (Gerente)
cashier    → role_id = 5 (Cajero)
user       → role_id = 4 (Empleado)
employee   → role_id = 4 (Empleado)
```

---

## 🔧 Compatibilidad con el Código Python

### Archivos Python que usan role_id:
- ✅ `models/user_model.py` (líneas 20-52)
- ✅ `models/role_model.py` (todo el archivo)
- ✅ `controllers/role_controller.py`
- ✅ `services/permission_service.py`

### user_type actualizado:
```python
# En models/user_model.py
self.valid_user_types = ['admin', 'supervisor', 'manager', 
                          'employee', 'cashier', 'user']
```

---

## ✅ Verificación Post-Instalación

Después de ejecutar los scripts, verifica:

```sql
-- 1. Ver roles creados
SELECT id, name, code, active FROM roles;

-- 2. Ver usuarios con roles asignados
SELECT u.username, u.user_type, r.name as role_name 
FROM users u 
LEFT JOIN roles r ON u.role_id = r.id;

-- 3. Ver todas las tablas
SHOW TABLES;

-- 4. Verificar estructura de users
DESCRIBE users;
```

**Deberías ver:**
- ✅ 5 roles en la tabla `roles`
- ✅ Todos los usuarios con `role_id` asignado
- ✅ 11-13 tablas (11 de scriptDB.txt + roles + opcional units)
- ✅ Campo `role_id` en tabla `users`

---

## 🗑️ Archivos a Mantener/Eliminar

### ✅ Mantener (Usar)
- `scriptDB.txt` - Base de datos principal
- `init_database_compatible.sql` - Mejoras y roles
- `connection.py` - Conexión a BD
- `er_diagram_dbdiagram.txt` - Diagrama ER

### 📦 Archivar (Ya integrados)
Puedes mover a una carpeta `database/archived/`:
- `add_roles_system.sql`
- `add_user_sessions_table.sql`
- `create_products_tables.sql`
- `update_user_types.sql`

### ⚠️ También existe:
- `init_database.sql` - Primera versión, reemplazada por `init_database_compatible.sql`

---

## 📞 Credenciales por Defecto

Después de ejecutar scriptDB.txt:

```
Usuario Admin:
- Username: admin
- Password: 123456
- Tipo: admin
- Rol: Administrador (role_id = 2)

Usuario Cajero:
- Username: cajero1  
- Password: 123456
- Tipo: cashier
- Rol: Cajero (role_id = 5)
```

**⚠️ IMPORTANTE**: Cambiar estas contraseñas en producción.

---

## 🐛 Solución de Problemas

### Error: "Column 'role_id' already exists"
✅ Normal - El script detecta que ya existe y continúa

### Error: "Duplicate entry for key 'PRIMARY'"
✅ Normal - Usa INSERT IGNORE, salta duplicados

### Error: "Table 'roles' already exists"  
✅ Normal - Usa IF NOT EXISTS, no causa problema

### Error: "Unknown column 'sku' in 'field list'"
❌ Estás usando create_products_tables.sql antiguo
✅ Usar solo scriptDB.txt que usa 'code'

---

## 📄 Resumen Final

```
PARA INSTALACIÓN NUEVA:
1. Ejecutar: scriptDB.txt
2. Ejecutar: init_database_compatible.sql
3. Verificar con las consultas de verificación

PARA AGREGAR ROLES A BD EXISTENTE:
1. Ejecutar solo: init_database_compatible.sql
2. Verificar que todos los usuarios tengan role_id

NO EJECUTAR:
- Los 4 archivos antiguos individuales
- create_products_tables.sql (estructura incompatible)
- add_user_sessions_table.sql (tabla ya existe)
```

---

## 📅 Versión del Documento
- **Fecha**: 2025-10-10
- **Versión**: 2.0
- **Compatible con**: MySQL 5.7+, MariaDB 10.2+

---

*Este documento fue generado automáticamente después de unificar y compatibilizar los scripts SQL del sistema POS.*
