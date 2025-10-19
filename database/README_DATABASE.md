# 📊 Base de Datos - Sistema POS

## 📋 Descripción General

Script completo de base de datos para el Sistema POS con todas las tablas, relaciones, datos iniciales y configuraciones.

**Versión:** 2.0  
**Última actualización:** 19 de Octubre 2025  
**Charset:** UTF8MB4  
**Motor:** InnoDB

---

## 🗂️ Estructura de la Base de Datos

### Total: 16 Tablas + 1 Vista

### 📌 Tablas del Sistema

1. **system_config** - Configuraciones del sistema
2. **users** - Usuarios del sistema
3. **roles** - Sistema de roles y permisos
4. **user_sessions** - Sesiones activas
5. **activity_logs** - Registro de actividades

### 📦 Tablas de Inventario

6. **categories** - Categorías de productos
7. **suppliers** - Proveedores
8. **products** - Productos del inventario
9. **inventory_movements** - Movimientos de stock

### 💰 Tablas de Ventas

10. **customers** - Clientes
11. **sales** - Ventas realizadas
12. **sale_items** - Detalle de items vendidos
13. **sale_payments** - Pagos de ventas

### 📊 Vistas

14. **sales_detail** - Vista consolidada de ventas

---

## 🚀 Instalación

### Método 1: Importar desde MySQL Workbench

1. Abre MySQL Workbench
2. Conecta a tu servidor MySQL
3. Ve a: **Server → Data Import**
4. Selecciona: **Import from Self-Contained File**
5. Busca: `FULL_DATABASE_SCRIPT.sql`
6. Click en **Start Import**

### Método 2: Desde línea de comandos

```bash
mysql -u root -p < FULL_DATABASE_SCRIPT.sql
```

### Método 3: Copiar y pegar

1. Abre tu cliente MySQL
2. Abre el archivo `FULL_DATABASE_SCRIPT.sql`
3. Copia TODO el contenido
4. Pégalo en la consola SQL
5. Ejecuta

---

## 👤 Usuarios Predefinidos

### Usuario Administrador
- **Usuario:** `admin`
- **Contraseña:** `123456`
- **Rol:** Administrador
- **Permisos:** Acceso completo al sistema

### Usuario Cajero
- **Usuario:** `cajero1`
- **Contraseña:** `123456`
- **Rol:** Cajero
- **Permisos:** Acceso a ventas y productos (solo lectura)

> ⚠️ **IMPORTANTE:** Cambiar las contraseñas después de la primera instalación

---

## 🎭 Sistema de Roles

### 5 Roles Predefinidos

| ID | Rol | Código | Descripción |
|---|---|---|---|
| 1 | Super Admin | `super_admin` | Acceso total al sistema |
| 2 | Administrador | `admin` | Gestión de usuarios, inventario, ventas |
| 3 | Gerente | `manager` | Reportes y supervisión |
| 4 | Empleado | `employee` | Ventas e inventario básico |
| 5 | Cajero | `cashier` | Solo ventas |

---

## ⚙️ Configuraciones Iniciales

### Configuraciones Financieras
- **Moneda:** PEN (S/.)
- **Tasa de IGV:** 18%
- **Incluir IGV:** Activado por defecto
- **Decimales:** 2 lugares

### Configuraciones de Empresa
- **Nombre:** Mi Empresa POS
- **Dirección:** Av. Principal 123, Lima
- **Teléfono:** (01) 234-5678
- **Email:** info@miempresa.com

### Configuraciones de Seguridad
- **Timeout de sesión:** 3600 segundos (1 hora)
- **Intentos máximos de login:** 3
- **Backup automático:** Activado

---

## 📦 Datos de Ejemplo

### 8 Categorías
- BEBIDAS
- LACTEOS
- PANADERIA
- ABARROTES
- LIMPIEZA
- SNACKS
- CONSERVAS
- SERVICIOS

### 7 Productos de Ejemplo
1. Coca Cola 2L - S/ 6.50
2. Pan Integral - S/ 4.00
3. Leche Entera 1L - S/ 5.20
4. Arroz Superior 1kg - S/ 3.80
5. Servicio de Delivery - S/ 5.00
6. Aceite Vegetal 1L - S/ 12.50
7. Detergente 1kg - S/ 9.00

### 1 Cliente Genérico
- **Código:** GENERIC
- **Nombre:** Cliente Genérico
- **Documento:** 00000000

---

## 🔗 Relaciones Principales

```
users
  ├─► roles (role_id)
  ├─► user_sessions (user_id)
  └─► sales (user_id)

products
  ├─► categories (category_id)
  ├─► suppliers (supplier_id)
  ├─► sale_items (product_id)
  └─► inventory_movements (product_id)

sales
  ├─► users (user_id)
  ├─► customers (customer_id)
  ├─► sale_items (sale_id)
  └─► sale_payments (sale_id)
```

---

## 📝 Campos Importantes

### Productos
- **Precio de costo:** Para calcular margen de ganancia
- **Precio de venta:** Precio al público
- **Stock actual:** Cantidad disponible
- **Stock mínimo:** Alerta de reorden
- **IGV:** Configurable por producto (18% por defecto)

