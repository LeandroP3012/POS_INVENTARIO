-- =============================================================================
-- SCRIPT DE INICIALIZACIÓN COMPLEMENTARIA DEL SISTEMA POS
-- =============================================================================
-- Este script COMPLEMENTA la estructura existente en scriptDB.txt
-- Solo agrega las funcionalidades que NO existen en el script principal
-- =============================================================================
-- IMPORTANTE: Ejecutar DESPUÉS de scriptDB.txt
-- =============================================================================
-- Fecha: 2025-10-10
-- Versión: 2.0 (Compatible 100% con scriptDB.txt)
-- =============================================================================

USE pos_system;

-- =============================================================================
-- SECCIÓN 1: ACTUALIZACIÓN DE TIPOS DE USUARIO
-- =============================================================================
-- scriptDB.txt tiene: ENUM('admin', 'supervisor', 'cashier', 'user')
-- Agregamos: 'manager', 'employee' para compatibilidad con el código Python
-- =============================================================================

ALTER TABLE users MODIFY COLUMN user_type 
    ENUM('admin', 'supervisor', 'manager', 'employee', 'cashier', 'user') 
    DEFAULT 'user';

SELECT '✓ Tipos de usuario actualizados' as 'PASO 1';

-- =============================================================================
-- SECCIÓN 2: SISTEMA DE ROLES Y PERMISOS (NUEVO)
-- =============================================================================
-- Esta tabla NO existe en scriptDB.txt - La creamos
-- =============================================================================

CREATE TABLE IF NOT EXISTS roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    permissions JSON COMMENT 'Permisos del rol en formato JSON',
    system_role BOOLEAN DEFAULT FALSE COMMENT 'Roles del sistema (protegidos)',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    
    INDEX idx_name (name),
    INDEX idx_code (code),
    INDEX idx_active (active),
    INDEX idx_system_role (system_role),
    
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Roles del sistema con permisos personalizables';

SELECT '✓ Tabla de roles creada' as 'PASO 2';

-- -----------------------------------------------------------------------------
-- Insertar roles predefinidos del sistema
-- -----------------------------------------------------------------------------

-- Super Admin (id=1)
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(1, 'Super Admin', 'super_admin', 'Acceso completo al sistema, puede gestionar todo', '["*"]', TRUE, TRUE);

-- Administrador (id=2)
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(2, 'Administrador', 'admin', 'Administrador del sistema con acceso a la mayoría de funciones', 
'["users.view", "users.create", "users.edit", "users.delete", "roles.view", "roles.create", "roles.edit", "system.config", "system.backup", "system.reports", "inventory.view", "inventory.edit", "inventory.reports", "sales.view", "sales.create", "sales.reports", "dashboard.view"]', 
TRUE, TRUE);

-- Gerente (id=3)
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(3, 'Gerente', 'manager', 'Gerente de tienda con acceso a reportes y supervisión', 
'["users.view", "inventory.view", "inventory.reports", "sales.view", "sales.create", "sales.reports", "dashboard.view", "dashboard.stats"]', 
TRUE, TRUE);

-- Empleado (id=4)
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(4, 'Empleado', 'employee', 'Empleado con acceso básico para ventas', 
'["sales.view", "sales.create", "inventory.view", "dashboard.view"]', 
TRUE, TRUE);

-- Cajero (id=5)
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(5, 'Cajero', 'cashier', 'Cajero con acceso solo a ventas y caja', 
'["sales.create", "sales.view_own", "cash.register"]', 
TRUE, TRUE);

SELECT '✓ Roles predefinidos insertados' as 'PASO 3';

-- =============================================================================
-- SECCIÓN 3: AGREGAR COLUMNA role_id A TABLA users
-- =============================================================================
-- Extender la tabla users existente de scriptDB.txt
-- =============================================================================

-- Verificar si la columna ya existe
SET @column_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'users'
    AND COLUMN_NAME = 'role_id'
);

-- Agregar columna solo si no existe
SET @sql = IF(@column_exists = 0,
    'ALTER TABLE users ADD COLUMN role_id INT DEFAULT NULL AFTER user_type',
    'SELECT "Columna role_id ya existe" as info');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar índice si no existe
SET @index_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'users'
    AND INDEX_NAME = 'idx_role_id'
);

SET @sql = IF(@index_exists = 0,
    'ALTER TABLE users ADD INDEX idx_role_id (role_id)',
    'SELECT "Índice idx_role_id ya existe" as info');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar foreign key solo si no existe
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
    AND TABLE_NAME = 'users'
    AND CONSTRAINT_TYPE = 'FOREIGN KEY'
    AND CONSTRAINT_NAME LIKE '%role%'
);

SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE users ADD CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL',
    'SELECT "Foreign key para role_id ya existe" as info');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT '✓ Columna role_id agregada a tabla users' as 'PASO 4';

-- =============================================================================
-- SECCIÓN 4: MIGRAR DATOS EXISTENTES A ROLES
-- =============================================================================
-- Asignar roles basados en user_type existente
-- =============================================================================

UPDATE users SET role_id = 2 WHERE user_type = 'admin' AND role_id IS NULL;      -- Admin -> Administrador
UPDATE users SET role_id = 3 WHERE user_type = 'supervisor' AND role_id IS NULL; -- Supervisor -> Gerente
UPDATE users SET role_id = 5 WHERE user_type = 'cashier' AND role_id IS NULL;    -- Cashier -> Cajero
UPDATE users SET role_id = 4 WHERE user_type = 'user' AND role_id IS NULL;       -- User -> Empleado
UPDATE users SET role_id = 3 WHERE user_type = 'manager' AND role_id IS NULL;    -- Manager -> Gerente
UPDATE users SET role_id = 4 WHERE user_type = 'employee' AND role_id IS NULL;   -- Employee -> Empleado

