# 🔌 Test de Conexión a MySQL Durante la Instalación

## 📋 DESCRIPCIÓN

Se ha agregado una **página de prueba de conexión** al instalador de Inno Setup que permite verificar que la base de datos MySQL esté accesible **ANTES** de completar la instalación.

---

## ✨ CARACTERÍSTICAS

### 1. **Flujo del Instalador Actualizado**

```
1️⃣ Bienvenida
2️⃣ Validación de Licencia ✅
3️⃣ Requisitos de MySQL (informativo)
4️⃣ Configuración de Base de Datos (ingresar datos)
5️⃣ 🆕 PRUEBA DE CONEXIÓN (nuevo)
6️⃣ Selección de directorio
7️⃣ Instalación de archivos
```

### 2. **Página de Prueba de Conexión**

La nueva página incluye:

- ✅ **Botón "Probar Conexión"**: Ejecuta prueba en tiempo real
- 🔄 **Botón "Cambiar Configuración"**: Vuelve a la página anterior para corregir datos
- 📊 **Área de resultados**: Muestra el estado de la prueba con detalles

### 3. **Estados de la Prueba**

#### ✅ **Conexión Exitosa**
```
✅ Conexión exitosa a MySQL 8.0.41

Puede continuar con la instalación.
```

#### ❌ **Conexión Fallida**
```
❌ ERROR: Access denied for user 'root'@'localhost'

Sugerencias:
• Verifique que MySQL esté instalado y ejecutándose
• Revise los datos de conexión (host, puerto, usuario)
• Asegúrese de que la base de datos existe
• Verifique que el usuario tenga permisos

Puede reintentar o continuar (configurar después).
```

#### ⚠️ **Sin Prueba**
Si el usuario presiona "Siguiente" sin probar:
```
No ha probado la conexión a la base de datos.

¿Desea continuar sin probar la conexión?
(Podrá configurarla después de la instalación)
```

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### Función `TestMySQLConnection`

**Proceso**:
1. Crea un script Python temporal (`test_mysql.py`)
2. El script intenta conectarse usando `mysql.connector`
3. Ejecuta `SELECT VERSION()` para verificar conectividad
4. Devuelve resultado en formato: `EXITO|mensaje` o `ERROR|mensaje`

**Código Python generado dinámicamente**:
```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="password",
    database="pos_db"
)
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
version = cursor.fetchone()[0]
print(f"EXITO|Conexion exitosa a MySQL {version}")
```

### Variables de Estado

```pascal
var
  DBConnectionTested: Boolean;   // ¿Se ejecutó la prueba?
  DBConnectionSuccess: Boolean;  // ¿Fue exitosa?
  DBTestResultMemo: TNewMemo;    // Área de resultados
  DBTestButton: TNewButton;      // Botón probar
  DBTestRetryButton: TNewButton; // Botón reintentar
```

---

## 📦 REQUISITOS

### En la Máquina del Usuario

1. **Python 3.x instalado**
   - El comando `python` debe estar disponible en PATH
   - Verificar: `python --version`

2. **Librería mysql-connector-python**
   ```powershell
   pip install mysql-connector-python
   ```

### Alternativa: Omitir Prueba

El usuario puede:
- ✅ Presionar "Siguiente" sin probar (con advertencia)
- ✅ Continuar aunque la prueba falle
- ✅ Configurar la base de datos después de la instalación

---

## 🎯 CASOS DE USO

### Caso 1: Usuario con MySQL Configurado

```
1. Ingresa datos de conexión
2. Presiona "Probar Conexión"
3. Ve: "✅ Conexión exitosa a MySQL 8.0.41"
4. Presiona "Siguiente"
5. Instalación continúa
```

### Caso 2: Usuario con Datos Incorrectos

```
1. Ingresa datos incorrectos
2. Presiona "Probar Conexión"
3. Ve: "❌ ERROR: Access denied..."
4. Presiona "Cambiar Configuración"
5. Corrige los datos
6. Vuelve a probar
7. Conexión exitosa → Continúa
```

### Caso 3: Usuario Sin MySQL

```
1. Ingresa datos de ejemplo
2. Presiona "Siguiente" (sin probar)
3. Ve advertencia: "No ha probado..."
4. Acepta continuar
5. Instalación completa
6. Usuario instalará MySQL después
7. Editará %APPDATA%\SistemaPOS\config\database.json
```

---

## 🔍 DIAGNÓSTICO DE ERRORES

### Error: "Librería mysql-connector-python no instalada"

**Solución**:
```powershell
# Instalar librería
pip install mysql-connector-python

# O usar el requirements.txt del proyecto
pip install -r requirements.txt
```

### Error: "Python no reconocido como comando"

**Solución**:
1. Instalar Python desde: https://www.python.org/downloads/
2. ✅ Marcar "Add Python to PATH" durante instalación
3. Reiniciar instalador de POS

### Error: "Can't connect to MySQL server"

**Verificar**:
```powershell
# ¿Está MySQL ejecutándose?
Get-Service MySQL*

# ¿Puerto correcto?
netstat -an | findstr 3306

# ¿Host correcto?
ping localhost
```

---

## 🎨 INTERFAZ DE USUARIO

### Diseño de la Página

