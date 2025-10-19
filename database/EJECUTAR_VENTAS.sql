-- =====================================================
-- MÓDULO DE VENTAS - SCRIPT COMPLETO
-- Copiar y pegar TODO en tu cliente MySQL
-- =====================================================

USE pos_system;

-- =====================================================
-- PASO 1: DESACTIVAR VERIFICACIÓN DE FOREIGN KEYS
-- =====================================================
SET FOREIGN_KEY_CHECKS = 0;

-- =====================================================
-- PASO 2: ELIMINAR TABLAS (sin importar el orden)
-- =====================================================
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS sale_payments;
DROP TABLE IF EXISTS inventory_movements;

-- =====================================================
-- PASO 3: REACTIVAR VERIFICACIÓN DE FOREIGN KEYS
-- =====================================================
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- PASO 3: REACTIVAR VERIFICACIÓN DE FOREIGN KEYS
-- =====================================================
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- PASO 4: CREAR TABLA DE CLIENTES
-- =====================================================

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
    INDEX idx_document (document_number),
    INDEX idx_status (status),
    FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- PASO 5: CREAR TABLA PRINCIPAL DE VENTAS
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- PASO 6: CREAR DETALLE DE ITEMS DE VENTA
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- PASO 7: CREAR TABLA DE PAGOS
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- PASO 8: CREAR TABLA DE MOVIMIENTOS DE INVENTARIO
-- =====================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- PASO 9: INSERTAR CLIENTE GENÉRICO POR DEFECTO
-- =====================================================
INSERT INTO customers (code, name, document_type, document_number, customer_type, status)
VALUES ('GENERIC', 'Cliente Genérico', 'other', '00000000', 'retail', 'active')
ON DUPLICATE KEY UPDATE name = 'Cliente Genérico';

-- =====================================================
-- PASO 10: CREAR VISTA DE VENTAS COMPLETA
-- =====================================================
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

-- =====================================================
-- PASO 11: VERIFICACIÓN FINAL
-- =====================================================
SELECT '✅ Tabla customers' as tabla, COUNT(*) as registros FROM customers
UNION ALL
SELECT '✅ Tabla sales', COUNT(*) FROM sales
UNION ALL
SELECT '✅ Tabla sale_items', COUNT(*) FROM sale_items
UNION ALL
SELECT '✅ Tabla sale_payments', COUNT(*) FROM sale_payments
UNION ALL
SELECT '✅ Tabla inventory_movements', COUNT(*) FROM inventory_movements;

-- =====================================================
-- ¡LISTO! Tablas creadas correctamente
-- =====================================================
