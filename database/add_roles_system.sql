-- =============================================================================
-- SCRIPT PARA AGREGAR SISTEMA DE ROLES AL POS
-- =============================================================================

USE pos_system;

-- =============================================================================
-- TABLA: roles
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

-- =============================================================================
-- INSERTAR ROLES POR DEFECTO
-- =============================================================================

-- Super Admin
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(1, 'Super Admin', 'super_admin', 'Acceso completo al sistema, puede gestionar todo', '["*"]', TRUE, TRUE);

-- Administrador
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(2, 'Administrador', 'admin', 'Administrador del sistema con acceso a la mayoría de funciones', 
'["users.view", "users.create", "users.edit", "users.delete", "roles.view", "roles.create", "roles.edit", "system.config", "system.backup", "system.reports", "inventory.view", "inventory.edit", "inventory.reports", "sales.view", "sales.create", "sales.reports", "dashboard.view"]', 
TRUE, TRUE);

-- Gerente
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(3, 'Gerente', 'manager', 'Gerente de tienda con acceso a reportes y supervisión', 
'["users.view", "inventory.view", "inventory.reports", "sales.view", "sales.create", "sales.reports", "dashboard.view", "dashboard.stats"]', 
TRUE, TRUE);

-- Empleado
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(4, 'Empleado', 'employee', 'Empleado con acceso básico para ventas', 
'["sales.view", "sales.create", "inventory.view", "dashboard.view"]', 
TRUE, TRUE);

-- Cajero
INSERT IGNORE INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(5, 'Cajero', 'cashier', 'Cajero con acceso solo a ventas y caja', 
'["sales.create", "sales.view_own", "cash.register"]', 
TRUE, TRUE);

-- =============================================================================
-- MODIFICAR TABLA USERS PARA AGREGAR ROLE_ID
-- =============================================================================

-- Agregar columna role_id
ALTER TABLE users ADD COLUMN role_id INT DEFAULT NULL AFTER user_type;
ALTER TABLE users ADD INDEX idx_role_id (role_id);
ALTER TABLE users ADD FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL;

-- =============================================================================
-- MIGRAR DATOS EXISTENTES
-- =============================================================================

-- Migrar usuarios existentes a roles
UPDATE users SET role_id = 2 WHERE user_type = 'admin';     -- Administrador
UPDATE users SET role_id = 3 WHERE user_type = 'supervisor'; -- Gerente
UPDATE users SET role_id = 5 WHERE user_type = 'cashier';   -- Cajero
UPDATE users SET role_id = 4 WHERE user_type = 'user';      -- Empleado

-- Asignar rol por defecto a usuarios sin rol
UPDATE users SET role_id = 4 WHERE role_id IS NULL;

-- =============================================================================
-- VERIFICACIONES
-- =============================================================================

SELECT 'ROLES CREADOS:' as info;
SELECT id, name, code, active, system_role FROM roles ORDER BY id;

SELECT 'USUARIOS CON ROLES:' as info;
SELECT u.username, u.full_name, u.user_type, r.name as role_name, r.code as role_code 
FROM users u 
LEFT JOIN roles r ON u.role_id = r.id 
ORDER BY u.id;

SELECT 'MIGRACION COMPLETADA!' as 'RESULTADO';
