-- =============================================================================
-- CONSULTAS ÚTILES - SISTEMA POS
-- =============================================================================
-- Colección de consultas SQL útiles para el sistema POS
-- Incluye reportes, estadísticas, mantenimiento y administración
-- =============================================================================

USE pos_system;

-- =============================================================================
-- 📊 REPORTES DE VENTAS
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Ventas del día actual
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    s.sale_number as 'Número',
    s.sale_date as 'Fecha',
    c.name as 'Cliente',
    s.total_amount as 'Total',
    s.payment_method as 'Método Pago',
    u.full_name as 'Cajero',
    s.status as 'Estado'
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.id
INNER JOIN users u ON s.user_id = u.id
WHERE DATE(s.sale_date) = CURDATE()
AND s.status = 'completed'
ORDER BY s.sale_date DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Resumen de ventas del día
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    COUNT(*) as 'Total Ventas',
    SUM(total_amount) as 'Monto Total',
    AVG(total_amount) as 'Ticket Promedio',
    SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END) as 'Efectivo',
    SUM(CASE WHEN payment_method = 'card' THEN total_amount ELSE 0 END) as 'Tarjeta',
    SUM(CASE WHEN payment_method = 'transfer' THEN total_amount ELSE 0 END) as 'Transferencia'
FROM sales
WHERE DATE(sale_date) = CURDATE()
AND status = 'completed';

-- ─────────────────────────────────────────────────────────────────────────────
-- Ventas por rango de fechas
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    DATE(s.sale_date) as 'Fecha',
    COUNT(*) as 'Cantidad',
    SUM(s.total_amount) as 'Monto Total',
    AVG(s.total_amount) as 'Ticket Promedio'
FROM sales s
WHERE s.sale_date BETWEEN '2025-01-01' AND '2025-12-31'
AND s.status = 'completed'
GROUP BY DATE(s.sale_date)
ORDER BY DATE(s.sale_date) DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Ventas por cajero (del día)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    u.username as 'Usuario',
    u.full_name as 'Nombre',
    COUNT(s.id) as 'Ventas',
    SUM(s.total_amount) as 'Monto Total',
    AVG(s.total_amount) as 'Ticket Promedio'
FROM sales s
INNER JOIN users u ON s.user_id = u.id
WHERE DATE(s.sale_date) = CURDATE()
AND s.status = 'completed'
GROUP BY u.id
ORDER BY SUM(s.total_amount) DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Detalle completo de una venta específica
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    -- Cabecera
    s.sale_number,
    s.sale_date,
    COALESCE(c.name, 'Cliente Genérico') as cliente,
    u.full_name as cajero,
    
    -- Items
    si.product_name,
    si.quantity,
    si.unit_price,
    si.discount_amount,
    si.tax_amount,
    si.total,
    
    -- Total
    s.subtotal,
    s.tax_amount as igv_total,
    s.total_amount,
    s.payment_method
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.id
INNER JOIN users u ON s.user_id = u.id
LEFT JOIN sale_items si ON s.id = si.sale_id
WHERE s.sale_number = 'VTA-2025-00001';  -- Cambiar número de venta

-- =============================================================================
-- 📦 REPORTES DE INVENTARIO
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Productos con stock bajo
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    p.code as 'Código',
    p.name as 'Producto',
    p.current_stock as 'Stock Actual',
    p.min_stock as 'Stock Mínimo',
    (p.min_stock - p.current_stock) as 'Faltan',
    c.name as 'Categoría',
    s.name as 'Proveedor'
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN suppliers s ON p.supplier_id = s.id
WHERE p.current_stock <= p.min_stock
AND p.track_stock = TRUE
AND p.active = TRUE
ORDER BY (p.min_stock - p.current_stock) DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Productos sin stock
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    code as 'Código',
    name as 'Producto',
    current_stock as 'Stock',
    min_stock as 'Stock Mínimo',
    sale_price as 'Precio'
