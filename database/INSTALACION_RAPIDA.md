# ⚡ INSTALACIÓN RÁPIDA - 5 MINUTOS

## 🎯 Objetivo
Tener la base de datos del Sistema POS funcionando en menos de 5 minutos.

---

## 📋 Requisitos Previos
- [x] MySQL 8.0+ instalado
- [x] Acceso root a MySQL
- [x] Cliente MySQL (Workbench, CLI, HeidiSQL, etc.)

---

## 🚀 Opción 1: MySQL Workbench (Recomendado)

### Paso 1: Abrir MySQL Workbench
1. Inicia MySQL Workbench
2. Conecta a tu servidor local (localhost)

### Paso 2: Importar Script
1. Ve al menú: **Server** → **Data Import**
2. Selecciona: **Import from Self-Contained File**
3. Busca y selecciona: `FULL_DATABASE_SCRIPT.sql`
4. En "Default Schema to be Imported To": déjalo vacío o selecciona "new"
5. Click en **Start Import**

### Paso 3: Verificar
1. Refresca la lista de bases de datos (F5)
2. Deberías ver: `pos_system` con 16 tablas
3. ✅ ¡Listo!

**Tiempo estimado:** 2 minutos

---

## 🚀 Opción 2: MySQL Command Line

### Paso 1: Abrir Terminal/CMD
```bash
# Windows (PowerShell)
cd C:\Users\USER\Desktop\POS\database

# Linux/Mac
cd /ruta/a/POS/database
```

### Paso 2: Ejecutar Script
```bash
mysql -u root -p < FULL_DATABASE_SCRIPT.sql
```

### Paso 3: Ingresar Contraseña
- Ingresa la contraseña de root cuando se te solicite
- El script se ejecutará automáticamente

### Paso 4: Verificar
```bash
mysql -u root -p
```

```sql
USE pos_system;
SHOW TABLES;
```

Deberías ver 16 tablas listadas.

**Tiempo estimado:** 3 minutos

---

## 🚀 Opción 3: Copiar y Pegar

### Paso 1: Abrir el Script
1. Abre `FULL_DATABASE_SCRIPT.sql` con tu editor favorito
2. Selecciona TODO el contenido (Ctrl+A)
3. Copia (Ctrl+C)

### Paso 2: Pegar en Cliente MySQL
1. Abre tu cliente MySQL (Workbench, HeidiSQL, etc.)
2. Crea una nueva consulta/query
3. Pega todo el contenido (Ctrl+V)
4. Ejecuta (Ctrl+Enter o botón Execute)

### Paso 3: Esperar
- El script puede tardar 30-60 segundos
- Verás mensajes de confirmación al final

**Tiempo estimado:** 4 minutos

---

## ✅ Verificación de Instalación

### Verificar Tablas
```sql
USE pos_system;
SHOW TABLES;
```

**Resultado esperado:** 16 tablas
```
activity_logs
categories
customers
inventory_movements
products
roles
sale_items
sale_payments
sales
suppliers
system_config
user_sessions
users
```

### Verificar Usuarios
```sql
SELECT username, full_name, user_type 
FROM users;
```

**Resultado esperado:**
```
admin      | Administrador del Sistema | admin
cajero1    | Cajero Principal          | cashier
```

### Verificar Productos
```sql
SELECT COUNT(*) as total FROM products;
```

**Resultado esperado:** 7 productos

### Verificar Configuraciones
```sql
SELECT COUNT(*) as total FROM system_config;
```

**Resultado esperado:** 18 configuraciones

---

## 🔑 Probar Login

### Desde MySQL
```sql
-- Verificar que la contraseña está correcta
SELECT username, 
       IF(password_hash = SHA2('123456', 256), 'OK', 'ERROR') as password_check
FROM users 
WHERE username = 'admin';
```

**Resultado esperado:** `OK`

### Desde la Aplicación
1. Inicia tu aplicación Python POS
2. Intenta hacer login:
   - **Usuario:** admin
   - **Contraseña:** 123456
3. Deberías entrar al dashboard

---

