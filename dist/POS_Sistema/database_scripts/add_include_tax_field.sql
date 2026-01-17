-- ================================================================
-- Script para agregar campo include_tax a la tabla sales
-- Fecha: 2026-01-10
-- Propósito: Registrar si una venta incluye IGV o no
-- Versión: 1.1 (seguro, puede ejecutarse múltiples veces)
-- ================================================================

USE pos_system;

-- Verificar si el campo ya existe
SET @column_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = 'pos_system' 
    AND TABLE_NAME = 'sales' 
    AND COLUMN_NAME = 'include_tax'
);

-- Agregar columna solo si no existe
SET @sql = IF(@column_exists = 0,
    'ALTER TABLE sales ADD COLUMN include_tax BOOLEAN DEFAULT TRUE COMMENT ''Indica si la venta incluye IGV'' AFTER tax_rate',
    'SELECT ''El campo include_tax ya existe'' AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Actualizar ventas existentes: todas incluyen IGV por defecto
-- (Esto es correcto porque todas las ventas antiguas fueron con IGV)
-- Usamos id > 0 para que funcione con safe mode activado
UPDATE sales SET include_tax = TRUE WHERE id > 0 AND (include_tax IS NULL OR include_tax = 0);

-- Verificar el cambio
SELECT 
    id, 
    sale_number, 
    subtotal, 
    tax_rate, 
    include_tax,
    tax_amount, 
    total_amount 
FROM sales 
ORDER BY id DESC
LIMIT 10;

-- Mostrar estadísticas
SELECT 
    COUNT(*) as total_ventas,
    SUM(CASE WHEN include_tax = 1 THEN 1 ELSE 0 END) as con_igv,
    SUM(CASE WHEN include_tax = 0 THEN 1 ELSE 0 END) as sin_igv
FROM sales;

-- Mostrar estructura actualizada
DESCRIBE sales;
