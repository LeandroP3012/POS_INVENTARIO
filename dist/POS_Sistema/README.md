# 🏪 Sistema POS v1.0

## Descripción
Sistema de Punto de Venta desarrollado en Python con arquitectura MVC, interfaz gráfica en Tkinter y base de datos MySQL.

## 🚀 Características Principales

### ✅ Sistema de Autenticación
- Login con roles de usuario (Admin, Supervisor, Cajero, Usuario)
- Gestión de sesiones con tiempo de expiración
- Sistema de permisos granular
- Funcionalidad "Recordar usuario"
- Bloqueo temporal por intentos fallidos

### 🏗️ Arquitectura MVC
- **Modelos**: Gestión de datos y lógica de negocio
- **Vistas**: Interfaz gráfica con Tkinter
- **Controladores**: Lógica de aplicación y coordinación

### 🔐 Seguridad
- Contraseñas hasheadas con SHA-256
- Validación de sesiones
- Control de acceso por permisos
- Logs de actividad detallados

### 🎨 Interfaz Moderna
- Diseño responsivo con TTK
- Colores personalizables
- Componentes reutilizables
- Experiencia de usuario intuitiva

## 📋 Requisitos del Sistema

### Software Necesario
- Python 3.8 o superior
- MySQL Server 8.0 o superior
- Windows 10/11 (recomendado)

### Dependencias Python
```bash
pip install mysql-connector-python
```

## 🛠️ Instalación

### 1. Preparar Base de Datos MySQL
```sql
-- Crear base de datos
CREATE DATABASE pos_sistema CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario (opcional)
CREATE USER 'pos_user'@'localhost' IDENTIFIED BY 'pos_password_2024';
GRANT ALL PRIVILEGES ON pos_sistema.* TO 'pos_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Configurar Conexión
Editar el archivo `config/database.json`:
```json
{
  "host": "localhost",
  "user": "pos_user",
  "password": "pos_password_2024",
  "database": "pos_sistema",
  "port": 3306
}
```

### 3. Ejecutar Script de Base de Datos
Ejecutar el contenido de `database/scriptDB.txt` en MySQL para crear las tablas necesarias.

### 4. Iniciar la Aplicación
```bash
python main.py
```

## 👤 Usuarios por Defecto

### Administrador
- **Usuario**: `admin`
- **Contraseña**: `123456`
- **Permisos**: Acceso completo al sistema

### Cajero
- **Usuario**: `cajero1`
- **Contraseña**: `123456`
- **Permisos**: Ventas y consultas básicas

## 📁 Estructura del Proyecto

```
POS/
├── main.py                 # Punto de entrada principal
├── README.md              # Este archivo
├── requirements.txt       # Dependencias Python
│
├── config/               # Configuración del sistema
│   ├── __init__.py
│   ├── database.json     # Configuración de BD
│   └── settings.py       # Configuración general
│
├── models/               # Modelos de datos (MVC)
│   ├── __init__.py
│   ├── base_model.py     # Clase base para modelos
│   ├── user_model.py     # Modelo de usuarios
│   └── auth_model.py     # Modelo de autenticación
│
├── views/                # Vistas/Interfaz (MVC)
│   ├── __init__.py
│   ├── base_view.py      # Clase base para vistas
│   └── login_view.py     # Vista de login
│
├── controllers/          # Controladores (MVC)
│   ├── __init__.py
│   ├── auth_controller.py    # Controlador de autenticación
│   └── main_controller.py    # Controlador principal
│
├── database/             # Scripts y conexión de BD
│   ├── __init__.py
│   ├── connection.py     # Gestión de conexiones
│   └── scriptDB.txt      # Script de creación de BD
│
├── logs/                 # Archivos de log
│   └── *.log            # Logs del sistema
│
└── assets/               # Recursos (iconos, imágenes)
    └── (vacío por ahora)
```

## 🔧 Configuración Avanzada

### Colores del Sistema
Editar `config/settings.py` para personalizar la paleta de colores:
```python
'colors': {
    'primary': '#2563eb',      # Azul principal
    'secondary': '#64748b',    # Gris secundario
    'success': '#16a34a',      # Verde éxito
    'warning': '#ca8a04',      # Amarillo advertencia
    'danger': '#dc2626',       # Rojo peligro
    # ... más colores
}
```

### Logging
Los logs se guardan en `logs/` con rotación automática:
- `pos_system.log`: Log principal del sistema
- `database_YYYYMMDD.log`: Logs específicos de base de datos

## 🚀 Uso del Sistema

### 1. Login
- Ejecutar `python main.py`
- Ingresar credenciales de usuario
- El sistema verificará permisos y creará sesión

### 2. Panel Principal
- Accesos rápidos según permisos del usuario
- Menú contextual por roles
- Información de sesión en tiempo real

### 3. Módulos Disponibles
- ✅ **Autenticación**: Sistema completo implementado
- 🚧 **Ventas**: En desarrollo
- 🚧 **Inventario**: En desarrollo  
- 🚧 **Reportes**: En desarrollo
- 🚧 **Administración**: En desarrollo

## 🔒 Seguridad

### Autenticación
- Contraseñas nunca se almacenan en texto plano
- Hash SHA-256 con salt implícito
- Sesiones con tiempo de expiración (8 horas por defecto)
- Bloqueo temporal después de 3 intentos fallidos

### Permisos
```python
# Ejemplos de permisos por rol
'admin': {
    'all_modules': True,
    'super_admin': True,
    'users_manage': True,
    'system_config': True
}

'cashier': {
    'sales_create': True,
    'sales_view': True,
    'products_view': True,
    'customers_view': True
}
```

## 🐛 Solución de Problemas

### Error de Conexión a MySQL
1. Verificar que MySQL esté ejecutándose
2. Comprobar credenciales en `config/database.json`
3. Verificar que la base de datos exista
4. Revisar logs en `logs/database_*.log`

### Error de Dependencias
```bash
# Instalar dependencias
pip install mysql-connector-python

# Verificar instalación
python -c "import mysql.connector; print('OK')"
```

### Problemas de Permisos
1. Verificar rol del usuario en la base de datos
2. Comprobar configuración de permisos en `models/user_model.py`
3. Revisar logs de autenticación

## 📈 Desarrollo Futuro

### Módulos Planeados
- [ ] Sistema de Ventas completo
- [ ] Gestión de Inventario
- [ ] Módulo de Clientes
- [ ] Reportes avanzados
- [ ] Backup automático
- [ ] Integración con hardware (impresoras, lectores)

### Mejoras Técnicas
- [ ] Migración a PostgreSQL (opcional)
- [ ] API REST para integración
- [ ] Interfaz web (Flask/Django)
- [ ] Aplicación móvil
- [ ] Sincronización en la nube

## 👥 Contribución

Este es un proyecto educativo que demuestra:
- Arquitectura MVC en Python
- Desarrollo de GUI con Tkinter
- Integración con MySQL
- Patrones de diseño
- Mejores prácticas de seguridad

## 📞 Soporte

Para problemas o dudas:
1. Revisar logs del sistema
2. Consultar documentación en código
3. Verificar configuración de base de datos

---

**Sistema POS v1.0** - Desarrollado con ❤️ en Python
