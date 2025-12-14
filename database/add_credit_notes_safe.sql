-- Migracion segura: notas de credito sin tocar productos
-- Objetivo: agregar tablas y relaciones para notas de credito sin alterar la tabla products ni sus datos.
-- Probado para MySQL 8.0.x. Ejecutar con un usuario con permisos ALTER/CREATE/FOREIGN KEY.

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Crea una rutina temporal para ejecutar alteraciones solo cuando hagan falta
DELIMITER $$
CREATE PROCEDURE apply_credit_notes_migration()
BEGIN
    DECLARE col_exists INT DEFAULT 0;
    DECLARE fk_exists INT DEFAULT 0;
    DECLARE needs_status ENUM('Y','N') DEFAULT 'N';
    DECLARE needs_movement ENUM('Y','N') DEFAULT 'N';

    -- Tabla principal de notas de credito (idempotente)
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

    -- Detalle de items de notas de credito (referencia productos, pero no modifica la tabla products)
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

    -- Agregar credit_note_id en sales si falta
    SELECT COUNT(*) INTO col_exists
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'sales' AND COLUMN_NAME = 'credit_note_id';

    IF col_exists = 0 THEN
        ALTER TABLE sales ADD COLUMN credit_note_id INT NULL AFTER cancellation_reason;
    END IF;

    -- Ajustar ENUM de sales.status para incluir 'refunded' y 'credited'
    SELECT CASE WHEN COLUMN_TYPE LIKE '%credited%' AND COLUMN_TYPE LIKE '%refunded%' THEN 'N' ELSE 'Y' END INTO needs_status
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'sales' AND COLUMN_NAME = 'status';

    IF needs_status = 'Y' THEN
        ALTER TABLE sales MODIFY COLUMN status ENUM('completed','cancelled','pending','refunded','credited') DEFAULT 'completed';
    END IF;

    -- FK de sales hacia credit_notes (idempotente)
    SELECT COUNT(*) INTO fk_exists
    FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
    WHERE tc.CONSTRAINT_SCHEMA = DATABASE()
      AND tc.TABLE_NAME = 'sales'
      AND tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
      AND tc.CONSTRAINT_NAME = 'fk_sale_credit_note';

    IF fk_exists = 0 THEN
        ALTER TABLE sales ADD CONSTRAINT fk_sale_credit_note FOREIGN KEY (credit_note_id) REFERENCES credit_notes(id) ON DELETE SET NULL;
    END IF;

    -- Ampliar inventory_movements.movement_type para incluir 'credit_note'
    SELECT CASE WHEN COLUMN_TYPE LIKE '%credit_note%' THEN 'N' ELSE 'Y' END INTO needs_movement
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'inventory_movements' AND COLUMN_NAME = 'movement_type';

    IF needs_movement = 'Y' THEN
        ALTER TABLE inventory_movements MODIFY COLUMN movement_type ENUM('sale','purchase','adjustment','return','transfer','credit_note') NOT NULL;
    END IF;
END$$
DELIMITER ;

CALL apply_credit_notes_migration();
DROP PROCEDURE IF EXISTS apply_credit_notes_migration;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