FROM products
WHERE current_stock = 0
AND track_stock = TRUE
AND active = TRUE
ORDER BY name;

-- ─────────────────────────────────────────────────────────────────────────────
-- Valor del inventario
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    COUNT(*) as 'Total Productos',
    SUM(current_stock) as 'Unidades Totales',
    SUM(current_stock * cost_price) as 'Valor Costo',
    SUM(current_stock * sale_price) as 'Valor Venta',
    SUM(current_stock * (sale_price - cost_price)) as 'Ganancia Potencial'
FROM products
WHERE active = TRUE
AND track_stock = TRUE;

-- ─────────────────────────────────────────────────────────────────────────────
-- Movimientos de inventario recientes
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    im.created_at as 'Fecha',
    p.code as 'Código',
    p.name as 'Producto',
    im.movement_type as 'Tipo',
    im.quantity as 'Cantidad',
    im.previous_stock as 'Stock Anterior',
    im.new_stock as 'Stock Nuevo',
    u.full_name as 'Usuario'
FROM inventory_movements im
INNER JOIN products p ON im.product_id = p.id
INNER JOIN users u ON im.user_id = u.id
ORDER BY im.created_at DESC
LIMIT 50;

-- =============================================================================
-- 🏆 TOP PRODUCTOS
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Top 10 productos más vendidos (cantidad)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    p.code as 'Código',
    p.name as 'Producto',
    SUM(si.quantity) as 'Unidades Vendidas',
    COUNT(DISTINCT si.sale_id) as 'Ventas',
    SUM(si.total) as 'Ingresos Totales',
    AVG(si.unit_price) as 'Precio Promedio'
FROM sale_items si
INNER JOIN products p ON si.product_id = p.id
INNER JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'completed'
GROUP BY p.id
ORDER BY SUM(si.quantity) DESC
LIMIT 10;

-- ─────────────────────────────────────────────────────────────────────────────
-- Top 10 productos por ingresos
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    p.code as 'Código',
    p.name as 'Producto',
    SUM(si.quantity) as 'Unidades',
    SUM(si.total) as 'Ingresos',
    AVG(si.unit_price) as 'Precio Promedio',
    COUNT(DISTINCT si.sale_id) as 'Ventas'
FROM sale_items si
INNER JOIN products p ON si.product_id = p.id
INNER JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'completed'
GROUP BY p.id
ORDER BY SUM(si.total) DESC
LIMIT 10;

-- ─────────────────────────────────────────────────────────────────────────────
-- Productos nunca vendidos
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    p.code as 'Código',
    p.name as 'Producto',
    p.current_stock as 'Stock',
    p.sale_price as 'Precio',
    c.name as 'Categoría'
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN sale_items si ON p.id = si.product_id
WHERE si.id IS NULL
AND p.active = TRUE
AND p.is_service = FALSE
ORDER BY p.created_at DESC;

-- =============================================================================
-- 👥 REPORTES DE CLIENTES
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Top 10 clientes por compras
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    c.code as 'Código',
    c.name as 'Cliente',
    c.document_number as 'Documento',
    COUNT(s.id) as 'Compras',
    SUM(s.total_amount) as 'Monto Total',
    AVG(s.total_amount) as 'Ticket Promedio',
    MAX(s.sale_date) as 'Última Compra'
FROM customers c
INNER JOIN sales s ON c.id = s.customer_id
WHERE s.status = 'completed'
GROUP BY c.id
ORDER BY SUM(s.total_amount) DESC
LIMIT 10;

-- ─────────────────────────────────────────────────────────────────────────────
-- Clientes sin compras (últimos 30 días)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    c.code,
    c.name,
    c.phone,
    c.email,
    MAX(s.sale_date) as 'Última Compra'
FROM customers c
LEFT JOIN sales s ON c.id = s.customer_id
WHERE c.status = 'active'
GROUP BY c.id
HAVING MAX(s.sale_date) < DATE_SUB(NOW(), INTERVAL 30 DAY)
OR MAX(s.sale_date) IS NULL
ORDER BY MAX(s.sale_date) ASC;

