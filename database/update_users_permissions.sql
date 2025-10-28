-- ============================================================================
-- SISTEMA DE PERMISOS - MÓDULO DE USUARIOS
-- Fecha: 2025-10-28
-- Descripción: Define estructura completa de permisos para el módulo de usuarios
-- ============================================================================

-- Lista completa de permisos disponibles para USUARIOS:
-- 1. users.view           - Ver lista de usuarios en el dashboard
-- 2. users.create         - Crear nuevos usuarios
-- 3. users.edit           - Editar usuarios existentes
-- 4. users.delete         - Eliminar usuarios
-- 5. users.activate       - Activar usuarios desactivados
-- 6. users.deactivate     - Desactivar usuarios activos
-- 7. users.export         - Exportar lista de usuarios a Excel

-- ============================================================================
-- ACTUALIZAR ROLES EXISTENTES CON NUEVOS PERMISOS
-- ============================================================================

-- Super Admin: Todos los permisos
UPDATE roles SET permissions = JSON_ARRAY('*') WHERE code = 'super_admin';

-- Administrador: Todos los permisos de usuarios
UPDATE roles SET permissions = JSON_ARRAY(
    'users.view',
    'users.create', 
    'users.edit',
    'users.delete',
    'users.activate',
    'users.deactivate',
    'users.export',
    'roles.view',
    'roles.create',
    'roles.edit',
    'roles.delete',
    'system.config',
    'system.backup',
    'system.reports',
    'inventory.view',
    'inventory.create',
    'inventory.edit',
    'inventory.delete',
    'inventory.reports',
    'inventory.export',
    'sales.view',
    'sales.create',
    'sales.edit',
    'sales.reports',
    'sales.export',
    'dashboard.view',
    'dashboard.stats',
    'reports.sales',
    'reports.inventory',
    'reports.users'
) WHERE code = 'admin';

-- Gerente: Ver usuarios, ver estadísticas
UPDATE roles SET permissions = JSON_ARRAY(
    'users.view',
    'inventory.view',
    'inventory.reports',
    'inventory.export',
    'sales.view',
    'sales.create',
    'sales.reports',
    'sales.export',
    'dashboard.view',
    'dashboard.stats',
    'reports.sales',
    'reports.inventory'
) WHERE code = 'manager';

-- Empleado: Sin permisos de usuarios
UPDATE roles SET permissions = JSON_ARRAY(
    'sales.view',
    'sales.create',
    'inventory.view',
    'dashboard.view'
) WHERE code = 'employee';

-- Cajero: Sin permisos de usuarios
UPDATE roles SET permissions = JSON_ARRAY(
    'sales.create',
    'sales.view_own',
    'cash.register',
    'dashboard.view'
) WHERE code = 'cashier';

-- ============================================================================
-- VERIFICAR PERMISOS
-- ============================================================================

-- Ver permisos de todos los roles
SELECT 
    id,
    name,
    code,
    permissions,
    active
FROM roles
ORDER BY id;

-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
-- 
-- FORMATO DE PERMISOS:
-- - JSON Array de strings
-- - Formato: "modulo.accion"
-- - Ejemplo: "users.create", "users.edit"
-- - Super admin: ["*"] (acceso total)
--
-- PERMISOS DEL MÓDULO DE USUARIOS:
-- users.view         -> Ver dashboard de usuarios (lista completa)
-- users.create       -> Botón "Nuevo Usuario" habilitado
-- users.edit         -> Botón "Editar" habilitado en cada fila
-- users.delete       -> Botón "Eliminar" habilitado en cada fila
-- users.activate     -> Botón "Activar" visible para usuarios inactivos
-- users.deactivate   -> Botón "Desactivar" visible para usuarios activos
-- users.export       -> Botón "Exportar Excel" habilitado
--
-- VALIDACIÓN EN LA APLICACIÓN:
-- - Los permisos se verifican en tiempo real
-- - Si un botón no tiene permiso, se oculta o deshabilita
-- - Los cambios en permisos requieren re-login para aplicarse
--
-- ============================================================================
