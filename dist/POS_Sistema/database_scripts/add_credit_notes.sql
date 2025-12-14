-- Migración: tablas de notas de crédito y ajustes de ventas/inventario
-- Fecha: 2025-12-13

-- Crear tabla principal de notas de crédito
CREATE TABLE IF NOT EXISTS credit_notes (
    id INT NOT NULL AUTO_INCREMENT,
    credit_note_number VARCHAR(50) NOT NULL,
    sale_id INT NOT NULL,
    issued_by INT NOT NULL,
    reason TEXT,
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status ENUM('issued','voided') NOT NULL DEFAULT 'issued',
    inventory_restored TINYINT(1) NOT NULL DEFAULT 0,
    inventory_restored_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY idx_credit_note_number (credit_note_number),
    KEY idx_sale_id (sale_id),
    KEY idx_status (status),
    CONSTRAINT fk_credit_note_sale FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    CONSTRAINT fk_credit_note_user FOREIGN KEY (issued_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Detalle de items de la nota de crédito
CREATE TABLE IF NOT EXISTS credit_note_items (
    id INT NOT NULL AUTO_INCREMENT,
    credit_note_id INT NOT NULL,
    sale_item_id INT NULL,
    product_id INT NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0.00,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    subtotal DECIMAL(10,2) NOT NULL,
    tax_rate DECIMAL(5,2) DEFAULT 18.00,
    tax_amount DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_credit_note (credit_note_id),
    KEY idx_product (product_id),
    CONSTRAINT fk_credit_note_item_note FOREIGN KEY (credit_note_id) REFERENCES credit_notes(id) ON DELETE CASCADE,
    CONSTRAINT fk_credit_note_item_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_credit_note_item_sale_item FOREIGN KEY (sale_item_id) REFERENCES sale_items(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ampliar estados de ventas y referencia a nota de crédito
ALTER TABLE sales
    ADD COLUMN IF NOT EXISTS credit_note_id INT NULL AFTER cancellation_reason,
    MODIFY COLUMN status ENUM('completed','cancelled','pending','refunded','credited') DEFAULT 'completed',
    ADD CONSTRAINT fk_sale_credit_note FOREIGN KEY (credit_note_id) REFERENCES credit_notes(id) ON DELETE SET NULL;

-- Ajustar tipos de movimiento de inventario para soportar notas de crédito
ALTER TABLE inventory_movements
    MODIFY COLUMN movement_type ENUM('sale','purchase','adjustment','return','transfer','credit_note') NOT NULL;
