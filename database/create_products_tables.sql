-- Script SQL para tablas de Productos e Inventario
-- Sistema POS - Módulo de Inventario

-- Tabla de Categorías
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id INT DEFAULT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de Unidades de Medida
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

-- Tabla de Productos
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

-- Tabla de Movimientos de Productos
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

-- Insertar categorías por defecto
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

-- Insertar unidades de medida por defecto
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

-- Insertar productos de ejemplo (opcional)
INSERT INTO products (sku, name, description, category_id, unit_id, price, cost, stock_quantity, min_stock, max_stock, tax_rate, status, created_by) VALUES
('PROD-001', 'Laptop Dell Inspiron 15', 'Laptop Dell Inspiron 15 - Intel Core i5, 8GB RAM, 256GB SSD', 2, 1, 799.99, 650.00, 5, 2, 20, 16.00, 'active', 1),
('PROD-002', 'Mouse Inalámbrico Logitech', 'Mouse inalámbrico Logitech M185 - Sensor óptico, batería incluida', 2, 1, 24.99, 15.00, 15, 5, 50, 16.00, 'active', 1),
('PROD-003', 'Cuaderno Universitario 100 hojas', 'Cuaderno universitario de 100 hojas, tapa dura', 6, 1, 3.50, 2.00, 50, 20, 200, 0.00, 'active', 1),
('PROD-004', 'Agua Mineral 500ml', 'Agua mineral natural embotellada 500ml', 3, 5, 0.75, 0.40, 200, 50, 500, 0.00, 'active', 1),
('PROD-005', 'Teclado Mecánico RGB', 'Teclado mecánico retroiluminado RGB, switches azules', 2, 1, 89.99, 55.00, 8, 3, 30, 16.00, 'active', 1)
ON DUPLICATE KEY UPDATE name = VALUES(name);