-- =============================================================================
-- 💰 REPORTES FINANCIEROS
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Resumen financiero del mes
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    YEAR(sale_date) as 'Año',
    MONTH(sale_date) as 'Mes',
    COUNT(*) as 'Ventas',
    SUM(subtotal) as 'Subtotal',
    SUM(tax_amount) as 'IGV',
    SUM(discount_amount) as 'Descuentos',
    SUM(total_amount) as 'Total'
FROM sales
WHERE status = 'completed'
AND YEAR(sale_date) = YEAR(CURDATE())
GROUP BY YEAR(sale_date), MONTH(sale_date)
ORDER BY YEAR(sale_date) DESC, MONTH(sale_date) DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Métodos de pago más usados
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    payment_method as 'Método',
    COUNT(*) as 'Cantidad',
    SUM(total_amount) as 'Monto Total',
    AVG(total_amount) as 'Ticket Promedio',
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales WHERE status = 'completed'), 2) as '% Uso'
FROM sales
WHERE status = 'completed'
GROUP BY payment_method
ORDER BY COUNT(*) DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Análisis de rentabilidad por producto
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    p.code,
    p.name,
    p.cost_price as 'Costo',
    p.sale_price as 'Venta',
    (p.sale_price - p.cost_price) as 'Margen',
    ROUND(((p.sale_price - p.cost_price) / p.cost_price * 100), 2) as 'Margen %',
    SUM(si.quantity) as 'Unidades Vendidas',
    SUM(si.quantity * (si.unit_price - p.cost_price)) as 'Ganancia Total'
FROM products p
LEFT JOIN sale_items si ON p.id = si.product_id
LEFT JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'completed' OR s.status IS NULL
GROUP BY p.id
ORDER BY SUM(si.quantity * (si.unit_price - p.cost_price)) DESC;

-- =============================================================================
-- 🔐 REPORTES DE USUARIOS Y SEGURIDAD
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Usuarios activos y sus roles
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    u.username as 'Usuario',
    u.full_name as 'Nombre',
    u.email as 'Email',
    u.user_type as 'Tipo',
    r.name as 'Rol',
    u.active as 'Activo',
    u.last_login as 'Último Login'
FROM users u
LEFT JOIN roles r ON u.role_id = r.id
ORDER BY u.active DESC, u.last_login DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Sesiones activas
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    us.username,
    us.user_type,
    us.login_time,
    us.last_activity,
    TIMESTAMPDIFF(MINUTE, us.last_activity, NOW()) as 'Minutos Inactivo',
    us.is_active
FROM user_sessions us
WHERE us.is_active = TRUE
AND us.expires_at > NOW()
ORDER BY us.last_activity DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Actividad reciente del sistema
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    al.created_at as 'Fecha',
    u.username as 'Usuario',
    al.activity_type as 'Actividad',
    al.table_name as 'Tabla',
    al.description as 'Descripción'
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC
LIMIT 50;

-- =============================================================================
-- 🔧 MANTENIMIENTO Y ADMINISTRACIÓN
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Tamaño de las tablas
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    TABLE_NAME as 'Tabla',
    TABLE_ROWS as 'Registros',
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) as 'Tamaño (MB)'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'pos_system'
AND TABLE_TYPE = 'BASE TABLE'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;

-- ─────────────────────────────────────────────────────────────────────────────
-- Limpiar sesiones expiradas
-- ─────────────────────────────────────────────────────────────────────────────
DELETE FROM user_sessions
WHERE expires_at < NOW()
OR (is_active = FALSE AND logout_time < DATE_SUB(NOW(), INTERVAL 30 DAY));