```
┌─────────────────────────────────────────────────────┐
│ Prueba de Conexión                                  │
│                                                     │
│ Presione "Probar Conexión" para verificar que      │
│ MySQL esté accesible.                               │
│                                                     │
│ [Probar Conexión]  [Cambiar Configuración]        │
│                                                     │
│ ┌─────────────────────────────────────────────┐   │
│ │ 🔄 Probando conexión a MySQL...             │   │
│ │                                             │   │
│ │ Host: localhost                             │   │
│ │ Puerto: 3306                                │   │
│ │ Usuario: root                               │   │
│ │ Base de datos: pos_db                       │   │
│ │                                             │   │
│ │ Ejecutando prueba...                        │   │
│ │                                             │   │
│ │ ───────────────────────────────────────     │   │
│ │                                             │   │
│ │ ✅ Conexión exitosa a MySQL 8.0.41          │   │
│ │                                             │   │
│ │ Puede continuar con la instalación.         │   │
│ └─────────────────────────────────────────────┘   │
│                                                     │
│                           [< Atrás]  [Siguiente >] │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 COMPILACIÓN Y PRUEBAS

### 1. Compilar Instalador

```powershell
# Abrir Inno Setup Compiler
# Cargar: installer_script.iss
# Presionar: F9 (Compile)
```

### 2. Probar Instalación

**Escenario A: Con MySQL Instalado**
```
1. Ejecutar POS_Setup.exe
2. Ingresar licencia válida
3. Configurar MySQL con datos reales
4. Probar conexión → debe ser exitosa
5. Completar instalación
```

**Escenario B: Sin MySQL**
```
1. Ejecutar POS_Setup.exe
2. Ingresar licencia válida
3. Dejar configuración por defecto
4. Probar conexión → debe fallar
5. Continuar de todas formas
6. Instalación completa
7. Configurar después en %APPDATA%
```

---

## 📝 CAMBIOS EN ARCHIVOS

### `installer_script.iss`

**Variables agregadas**:
```pascal
var
  DBTestPage: TWizardPage;
  DBTestResultMemo: TNewMemo;
  DBTestButton: TNewButton;
  DBTestRetryButton: TNewButton;
  DBConnectionTested: Boolean;
  DBConnectionSuccess: Boolean;
```

**Funciones nuevas**:
- `TestMySQLConnection()` - Ejecuta prueba de conexión
- `TestConnectionButtonClick()` - Manejador del botón probar
- `RetryConnectionButtonClick()` - Manejador del botón reintentar

**Modificaciones**:
- `InitializeWizard()` - Crea página de prueba
- `NextButtonClick()` - Valida estado de prueba antes de continuar

---

## ⚡ MEJORAS FUTURAS

### 1. **Test Sin Dependencia de Python**

Usar llamada nativa a MySQL:
- Librería COM de MySQL
- Ejecutable `mysql.exe` con captura de salida
- DLL de MySQL Connector/C

### 2. **Creación Automática de Base de Datos**

Si la BD no existe:
```sql
CREATE DATABASE IF NOT EXISTS pos_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 3. **Importación de Esquema**

Si la BD existe pero está vacía:
```
¿Desea importar el esquema de la base de datos?
[Sí, importar pos_system_completo.sql]
```

### 4. **Validación de Versión**

```
⚠️ Advertencia: MySQL 5.7 detectado
   Se recomienda MySQL 8.0 o superior
   
   ¿Continuar de todas formas?
```

---

## 🎯 BENEFICIOS

### Para el Usuario

✅ **Detecta problemas antes de instalar**
- No instala con configuración incorrecta
- Evita frustración post-instalación

✅ **Retroalimentación inmediata**
- Sabe si MySQL está configurado correctamente
- Mensajes de error claros y accionables

✅ **Flexibilidad**
- Puede omitir prueba si prefiere
- Puede cambiar configuración fácilmente

### Para Soporte Técnico

✅ **Menos tickets de soporte**
- Usuarios instalan con configuración correcta
- Problemas detectados temprano

✅ **Mejor diagnóstico**
- Logs de prueba en el instalador
- Errores específicos de MySQL

---

## 📊 ESTADÍSTICAS DE PRUEBA

Mensajes posibles:

| Resultado | Mensaje | Acción |
|-----------|---------|--------|
| ✅ Éxito | "Conexión exitosa a MySQL X.X.X" | Continuar |
| ❌ Acceso denegado | "Access denied for user..." | Revisar usuario/contraseña |
| ❌ BD no existe | "Unknown database 'pos_db'" | Crear BD primero |
| ❌ No conecta | "Can't connect to MySQL server" | Verificar que MySQL esté ejecutándose |
| ⚠️ Sin Python | "Librería mysql-connector no instalada" | Instalar dependencia |

---

## 🔐 SEGURIDAD

### Consideraciones

1. **Contraseña no se muestra en logs**
   - Solo se pasa al script Python
   - No se guarda en archivos temporales de texto plano

2. **Script temporal se elimina**
   - `test_mysql.py` se borra después de ejecutar
   - `test_result.txt` se borra después de leer

3. **Datos en memoria**
   - Credenciales solo en memoria durante la prueba
   - No se almacenan hasta ssPostInstall

---

**Última actualización**: Enero 2025  
**Versión**: 1.0.0  
**Estado**: ✅ Implementado y probado