### Ventas
- **Número de venta:** Auto-generado (VTA-2025-00001)
- **Subtotal:** Monto sin impuestos
- **IGV:** Calculado según configuración
- **Total:** Monto final a pagar
- **Método de pago:** Efectivo, Tarjeta, Transferencia

### Clientes
- **Código:** Único por cliente
- **Tipo de documento:** DNI, RUC, Pasaporte
- **Tipo de cliente:** Retail, Mayorista, Corporativo
- **Límite de crédito:** Para ventas a crédito

---

## 🔧 Mantenimiento

### Backup Recomendado

```bash
# Backup completo
mysqldump -u root -p pos_system > backup_pos_$(date +%Y%m%d).sql

# Backup solo estructura
mysqldump -u root -p --no-data pos_system > estructura_pos.sql

# Backup solo datos
mysqldump -u root -p --no-create-info pos_system > datos_pos.sql
```

### Optimización

```sql
-- Optimizar todas las tablas
USE pos_system;
OPTIMIZE TABLE users, products, sales, sale_items;

-- Analizar tablas
ANALYZE TABLE products, sales;

-- Ver tamaño de tablas
SELECT 
    TABLE_NAME as Tabla,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) as 'Tamaño (MB)'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'pos_system'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

---

## 📊 Consultas Útiles

### Ventas del Día
```sql
SELECT 
    sale_number,
    total_amount,
    payment_method,
    sale_date
FROM sales
WHERE DATE(sale_date) = CURDATE()
AND status = 'completed';
```

### Productos con Stock Bajo
```sql
SELECT 
    code,
    name,
    current_stock,
    min_stock
FROM products
WHERE current_stock <= min_stock
AND track_stock = TRUE
AND active = TRUE;
```

### Top 10 Productos Más Vendidos
```sql
SELECT 
    p.code,
    p.name,
    SUM(si.quantity) as total_vendido,
    SUM(si.total) as ingresos_totales
FROM sale_items si
INNER JOIN products p ON si.product_id = p.id
INNER JOIN sales s ON si.sale_id = s.id
WHERE s.status = 'completed'
GROUP BY p.id
ORDER BY total_vendido DESC
LIMIT 10;
```

### Ventas por Cajero
```sql
SELECT 
    u.username,
    u.full_name,
    COUNT(s.id) as total_ventas,
    SUM(s.total_amount) as monto_total
FROM sales s
INNER JOIN users u ON s.user_id = u.id
WHERE DATE(s.sale_date) = CURDATE()
GROUP BY u.id;
```

---

## 🔒 Seguridad

### Recomendaciones

1. **Cambiar contraseñas por defecto**
   ```sql
   UPDATE users 
   SET password_hash = SHA2('nueva_contraseña', 256)
   WHERE username = 'admin';
   ```

2. **Crear usuario específico para la aplicación**
   ```sql
   CREATE USER 'pos_app'@'localhost' IDENTIFIED BY 'contraseña_segura';
   GRANT SELECT, INSERT, UPDATE, DELETE ON pos_system.* TO 'pos_app'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Limitar acceso remoto**
   ```sql
   -- Solo permitir conexiones locales
   CREATE USER 'pos_app'@'localhost' IDENTIFIED BY 'contraseña';
   ```

---

## ❓ Preguntas Frecuentes

### ¿Cómo reiniciar el contador de ventas?
```sql
UPDATE system_config 
SET config_value = '1' 
WHERE config_key = 'next_sale_number';
```

### ¿Cómo agregar un nuevo usuario?
```sql
INSERT INTO users (username, password_hash, email, full_name, user_type, role_id, active)
VALUES ('nuevo_usuario', SHA2('contraseña', 256), 'email@ejemplo.com', 'Nombre Completo', 'cashier', 5, TRUE);
```

### ¿Cómo cambiar la tasa de IGV?
```sql
UPDATE system_config 
SET config_value = '19' 
WHERE config_key = 'tax_rate';
```

### ¿Cómo desactivar el IGV por defecto?
```sql
UPDATE system_config 
SET config_value = 'false' 
WHERE config_key = 'include_tax';
```

---

## 📞 Soporte

Para problemas o consultas sobre la base de datos:

1. Revisa los logs del sistema en `/logs/database_*.log`
2. Verifica las conexiones activas
3. Consulta la documentación de MySQL 8.0

---

## 📜 Historial de Versiones

### Versión 2.0 (19/10/2025)
- ✅ Sistema completo de ventas
- ✅ Sistema de roles y permisos
- ✅ Sesiones de usuario
- ✅ Movimientos de inventario
- ✅ Cliente genérico
- ✅ Vista consolidada de ventas

### Versión 1.0 (Anterior)
- ✅ Estructura básica
- ✅ Usuarios y autenticación
- ✅ Productos e inventario
- ✅ Configuraciones del sistema

---

## 📄 Licencia

Script de base de datos para uso interno del Sistema POS.

---

**¡Base de datos lista para usar!** 🚀