-- ─────────────────────────────────────────────────────────────────────────────
-- Limpiar logs antiguos (más de 90 días)
-- ─────────────────────────────────────────────────────────────────────────────
DELETE FROM activity_logs
WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- ─────────────────────────────────────────────────────────────────────────────
-- Optimizar tablas
-- ─────────────────────────────────────────────────────────────────────────────
OPTIMIZE TABLE users, products, sales, sale_items, inventory_movements;

-- ─────────────────────────────────────────────────────────────────────────────
-- Analizar tablas
-- ─────────────────────────────────────────────────────────────────────────────
ANALYZE TABLE products, sales, sale_items;

-- =============================================================================
-- ⚙️ CONFIGURACIÓN DEL SISTEMA
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Ver todas las configuraciones
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    category as 'Categoría',
    config_key as 'Clave',
    config_value as 'Valor',
    config_type as 'Tipo',
    is_editable as 'Editable'
FROM system_config
ORDER BY category, config_key;

-- ─────────────────────────────────────────────────────────────────────────────
-- Cambiar tasa de IGV
-- ─────────────────────────────────────────────────────────────────────────────
UPDATE system_config 
SET config_value = '19'  -- Cambiar al valor deseado
WHERE config_key = 'tax_rate';

-- ─────────────────────────────────────────────────────────────────────────────
-- Reiniciar contador de ventas
-- ─────────────────────────────────────────────────────────────────────────────
UPDATE system_config 
SET config_value = '1' 
WHERE config_key = 'next_sale_number';

-- =============================================================================
-- 🔑 GESTIÓN DE USUARIOS
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Crear nuevo usuario
-- ─────────────────────────────────────────────────────────────────────────────
INSERT INTO users (username, password_hash, email, full_name, user_type, role_id, active)
VALUES (
    'nuevo_usuario',                         -- Usuario
    SHA2('contraseña_segura', 256),         -- Contraseña hasheada
    'email@ejemplo.com',                     -- Email
    'Nombre Completo',                       -- Nombre
    'cashier',                               -- Tipo
    5,                                       -- Rol (5 = Cajero)
    TRUE                                     -- Activo
);

-- ─────────────────────────────────────────────────────────────────────────────
-- Cambiar contraseña de usuario
-- ─────────────────────────────────────────────────────────────────────────────
UPDATE users 
SET password_hash = SHA2('nueva_contraseña', 256)
WHERE username = 'admin';

-- ─────────────────────────────────────────────────────────────────────────────
-- Desbloquear usuario
-- ─────────────────────────────────────────────────────────────────────────────
UPDATE users 
SET failed_attempts = 0, 
    locked_until = NULL
WHERE username = 'usuario_bloqueado';

-- ─────────────────────────────────────────────────────────────────────────────
-- Desactivar usuario
-- ─────────────────────────────────────────────────────────────────────────────
UPDATE users 
SET active = FALSE
WHERE username = 'usuario_a_desactivar';

-- =============================================================================
-- 📊 ESTADÍSTICAS GENERALES
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- Dashboard: Resumen general del día
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 
    'VENTAS HOY' as Métrica,
    COUNT(*) as Cantidad,
    CONCAT('S/ ', FORMAT(SUM(total_amount), 2)) as Monto
FROM sales 
WHERE DATE(sale_date) = CURDATE() AND status = 'completed'

UNION ALL

SELECT 
    'PRODUCTOS ACTIVOS',
    COUNT(*),
    CONCAT(SUM(current_stock), ' unidades')
FROM products 
WHERE active = TRUE

UNION ALL

SELECT 
    'PRODUCTOS BAJO STOCK',
    COUNT(*),
    CONCAT('Alerta en ', COUNT(*), ' productos')
FROM products 
WHERE current_stock <= min_stock AND active = TRUE AND track_stock = TRUE

UNION ALL

SELECT 
    'USUARIOS ACTIVOS',
    COUNT(*),
    CONCAT(COUNT(*), ' usuarios')
FROM users 
WHERE active = TRUE;

-- =============================================================================
-- FIN DE CONSULTAS ÚTILES
-- =============================================================================