## 🔧 Solución de Problemas

### Error: "Database already exists"
```sql
-- Eliminar base de datos existente
DROP DATABASE IF EXISTS pos_system;

-- Ejecutar el script nuevamente
```

### Error: "Access denied for user"
```bash
# Verificar usuario y contraseña
mysql -u root -p

# Si es correcto, verificar permisos
GRANT ALL PRIVILEGES ON pos_system.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Can't connect to MySQL server"
```bash
# Windows: Verificar que MySQL está ejecutándose
net start MySQL80

# Linux/Mac
sudo systemctl start mysql
```

### Error: "Unknown character set: 'utf8mb4'"
- Tu versión de MySQL es muy antigua
- Actualiza a MySQL 8.0+ o MariaDB 10.5+
- O cambia UTF8MB4 a UTF8 en el script

---

## 🎨 Configuración Inicial (Opcional)

### Cambiar Contraseña de Admin
```sql
UPDATE users 
SET password_hash = SHA2('tu_nueva_contraseña', 256)
WHERE username = 'admin';
```

### Ajustar IGV
```sql
UPDATE system_config 
SET config_value = '19'  -- Cambiar al % deseado
WHERE config_key = 'tax_rate';
```

### Configurar Empresa
```sql
UPDATE system_config SET config_value = 'Mi Empresa S.A.C.' WHERE config_key = 'company_name';
UPDATE system_config SET config_value = 'Av. Principal 456' WHERE config_key = 'company_address';
UPDATE system_config SET config_value = '(01) 987-6543' WHERE config_key = 'company_phone';
UPDATE system_config SET config_value = 'ventas@miempresa.com' WHERE config_key = 'company_email';
```

---

## 📊 Siguientes Pasos

### 1. Cambiar Contraseñas (CRÍTICO)
```sql
-- Admin
UPDATE users SET password_hash = SHA2('contraseña_segura_admin', 256) WHERE username = 'admin';

-- Cajero
UPDATE users SET password_hash = SHA2('contraseña_segura_cajero', 256) WHERE username = 'cajero1';
```

### 2. Conectar con la Aplicación
Verifica el archivo `config/database.json`:
```json
{
    "host": "localhost",
    "user": "root",
    "password": "tu_contraseña_mysql",
    "database": "pos_system",
    "port": 3306
}
```

### 3. Agregar Tus Datos
- Categorías de tus productos
- Tu inventario real
- Tus proveedores
- Clientes frecuentes

### 4. Configurar Backup
```bash
# Crear backup diario (agregar a cron/task scheduler)
mysqldump -u root -p pos_system > backup_$(date +%Y%m%d).sql
```

---

## 📚 Documentación Adicional

- **LEEME_PRIMERO.md** → Resumen completo del paquete
- **README_DATABASE.md** → Documentación detallada
- **DIAGRAMA_BASE_DATOS.txt** → Estructura visual
- **CONSULTAS_UTILES.sql** → 50+ consultas listas para usar

---

## ✨ Checklist Final

Después de la instalación, verifica:

- [ ] Base de datos `pos_system` creada
- [ ] 16 tablas presentes
- [ ] 2 usuarios creados (admin, cajero1)
- [ ] 7 productos de ejemplo
- [ ] 8 categorías creadas
- [ ] Login funciona con admin/123456
- [ ] Contraseñas cambiadas
- [ ] Configuración de empresa ajustada
- [ ] Aplicación Python conectada
- [ ] Primera venta de prueba realizada

---

## 🎉 ¡Éxito!

Si todo lo anterior funciona, tu base de datos está **lista para producción**.

**Tiempo total:** 3-5 minutos  
**Nivel de dificultad:** ⭐⭐☆☆☆ (Fácil)

---

## 📞 ¿Necesitas Ayuda?

1. Revisa los logs de MySQL
2. Consulta `README_DATABASE.md` → Sección "Preguntas Frecuentes"
3. Ejecuta consultas de verificación de `CONSULTAS_UTILES.sql`

---

**¡Tu Sistema POS está listo para vender!** 🚀
