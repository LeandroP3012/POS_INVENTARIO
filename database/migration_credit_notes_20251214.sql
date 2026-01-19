-- Migracion de mejoras de notas de credito.
-- Este script agrega tablas y columnas necesarias sin modificar datos existentes (productos incluidos).

USE `pos_system`;

-- 1) Tabla principal de notas de credito
CREATE TABLE IF NOT EXISTS `credit_notes` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `credit_note_number` VARCHAR(50) NOT NULL,
    `sale_id` INT NOT NULL,
    `issued_by` INT NOT NULL,
    `reason` TEXT,
    `subtotal` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `tax_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `total_amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `status` ENUM('issued','voided') NOT NULL DEFAULT 'issued',
    `inventory_restored` TINYINT(1) NOT NULL DEFAULT 0,
    `inventory_restored_at` TIMESTAMP NULL DEFAULT NULL,
    `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_credit_note_number` (`credit_note_number`),
    KEY `idx_sale_id` (`sale_id`),
    KEY `idx_status` (`status`),
    CONSTRAINT `fk_credit_note_sale` FOREIGN KEY (`sale_id`) REFERENCES `sales`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_credit_note_user` FOREIGN KEY (`issued_by`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2) Detalle de items de la nota de credito
CREATE TABLE IF NOT EXISTS `credit_note_items` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `credit_note_id` INT NOT NULL,
    `sale_item_id` INT NULL,
    `product_id` INT NOT NULL,
    `product_sku` VARCHAR(50) NOT NULL,
    `product_name` VARCHAR(200) NOT NULL,
    `quantity` DECIMAL(10,2) NOT NULL,
    `unit_price` DECIMAL(10,2) NOT NULL,
    `discount_percent` DECIMAL(5,2) DEFAULT 0.00,
    `discount_amount` DECIMAL(10,2) DEFAULT 0.00,
    `subtotal` DECIMAL(10,2) NOT NULL,
    `tax_rate` DECIMAL(5,2) DEFAULT 18.00,
    `tax_amount` DECIMAL(10,2) NOT NULL,
    `total` DECIMAL(10,2) NOT NULL,
    `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_credit_note` (`credit_note_id`),
    KEY `idx_product` (`product_id`),
    CONSTRAINT `fk_credit_note_item_note` FOREIGN KEY (`credit_note_id`) REFERENCES `credit_notes`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_credit_note_item_product` FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Si existe una tabla de items de venta, agregar FK opcionalmente (compatible con esquemas que usan sale_details)
SET @sale_items_table := (
    SELECT TABLE_NAME FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME IN ('sale_items','sale_details')
    ORDER BY FIELD(TABLE_NAME,'sale_items','sale_details') LIMIT 1
);
SET @fk_exists := (
    SELECT COUNT(*) FROM information_schema.REFERENTIAL_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE() AND CONSTRAINT_NAME = 'fk_credit_note_item_sale_item'
);
SET @sql_fk_sale_item := IF(@fk_exists = 0 AND @sale_items_table IS NOT NULL,
    CONCAT('ALTER TABLE `credit_note_items` ADD CONSTRAINT `fk_credit_note_item_sale_item` FOREIGN KEY (`sale_item_id`) REFERENCES `', @sale_items_table, '`(`id`) ON DELETE SET NULL'),
    'SELECT ''fk_credit_note_item_sale_item no creado (ya existe o no hay tabla de items)'''
);
PREPARE stmt FROM @sql_fk_sale_item; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 3) Ampliar la tabla sales para referenciar notas de credito
-- Agregar columna credit_note_id solo si no existe (compatibilidad con versiones < 8.0.29)
SET @has_credit_note_id := (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'sales' AND COLUMN_NAME = 'credit_note_id'
);
SET @sql_add_credit_col := IF(@has_credit_note_id = 0,
    'ALTER TABLE `sales` ADD COLUMN `credit_note_id` INT NULL AFTER `cancellation_reason`',
    'SELECT ''credit_note_id ya existe'''
);
PREPARE stmt FROM @sql_add_credit_col; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Asegurar indice para la nueva columna
SET @idx_credit_note := (
    SELECT COUNT(1) FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'sales' AND INDEX_NAME = 'idx_credit_note_id'
);
SET @sql_idx_credit_note := IF(@idx_credit_note = 0,
    'ALTER TABLE `sales` ADD INDEX `idx_credit_note_id` (`credit_note_id`)',
    'SELECT ''idx_credit_note_id ya existe'''
);
PREPARE stmt FROM @sql_idx_credit_note; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Extender el enum de status para incluir credited
ALTER TABLE `sales`
    MODIFY COLUMN `status` ENUM('completed','cancelled','pending','refunded','credited')
        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'completed';

-- Agregar FK a credit_notes si aun no existe
SET @fk_sale_credit_note := (
    SELECT COUNT(*) FROM information_schema.REFERENTIAL_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE() AND CONSTRAINT_NAME = 'fk_sale_credit_note'
);
SET @sql_fk_sale := IF(@fk_sale_credit_note = 0,
    'ALTER TABLE `sales` ADD CONSTRAINT `fk_sale_credit_note` FOREIGN KEY (`credit_note_id`) REFERENCES `credit_notes`(`id`) ON DELETE SET NULL',
    'SELECT ''fk_sale_credit_note ya existe'''
);
PREPARE stmt FROM @sql_fk_sale; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 4) Permitir movimiento de inventario asociado a notas de credito
ALTER TABLE `inventory_movements`
    MODIFY COLUMN `movement_type` ENUM('sale','purchase','adjustment','return','transfer','credit_note')
        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;

-- Nota: no se modifican filas de productos ni se insertan nuevos productos.
