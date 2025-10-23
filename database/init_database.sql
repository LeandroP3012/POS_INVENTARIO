-- =============================================================================
-- SCRIPT DE INICIALIZACIÓN COMPLETA DEL SISTEMA POS
-- =============================================================================
-- Este script unifica todas las configuraciones de base de datos:
-- - Actualización de tipos de usuario (compatible con estructura existente)
-- - Sistema de roles y permisos
-- - Sistema de sesiones de usuario (ya existe en scriptDB.txt)
-- - Tablas complementarias de inventario (units)
-- =============================================================================
-- IMPORTANTE: Este script está diseñado para trabajar con la estructura
-- definida en scriptDB.txt. Solo agrega/actualiza lo necesario.
-- =============================================================================
-- Fecha: 2025-10-10
-- Versión: 2.0 (Compatible con scriptDB.txt)
-- =============================================================================

USE pos_system;

-- =============================================================================
-- SECCIÓN 1: ACTUALIZACIÓN DE TIPOS DE USUARIO
-- =============================================================================
-- Agregar nuevos tipos de usuario al enum existente
-- NOTA: scriptDB.txt tiene: 'admin', 'supervisor', 'cashier', 'user'
-- Agregamos: 'manager', 'employee' para compatibilidad completa
-- =============================================================================

ALTER TABLE users MODIFY COLUMN user_type 
    ENUM('admin', 'supervisor', 'manager', 'employee', 'cashier', 'user') 
    DEFAULT 'user';

-- =============================================================================
-- SECCIÓN 2: SISTEMA DE ROLES Y PERMISOS
-- =============================================================================
-- Tabla de roles con permisos personalizables
-- COMPATIBLE con la estructura de users existente en scriptDB.txt
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

-- -----------------------------------------------------------------------------
-- Insertar roles predefinidos del sistema
-- -----------------------------------------------------------------------------

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

-- -----------------------------------------------------------------------------
-- Agregar columna role_id a la tabla users (si no existe)
-- -----------------------------------------------------------------------------

-- Verificar si la columna ya existe antes de agregarla
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

-- -----------------------------------------------------------------------------
-- Migrar datos existentes a roles
-- -----------------------------------------------------------------------------

UPDATE users SET role_id = 2 WHERE user_type = 'admin' AND role_id IS NULL;      -- Administrador
UPDATE users SET role_id = 3 WHERE user_type = 'supervisor' AND role_id IS NULL; -- Gerente
UPDATE users SET role_id = 5 WHERE user_type = 'cashier' AND role_id IS NULL;    -- Cajero
UPDATE users SET role_id = 4 WHERE user_type = 'user' AND role_id IS NULL;       -- Empleado
UPDATE users SET role_id = 3 WHERE user_type = 'manager' AND role_id IS NULL;    -- Gerente
UPDATE users SET role_id = 4 WHERE user_type = 'employee' AND role_id IS NULL;   -- Empleado

-- Asignar rol por defecto a usuarios sin rol
UPDATE users SET role_id = 4 WHERE role_id IS NULL;

-- =============================================================================
-- SECCIÓN 3: SISTEMA DE SESIONES DE USUARIO
-- =============================================================================
-- Tabla para controlar sesiones activas
-- =============================================================================

CREATE TABLE IF NOT EXISTS user_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    user_type VARCHAR(20) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL,
    login_method VARCHAR(20) DEFAULT 'manual',
    logout_reason VARCHAR(50) NULL,
    is_active BOOLEAN DEFAULT TRUE,
    permissions JSON,
    expires_at TIMESTAMP NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_is_active (is_active),
    INDEX idx_expires_at (expires_at),
    INDEX idx_login_time (login_time),
    INDEX idx_last_activity (last_activity),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Sesiones de usuarios activas';

-- =============================================================================
-- SECCIÓN 4: MÓDULO DE INVENTARIO - CATEGORÍAS Y UNIDADES
-- =============================================================================
-- Tablas para gestión de productos e inventario
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla de Categorías
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INT DEFAULT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_status (status),
    INDEX idx_parent (parent_id),
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Tabla de Unidades de Medida
-- -----------------------------------------------------------------------------

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- SECCIÓN 5: MÓDULO DE INVENTARIO - PRODUCTOS Y MOVIMIENTOS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabla de Productos
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    unit_id INT NOT NULL DEFAULT 1,
    barcode VARCHAR(100) DEFAULT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    stock_quantity DECIMAL(10, 2) NOT NULL DEFAULT 0,
    min_stock DECIMAL(10, 2) NOT NULL DEFAULT 0,
    max_stock DECIMAL(10, 2) NOT NULL DEFAULT 0,
    tax_rate DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    image_path VARCHAR(255) DEFAULT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_sku (sku),
    INDEX idx_name (name),
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_stock (stock_quantity),
    INDEX idx_barcode (barcode),
    
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (unit_id) REFERENCES units(id) ON DELETE RESTRICT,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Tabla de Movimientos de Productos
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS product_movements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    movement_type ENUM('purchase', 'sale', 'adjustment', 'return', 'transfer') NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    previous_stock DECIMAL(10, 2) NOT NULL,
    new_stock DECIMAL(10, 2) NOT NULL,
    reference_id INT DEFAULT NULL COMMENT 'ID de referencia (venta, compra, etc)',
    reference_type VARCHAR(50) DEFAULT NULL COMMENT 'Tipo de referencia',
    notes TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_product (product_id),
    INDEX idx_type (movement_type),
    INDEX idx_date (created_at),
    INDEX idx_reference (reference_type, reference_id),
    
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================================
-- SECCIÓN 6: DATOS INICIALES - CATEGORÍAS
-- =============================================================================

