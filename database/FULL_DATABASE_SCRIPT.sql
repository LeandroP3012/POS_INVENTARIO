-- =============================================================================
-- SCRIPT COMPLETO DE BASE DE DATOS - SISTEMA POS
-- =============================================================================
-- Versión: 2.0
-- Fecha: 19 de Octubre 2025
-- Descripción: Script completo con todas las tablas y configuraciones
-- Incluye: Sistema base + Roles + Ventas + Sesiones
-- =============================================================================

-- =============================================================================
-- CREAR BASE DE DATOS
-- =============================================================================
CREATE DATABASE IF NOT EXISTS pos_system 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE pos_system;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================================
-- TABLA: system_config
-- Configuraciones del sistema
-- =============================================================================
DROP TABLE IF EXISTS system_config;
CREATE TABLE system_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT,
    config_type ENUM('string', 'integer', 'float', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE COMMENT 'Si usuarios normales pueden verlo',
    is_editable BOOLEAN DEFAULT TRUE COMMENT 'Si se puede modificar desde la UI',
    category VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_config_key (config_key),
    INDEX idx_category (category),
    INDEX idx_config_type (config_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Configuraciones del sistema';

-- =============================================================================
-- TABLA: users
-- Usuarios del sistema
-- =============================================================================
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    user_type ENUM('admin', 'supervisor', 'cashier', 'user') DEFAULT 'user',
    role_id INT DEFAULT NULL COMMENT 'Sistema de roles',
    active BOOLEAN DEFAULT TRUE,
    avatar_path VARCHAR(255),
    preferences JSON COMMENT 'Preferencias personales del usuario',
    permissions JSON COMMENT 'Permisos específicos del usuario',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    failed_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    created_by INT,
    notes TEXT COMMENT 'Notas administrativas',
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_user_type (user_type),
    INDEX idx_role_id (role_id),
    INDEX idx_active (active),
    INDEX idx_last_login (last_login)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Usuarios del sistema';

-- =============================================================================
-- TABLA: roles
-- Sistema de roles y permisos
-- =============================================================================
DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
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
    INDEX idx_system_role (system_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Roles del sistema con permisos personalizables';

-- =============================================================================
-- TABLA: user_sessions
-- Sesiones activas de usuarios
-- =============================================================================
DROP TABLE IF EXISTS user_sessions;
CREATE TABLE user_sessions (
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
-- TABLA: categories
-- Categorías de productos
-- =============================================================================
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INT NULL COMMENT 'Para categorias anidadas',
    color VARCHAR(7) DEFAULT '#3498db',
    icon VARCHAR(50) DEFAULT 'folder',
    active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    
    INDEX idx_name (name),
    INDEX idx_active (active),
    INDEX idx_parent_id (parent_id),
    INDEX idx_sort_order (sort_order),
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Categorias de productos';

-- =============================================================================
-- TABLA: suppliers
-- Proveedores
-- =============================================================================
DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50) DEFAULT 'Peru',
    tax_id VARCHAR(20) COMMENT 'RUC o documento tributario',
    payment_terms VARCHAR(100) COMMENT 'Condiciones de pago',
    credit_limit DECIMAL(12,2) DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    
    INDEX idx_code (code),
    INDEX idx_name (name),
    INDEX idx_active (active),
    INDEX idx_tax_id (tax_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Proveedores';

-- =============================================================================
-- TABLA: products
-- Productos del inventario
-- =============================================================================
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    barcode VARCHAR(100) UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT,
    supplier_id INT,
    brand VARCHAR(100),
    model VARCHAR(100),
    
    -- Precios y costos
    cost_price DECIMAL(12,4) DEFAULT 0 COMMENT 'Precio de costo',
    sale_price DECIMAL(12,4) NOT NULL COMMENT 'Precio de venta',
    wholesale_price DECIMAL(12,4) COMMENT 'Precio mayorista',
    min_price DECIMAL(12,4) COMMENT 'Precio minimo de venta',
    
    -- Inventario
    current_stock INT DEFAULT 0,
    min_stock INT DEFAULT 0 COMMENT 'Stock minimo (alerta)',
    max_stock INT DEFAULT 0 COMMENT 'Stock maximo',
    reorder_point INT DEFAULT 0 COMMENT 'Punto de reorden',
    
    -- Configuraciones
    unit VARCHAR(20) DEFAULT 'unidad' COMMENT 'Unidad de medida',
    weight DECIMAL(8,3) COMMENT 'Peso en kg',
    dimensions VARCHAR(50) COMMENT 'Dimensiones',
    tax_rate DECIMAL(5,2) DEFAULT 18.00 COMMENT 'Tasa de impuesto',
    
    -- Estados
    active BOOLEAN DEFAULT TRUE,
    is_service BOOLEAN DEFAULT FALSE COMMENT 'Es un servicio (no maneja stock)',
    track_stock BOOLEAN DEFAULT TRUE COMMENT 'Controlar inventario',
    allow_negative_stock BOOLEAN DEFAULT FALSE,
    
    -- Metadatos
    image_path VARCHAR(255),
    tags JSON COMMENT 'Etiquetas para busqueda',
    attributes JSON COMMENT 'Atributos personalizados',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    
    INDEX idx_code (code),
    INDEX idx_barcode (barcode),
    INDEX idx_name (name),
    INDEX idx_category (category_id),
    INDEX idx_supplier (supplier_id),
    INDEX idx_active (active),
    INDEX idx_current_stock (current_stock),
    INDEX idx_sale_price (sale_price),
    
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Productos del inventario';

-- =============================================================================
-- TABLA: customers
-- Clientes del sistema
-- =============================================================================
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    document_type ENUM('dni', 'ruc', 'passport', 'other') DEFAULT 'dni',
    document_number VARCHAR(20) NULL,
    email VARCHAR(100) NULL,
    phone VARCHAR(20) NULL,
    address TEXT NULL,
    city VARCHAR(50) NULL,
    country VARCHAR(50) DEFAULT 'Perú',
    tax_id VARCHAR(20) NULL COMMENT 'RUC para facturas',
    customer_type ENUM('retail', 'wholesale', 'corporate') DEFAULT 'retail',
    credit_limit DECIMAL(10,2) DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT NULL,
    
    INDEX idx_code (code),
    INDEX idx_document (document_number),
    INDEX idx_status (status),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Clientes del sistema';

-- =============================================================================
-- TABLA: sales
-- Ventas realizadas
-- =============================================================================
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_number VARCHAR(50) UNIQUE NOT NULL COMMENT 'VTA-2025-00001',
    user_id INT NOT NULL COMMENT 'Cajero',
    customer_id INT NULL COMMENT 'Cliente (NULL = genérico)',
    
    -- Montos
    subtotal DECIMAL(10,2) NOT NULL,
    tax_rate DECIMAL(5,2) DEFAULT 18.00,
    tax_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    
    -- Pago
    payment_method ENUM('cash', 'card', 'transfer', 'multiple') NOT NULL DEFAULT 'cash',
    paid_amount DECIMAL(10,2) NOT NULL,
    change_amount DECIMAL(10,2) DEFAULT 0,
    
    -- Estado
    status ENUM('completed', 'cancelled', 'pending', 'refunded') DEFAULT 'completed',
    notes TEXT NULL,
    
    -- Fechas
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    cancelled_at TIMESTAMP NULL,
    cancelled_by INT NULL,
    cancellation_reason TEXT NULL,
    
    INDEX idx_sale_number (sale_number),
    INDEX idx_sale_date (sale_date),
    INDEX idx_user (user_id),
    INDEX idx_customer (customer_id),
    INDEX idx_status (status),
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
    FOREIGN KEY (cancelled_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Ventas realizadas';

-- =============================================================================
-- TABLA: sale_items
-- Detalle de items de venta
-- =============================================================================
DROP TABLE IF EXISTS sale_items;
CREATE TABLE sale_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    product_id INT NOT NULL,
    
    -- Info del producto
    product_sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    
    -- Cantidades y precios
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    subtotal DECIMAL(10,2) NOT NULL,
    
    -- Impuestos
    tax_rate DECIMAL(5,2) DEFAULT 18.00,
    tax_amount DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_sale (sale_id),
    INDEX idx_product (product_id),
    
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Detalle de items de venta';

-- =============================================================================
-- TABLA: sale_payments
-- Pagos de ventas
-- =============================================================================
DROP TABLE IF EXISTS sale_payments;
CREATE TABLE sale_payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT NOT NULL,
    payment_method ENUM('cash', 'card', 'transfer', 'other') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    
    -- Info adicional
    card_type VARCHAR(50) NULL,
    card_last_digits VARCHAR(4) NULL,
    transaction_reference VARCHAR(100) NULL,
    bank_name VARCHAR(100) NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_sale (sale_id),
    INDEX idx_method (payment_method),
    
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Pagos de ventas';

-- =============================================================================
-- TABLA: inventory_movements
-- Movimientos de inventario
-- =============================================================================
DROP TABLE IF EXISTS inventory_movements;
CREATE TABLE inventory_movements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    movement_type ENUM('sale', 'purchase', 'adjustment', 'return', 'transfer') NOT NULL,
    quantity DECIMAL(10,2) NOT NULL COMMENT 'Positivo=entrada, Negativo=salida',
    previous_stock DECIMAL(10,2) NOT NULL,
    new_stock DECIMAL(10,2) NOT NULL,
    
    -- Referencias
    reference_type ENUM('sale', 'purchase', 'manual', 'other') NULL,
    reference_id INT NULL,
    
    -- Info adicional
    user_id INT NOT NULL,
    notes TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_product (product_id),
    INDEX idx_type (movement_type),
    INDEX idx_reference (reference_type, reference_id),
    INDEX idx_date (created_at),
    
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Movimientos de inventario';

-- =============================================================================
-- TABLA: activity_logs
-- Logs de actividad del sistema
-- =============================================================================
DROP TABLE IF EXISTS activity_logs;
CREATE TABLE activity_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    activity_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    description TEXT,
    old_values JSON COMMENT 'Valores anteriores del registro',
    new_values JSON COMMENT 'Valores nuevos del registro',
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_activity_type (activity_type),
    INDEX idx_table_name (table_name),
    INDEX idx_record_id (record_id),
    INDEX idx_created_at (created_at),
    INDEX idx_session_id (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Logs de actividad del sistema';

-- =============================================================================
-- AGREGAR FOREIGN KEYS DE USERS (después de crear roles)
-- =============================================================================
ALTER TABLE users ADD FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL;
ALTER TABLE users ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE categories ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE suppliers ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE products ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE roles ADD FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE customers ADD FOREIGN KEY (created_by) REFERENCES users(id);
ALTER TABLE activity_logs ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;

SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- VISTA: sales_detail
-- Vista completa de ventas con información relacionada
-- =============================================================================
CREATE OR REPLACE VIEW sales_detail AS
SELECT 
    s.id,
    s.sale_number,
    s.sale_date,
    s.total_amount,
    s.status,
    s.payment_method,
    u.username as cashier_username,
    u.full_name as cashier_name,
    COALESCE(c.name, 'Cliente Genérico') as customer_name,
    COALESCE(c.document_number, '00000000') as customer_document,
    COUNT(si.id) as items_count,
    SUM(si.quantity) as total_items_qty
FROM sales s
INNER JOIN users u ON s.user_id = u.id
LEFT JOIN customers c ON s.customer_id = c.id
LEFT JOIN sale_items si ON s.id = si.sale_id
GROUP BY s.id;

-- =============================================================================
-- DATOS INICIALES - ROLES
-- =============================================================================
INSERT INTO roles (id, name, code, description, permissions, system_role, active) VALUES
(1, 'Super Admin', 'super_admin', 'Acceso completo al sistema', '["*"]', TRUE, TRUE),
(2, 'Administrador', 'admin', 'Administrador del sistema con acceso a mayoría de funciones', 
 '["users.view", "users.create", "users.edit", "users.delete", "roles.view", "roles.create", "roles.edit", "system.config", "system.backup", "system.reports", "inventory.view", "inventory.edit", "inventory.reports", "sales.view", "sales.create", "sales.reports", "dashboard.view"]', 
 TRUE, TRUE),
(3, 'Gerente', 'manager', 'Gerente de tienda con acceso a reportes', 
 '["users.view", "inventory.view", "inventory.reports", "sales.view", "sales.create", "sales.reports", "dashboard.view", "dashboard.stats"]', 
 TRUE, TRUE),
(4, 'Empleado', 'employee', 'Empleado con acceso básico', 
 '["sales.view", "sales.create", "inventory.view", "dashboard.view"]', 
 TRUE, TRUE),
(5, 'Cajero', 'cashier', 'Cajero con acceso solo a ventas', 
 '["sales.create", "sales.view_own", "cash.register"]', 
 TRUE, TRUE);

-- =============================================================================
-- DATOS INICIALES - USUARIOS
-- =============================================================================
-- Usuario administrador (password: 123456)
INSERT INTO users (username, password_hash, email, full_name, user_type, role_id, active, permissions) VALUES
('admin', SHA2('123456', 256), 'admin@sistema-pos.com', 'Administrador del Sistema', 'admin', 2, TRUE, '{"all_modules": true, "super_admin": true}');

-- Usuario cajero (password: 123456)
INSERT INTO users (username, password_hash, email, full_name, user_type, role_id, active, permissions) VALUES
('cajero1', SHA2('123456', 256), 'cajero@sistema-pos.com', 'Cajero Principal', 'cashier', 5, TRUE, '{"ventas": ["ver", "crear"], "productos": ["ver"]}');

-- =============================================================================
-- DATOS INICIALES - CONFIGURACIONES
-- =============================================================================
INSERT INTO system_config (config_key, config_value, config_type, description, is_public, is_editable, category) VALUES
('app_name', 'Sistema POS Avanzado', 'string', 'Nombre de la aplicacion', TRUE, TRUE, 'general'),
('app_version', '2.0.0', 'string', 'Version de la aplicacion', TRUE, FALSE, 'general'),
('company_name', 'Mi Empresa POS', 'string', 'Nombre de la empresa', TRUE, TRUE, 'company'),
('company_address', 'Av. Principal 123, Lima', 'string', 'Direccion de la empresa', TRUE, TRUE, 'company'),
('company_phone', '(01) 234-5678', 'string', 'Telefono de la empresa', TRUE, TRUE, 'company'),
('company_email', 'info@miempresa.com', 'string', 'Email de la empresa', TRUE, TRUE, 'company'),
('currency_code', 'PEN', 'string', 'Codigo de moneda', TRUE, TRUE, 'financial'),
('currency_symbol', 'S/.', 'string', 'Simbolo de moneda', TRUE, TRUE, 'financial'),
('tax_rate', '18', 'float', 'Tasa de impuestos (%)', TRUE, TRUE, 'financial'),
('include_tax', 'true', 'boolean', 'Incluir IGV por defecto', TRUE, TRUE, 'financial'),
('decimal_places', '2', 'integer', 'Decimales para precios', TRUE, TRUE, 'financial'),
('session_timeout', '3600', 'integer', 'Tiempo de sesion en segundos', FALSE, TRUE, 'security'),
('max_login_attempts', '3', 'integer', 'Intentos maximos de login', FALSE, TRUE, 'security'),
('backup_enabled', 'true', 'boolean', 'Backup automatico habilitado', FALSE, TRUE, 'system'),
('next_sale_number', '1', 'integer', 'Proximo numero de venta', FALSE, FALSE, 'sales'),
('receipt_footer', 'Gracias por su compra', 'string', 'Pie de pagina del recibo', TRUE, TRUE, 'sales'),
('system_initialized', 'true', 'boolean', 'Sistema inicializado', FALSE, FALSE, 'system'),
('install_date', NOW(), 'string', 'Fecha de instalacion', FALSE, FALSE, 'system');

-- =============================================================================
-- DATOS INICIALES - CATEGORÍAS
-- =============================================================================
INSERT INTO categories (name, description, color, icon, created_by) VALUES
('BEBIDAS', 'Bebidas y refrescos', '#3498db', 'glass-water', 1),
('LACTEOS', 'Productos lacteos', '#e67e22', 'cheese', 1),
('PANADERIA', 'Pan y productos de panaderia', '#f39c12', 'bread-slice', 1),
('ABARROTES', 'Productos de abarrotes', '#2ecc71', 'shopping-bag', 1),
('LIMPIEZA', 'Productos de limpieza', '#9b59b6', 'spray-can', 1),
('SNACKS', 'Aperitivos y golosinas', '#e74c3c', 'cookie', 1),
('CONSERVAS', 'Productos enlatados', '#34495e', 'can-food', 1),
('SERVICIOS', 'Servicios diversos', '#95a5a6', 'handshake', 1);

-- =============================================================================
-- DATOS INICIALES - PROVEEDOR
-- =============================================================================
INSERT INTO suppliers (code, name, contact_person, phone, email, created_by) VALUES
('PROV001', 'Proveedor General', 'Contacto General', '(01) 000-0000', 'contacto@proveedor.com', 1);

-- =============================================================================
-- DATOS INICIALES - PRODUCTOS
-- =============================================================================
INSERT INTO products (code, barcode, name, description, cost_price, sale_price, current_stock, min_stock, category_id, supplier_id, created_by, is_service, track_stock) VALUES
('P001', '7751271000017', 'Coca Cola 2L', 'Gaseosa Coca Cola 2 litros', 4.50, 6.50, 25, 10, 1, 1, 1, FALSE, TRUE),
('P002', '7751271000024', 'Pan Integral', 'Pan integral artesanal', 2.50, 4.00, 15, 5, 3, 1, 1, FALSE, TRUE),
('P003', '7751271000031', 'Leche Entera 1L', 'Leche entera pasteurizada', 3.50, 5.20, 20, 8, 2, 1, 1, FALSE, TRUE),
('P004', '7751271000048', 'Arroz Superior 1kg', 'Arroz extra superior', 2.20, 3.80, 50, 20, 4, 1, 1, FALSE, TRUE),
('P005', '', 'Servicio de Delivery', 'Servicio de entrega a domicilio', 0.00, 5.00, 0, 0, 8, 1, 1, TRUE, FALSE),
('P006', '7751271000055', 'Aceite Vegetal 1L', 'Aceite vegetal comestible', 8.00, 12.50, 30, 10, 4, 1, 1, FALSE, TRUE),
('P007', '7751271000062', 'Detergente 1kg', 'Detergente en polvo', 5.50, 9.00, 20, 8, 5, 1, 1, FALSE, TRUE);

-- =============================================================================
-- DATOS INICIALES - CLIENTE GENÉRICO
-- =============================================================================
INSERT INTO customers (code, name, document_type, document_number, customer_type, status) VALUES
('GENERIC', 'Cliente Genérico', 'other', '00000000', 'retail', 'active');

-- =============================================================================
-- VERIFICACIÓN FINAL
-- =============================================================================
SELECT '==============================================================================' as '';
SELECT '✅ BASE DE DATOS CREADA EXITOSAMENTE!' as 'RESULTADO';
SELECT '==============================================================================' as '';

SELECT 'TABLAS CREADAS:' as info;
SELECT TABLE_NAME as 'Tabla', TABLE_ROWS as 'Registros' 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'pos_system' 
AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;

SELECT '' as '';
SELECT 'USUARIOS CREADOS:' as info;
SELECT username, full_name, user_type, 
       (SELECT name FROM roles WHERE id = users.role_id) as rol,
       active 
FROM users;

SELECT '' as '';
SELECT 'ROLES DEL SISTEMA:' as info;
SELECT id, name, code, active FROM roles ORDER BY id;

SELECT '' as '';
SELECT 'CONFIGURACIONES:' as info;
SELECT config_key, config_value, category 
FROM system_config 
ORDER BY category, config_key;

SELECT '' as '';
SELECT 'CATEGORÍAS:' as info;
SELECT name, color, icon FROM categories;

SELECT '' as '';
SELECT 'PRODUCTOS:' as info;
SELECT code, name, sale_price, current_stock FROM products;

SELECT '' as '';
SELECT 'CLIENTES:' as info;
SELECT code, name, document_number FROM customers;

SELECT '' as '';
SELECT '==============================================================================' as '';
SELECT '📋 INFORMACIÓN DE ACCESO' as '';
SELECT '==============================================================================' as '';
SELECT 'Usuario Admin: admin | Contraseña: 123456' as 'Credenciales';
SELECT 'Usuario Cajero: cajero1 | Contraseña: 123456' as 'Credenciales';
SELECT '' as '';
SELECT '📊 RESUMEN' as '';
SELECT '==============================================================================' as '';
SELECT 'Total de Tablas: 16' as 'Estadísticas';
SELECT 'Total de Vistas: 1' as 'Estadísticas';
SELECT 'Usuarios creados: 2' as 'Estadísticas';
SELECT 'Roles del sistema: 5' as 'Estadísticas';
SELECT 'Productos de ejemplo: 7' as 'Estadísticas';
SELECT 'Configuraciones: 18' as 'Estadísticas';
SELECT '' as '';
SELECT '✅ Script ejecutado correctamente!' as 'FINAL';
SELECT '==============================================================================' as '';