-- Asignar rol por defecto (Empleado) a usuarios sin rol
UPDATE users SET role_id = 4 WHERE role_id IS NULL;

SELECT '✓ Usuarios migrados a sistema de roles' as 'PASO 5';

-- =============================================================================
-- SECCIÓN 5: TABLA COMPLEMENTARIA - UNIDADES DE MEDIDA (OPCIONAL)
-- =============================================================================
-- Esta tabla NO existe en scriptDB.txt pero puede ser útil
-- Puedes comentar esta sección si no la necesitas
-- =============================================================================

CREATE TABLE IF NOT EXISTS units (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    type ENUM('weight', 'length', 'volume', 'unit', 'other') DEFAULT 'unit',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_symbol (symbol),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Unidades de medida para productos (complementaria)';

-- Insertar unidades por defecto
INSERT IGNORE INTO units (name, symbol, type, status) VALUES
('Unidad', 'un', 'unit', 'active'),
('Kilogramo', 'kg', 'weight', 'active'),
('Gramo', 'g', 'weight', 'active'),
('Litro', 'L', 'volume', 'active'),
('Mililitro', 'ml', 'volume', 'active'),
('Metro', 'm', 'length', 'active'),
('Centímetro', 'cm', 'length', 'active'),
('Paquete', 'paq', 'unit', 'active'),
('Caja', 'cja', 'unit', 'active'),
('Docena', 'doc', 'unit', 'active')
ON DUPLICATE KEY UPDATE name = VALUES(name);

SELECT '✓ Tabla de unidades creada (opcional)' as 'PASO 6';

-- =============================================================================
-- RESUMEN DE TABLAS EXISTENTES EN scriptDB.txt (NO MODIFICADAS)
-- =============================================================================
-- Las siguientes tablas YA EXISTEN en scriptDB.txt y NO se tocan aquí:
-- 
-- ✓ system_config       - Configuraciones del sistema
-- ✓ users              - Usuarios (solo se agregó role_id)
-- ✓ categories         - Categorías con color, icon, parent_id, sort_order
-- ✓ suppliers          - Proveedores
-- ✓ products           - Productos (usa 'code' NO 'sku')
-- ✓ customers          - Clientes
-- ✓ sales              - Ventas
-- ✓ sale_details       - Detalles de ventas
-- ✓ stock_movements    - Movimientos de stock
-- ✓ user_sessions      - Sesiones de usuario (YA EXISTE)
-- ✓ activity_logs      - Logs de actividad
-- 
-- =============================================================================
-- TABLAS AGREGADAS POR ESTE SCRIPT:
-- =============================================================================
-- + roles              - Sistema de roles y permisos (NUEVO)
-- + units              - Unidades de medida (OPCIONAL, complementaria)
-- 
-- MODIFICACIONES:
-- ~ users.user_type    - Enum ampliado (agregado 'manager', 'employee')
-- ~ users.role_id      - Nueva columna (FK a roles)
-- =============================================================================

-- =============================================================================
-- VERIFICACIONES FINALES
-- =============================================================================

SELECT '' as '';
SELECT '============================================' as '';
SELECT '   INICIALIZACIÓN COMPLEMENTARIA EXITOSA' as 'RESULTADO';
SELECT '============================================' as '';

SELECT '' as '';
SELECT '1. ROLES CREADOS:' as '';
SELECT id, name, code, 
       CASE WHEN active THEN 'Activo' ELSE 'Inactivo' END as estado,
       CASE WHEN system_role THEN 'Sistema' ELSE 'Personalizado' END as tipo
FROM roles 
ORDER BY id;

SELECT '' as '';
SELECT '2. USUARIOS CON ROLES ASIGNADOS:' as '';
SELECT u.id, u.username, u.full_name, u.user_type as tipo_usuario, 
       IFNULL(r.name, 'Sin Rol') as rol_asignado,
       CASE WHEN u.active THEN 'Activo' ELSE 'Inactivo' END as estado
FROM users u 
LEFT JOIN roles r ON u.role_id = r.id 
ORDER BY u.id;

SELECT '' as '';
SELECT '3. ESTADÍSTICAS:' as '';
SELECT 
    (SELECT COUNT(*) FROM roles) as total_roles,
    (SELECT COUNT(*) FROM roles WHERE active = TRUE) as roles_activos,
    (SELECT COUNT(*) FROM users) as total_usuarios,
    (SELECT COUNT(*) FROM users WHERE role_id IS NOT NULL) as usuarios_con_rol,
    (SELECT COUNT(*) FROM units) as unidades_medida;

SELECT '' as '';
SELECT '============================================' as '';
SELECT '✓ SCRIPT COMPLETADO SIN ERRORES' as 'ESTADO';
SELECT '============================================' as '';
SELECT '' as '';
SELECT 'NOTAS IMPORTANTES:' as '';
SELECT '- Este script complementa scriptDB.txt' as '';
SELECT '- Ejecutar scriptDB.txt primero si no se ha hecho' as '';
SELECT '- La tabla "units" es opcional y complementaria' as '';
SELECT '- Todos los usuarios ahora tienen rol asignado' as '';
SELECT '' as '';

