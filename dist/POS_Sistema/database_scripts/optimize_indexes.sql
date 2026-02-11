-- ====================================================================
-- OPTIMIZACIÓN DE ÍNDICES PARA MEJORAR PERFORMANCE DE REPORTES
-- ====================================================================
-- Este script crea índices optimizados para las consultas más frecuentes
-- del sistema POS, especialmente para reportes de ventas.
--
-- Ejecutar este script mejorará significativamente la velocidad de:
-- - Reporte Diario de Ventas
-- - Reportes por rango de fechas
-- - Consultas por cajero
-- - Reportes de productos vendidos
-- ====================================================================

USE pos_system;

-- ====================================================================
-- ÍNDICES PARA LA TABLA SALES
-- ====================================================================

-- Índice compuesto para consultas de reportes por fecha y estado
-- Esto optimiza las consultas WHERE sale_date BETWEEN ? AND ? AND status = 'completed'
CREATE INDEX IF NOT EXISTS idx_sales_date_status 
ON sales(sale_date, status);

-- Índice para consultas por cajero y fecha
-- Optimiza reportes filtrados por usuario
CREATE INDEX IF NOT EXISTS idx_sales_user_date 
ON sales(user_id, sale_date, status);

-- Índice para consultas por método de pago
-- Útil para reportes de ventas por método de pago
CREATE INDEX IF NOT EXISTS idx_sales_payment_method 
ON sales(payment_method, sale_date);

-- Índice para consultas por cliente
CREATE INDEX IF NOT EXISTS idx_sales_customer 
ON sales(customer_id, sale_date);

-- ====================================================================
-- ÍNDICES PARA LA TABLA SALE_DETAILS
-- ====================================================================

-- Índice compuesto para optimizar cálculo de productos vendidos
-- Optimiza SUM(quantity) y reportes de productos
CREATE INDEX IF NOT EXISTS idx_sale_details_product 
ON sale_details(product_id, sale_id);

-- Índice para relacionar detalles con ventas
-- Mejora JOINs entre sales y sale_details
CREATE INDEX IF NOT EXISTS idx_sale_details_sale 
ON sale_details(sale_id);

-- ====================================================================
-- ÍNDICES PARA LA TABLA PRODUCTS
-- ====================================================================

-- Índice para búsquedas por SKU
CREATE INDEX IF NOT EXISTS idx_products_sku 
ON products(sku);

-- Índice para búsquedas por categoría
CREATE INDEX IF NOT EXISTS idx_products_category 
ON products(category_id);

-- Índice para filtros de stock
CREATE INDEX IF NOT EXISTS idx_products_stock 
ON products(stock);

-- ====================================================================
-- ÍNDICES PARA LA TABLA CREDIT_NOTES
-- ====================================================================

-- Índice para reportes de notas de crédito por fecha
CREATE INDEX IF NOT EXISTS idx_credit_notes_date 
ON credit_notes(issue_date, status);

-- Índice para búsqueda por venta original
CREATE INDEX IF NOT EXISTS idx_credit_notes_sale 
ON credit_notes(original_sale_id);

-- ====================================================================
-- ÍNDICES PARA LA TABLA USERS
-- ====================================================================

-- Índice para búsquedas por rol
CREATE INDEX IF NOT EXISTS idx_users_role 
ON users(role_id, active);

-- Índice para búsquedas por username
CREATE INDEX IF NOT EXISTS idx_users_username 
ON users(username);

-- ====================================================================
-- VERIFICAR ÍNDICES CREADOS
-- ====================================================================

-- Consultar todos los índices de la tabla sales
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'pos_system'
AND TABLE_NAME IN ('sales', 'sale_details', 'products', 'credit_notes', 'users')
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- ====================================================================
-- ESTADÍSTICAS DE TABLAS
-- ====================================================================

-- Ver tamaño y número de registros en las tablas principales
SELECT 
    table_name AS 'Tabla',
    table_rows AS 'Registros (aprox)',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Tamaño MB'
FROM information_schema.TABLES
WHERE table_schema = 'pos_system'
AND table_name IN ('sales', 'sale_details', 'products', 'credit_notes', 'users')
ORDER BY (data_length + index_length) DESC;

-- ====================================================================
-- NOTAS IMPORTANTES
-- ====================================================================
-- 
-- 1. Los índices mejoran la velocidad de lectura (SELECT) pero pueden
--    afectar ligeramente la velocidad de escritura (INSERT/UPDATE).
--    En un sistema POS, las lecturas de reportes son mucho más frecuentes
--    que las escrituras, por lo que el beneficio es significativo.
--
-- 2. MySQL usa automáticamente el mejor índice disponible para cada consulta.
--
-- 3. Para verificar si un índice se está usando en una consulta específica,
--    usar: EXPLAIN SELECT ... antes de la consulta.
--
-- 4. Ejecutar ANALYZE TABLE periódicamente para mantener las estadísticas
--    de índices actualizadas:
--    ANALYZE TABLE sales, sale_details, products, credit_notes, users;
--
-- ====================================================================