INSERT INTO categories (name, description, status) VALUES
('General', 'Categoría general para productos sin clasificación específica', 'active'),
('Electrónica', 'Productos electrónicos y tecnología', 'active'),
('Alimentos', 'Productos alimenticios y bebidas', 'active'),
('Ropa', 'Ropa y accesorios', 'active'),
('Hogar', 'Artículos para el hogar', 'active'),
('Oficina', 'Artículos de oficina y papelería', 'active'),
('Salud', 'Productos de salud y cuidado personal', 'active'),
('Deportes', 'Artículos deportivos y fitness', 'active')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- =============================================================================
-- SECCIÓN 7: DATOS INICIALES - UNIDADES DE MEDIDA
-- =============================================================================

INSERT INTO units (name, symbol, type, status) VALUES
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

-- =============================================================================
-- SECCIÓN 8: DATOS DE EJEMPLO - PRODUCTOS (OPCIONAL)
-- =============================================================================
-- Puedes comentar esta sección si no deseas productos de ejemplo
-- =============================================================================

INSERT INTO products (sku, name, description, category_id, unit_id, price, cost, stock_quantity, min_stock, max_stock, tax_rate, status, created_by) VALUES
('PROD-001', 'Laptop Dell Inspiron 15', 'Laptop Dell Inspiron 15 - Intel Core i5, 8GB RAM, 256GB SSD', 2, 1, 799.99, 650.00, 5, 2, 20, 16.00, 'active', 1),
('PROD-002', 'Mouse Inalámbrico Logitech', 'Mouse inalámbrico Logitech M185 - Sensor óptico, batería incluida', 2, 1, 24.99, 15.00, 15, 5, 50, 16.00, 'active', 1),
('PROD-003', 'Cuaderno Universitario 100 hojas', 'Cuaderno universitario de 100 hojas, tapa dura', 6, 1, 3.50, 2.00, 50, 20, 200, 0.00, 'active', 1),
('PROD-004', 'Agua Mineral 500ml', 'Agua mineral natural embotellada 500ml', 3, 5, 0.75, 0.40, 200, 50, 500, 0.00, 'active', 1),
('PROD-005', 'Teclado Mecánico RGB', 'Teclado mecánico retroiluminado RGB, switches azules', 2, 1, 89.99, 55.00, 8, 3, 30, 16.00, 'active', 1)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- =============================================================================
-- SECCIÓN 9: VERIFICACIONES FINALES
-- =============================================================================
-- Consultas para verificar que todo se haya configurado correctamente
-- =============================================================================

SELECT '============================================' as '';
SELECT 'VERIFICACIÓN DE INSTALACIÓN COMPLETADA' as 'RESULTADO';
SELECT '============================================' as '';

SELECT '' as '';
SELECT '1. ROLES CREADOS:' as 'INFORMACIÓN';
SELECT id, name, code, active, system_role 
FROM roles 
ORDER BY id;

SELECT '' as '';
SELECT '2. USUARIOS CON ROLES ASIGNADOS:' as 'INFORMACIÓN';
SELECT u.username, u.full_name, u.user_type, r.name as role_name, r.code as role_code 
FROM users u 
LEFT JOIN roles r ON u.role_id = r.id 
ORDER BY u.id;

SELECT '' as '';
SELECT '3. CATEGORÍAS DE PRODUCTOS:' as 'INFORMACIÓN';
SELECT id, name, status 
FROM categories 
ORDER BY id;

SELECT '' as '';
SELECT '4. UNIDADES DE MEDIDA:' as 'INFORMACIÓN';
SELECT id, name, symbol, type, status 
FROM units 
ORDER BY id;

SELECT '' as '';
SELECT '5. PRODUCTOS REGISTRADOS:' as 'INFORMACIÓN';
SELECT COUNT(*) as total_productos 
FROM products;

SELECT '' as '';
SELECT '============================================' as '';
SELECT '✓ INICIALIZACIÓN COMPLETADA EXITOSAMENTE' as 'ESTADO';
SELECT '============================================' as '';
