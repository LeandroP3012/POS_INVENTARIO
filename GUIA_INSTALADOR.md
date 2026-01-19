# GUÍA COMPLETA: CREAR INSTALADOR DEL SISTEMA POS

## 📋 Índice
1. [Requisitos](#requisitos)
2. [Preparación](#preparación)
3. [Construcción del Ejecutable](#construcción)
4. [Creación del Instalador](#instalador)
5. [Distribución](#distribución)

---

## 🔧 Requisitos

### Software Necesario:

1. **Python 3.8+** (con todas las dependencias del proyecto instaladas)
2. **PyInstaller** (para crear el .exe)
   ```powershell
   pip install pyinstaller
   ```

3. **Inno Setup** (para crear el instalador)
   - Descargar desde: https://jrsoftware.org/isdl.php
   - Instalar versión 6.2 o superior
   - Instalar el paquete de idioma español

4. **Visual C++ Redistributable** (para que funcione en otras PCs)
   - Incluido en Windows 10/11

---

## 📦 Preparación

### Paso 1: Verificar dependencias
```powershell
pip list | findstr "mysql openpyxl reportlab Pillow"
```

Todas estas deben estar instaladas.

### Paso 2: Crear icono (opcional)
- Crear un archivo `icon.ico` (256x256 px)
- Guardarlo en `assets/images/icon.ico`
- Herramientas online: https://www.icoconverter.com/

---

## 🔨 Construcción del Ejecutable

### Opción A: Script Automático (RECOMENDADO)

```powershell
# Ejecutar desde la raíz del proyecto
python build_installer.py
```

Este script:
- ✅ Limpia compilaciones anteriores
- ✅ Crea el ejecutable con PyInstaller
- ✅ Copia archivos necesarios
- ✅ Crea plantillas de configuración
- ✅ Genera instrucciones

**Duración estimada:** 5-10 minutos

### Opción B: Manual con PyInstaller

```powershell
pyinstaller --name=POS_Sistema `
    --onedir `
    --windowed `
    --icon=assets/images/icon.ico `
    --add-data="assets;assets" `
    --add-data="config;config" `
    --add-data="database;database" `
    --hidden-import=PIL._tkinter_finder `
    --hidden-import=openpyxl `
    --hidden-import=mysql.connector `
    --collect-all=mysql.connector `
    --noconsole `
    main.py
```

### Verificar el ejecutable:
```powershell
cd dist\POS_Sistema
.\POS_Sistema.exe
```

---

## 🎁 Creación del Instalador con Inno Setup

### Paso 1: Abrir Inno Setup Compiler
- Inicio > Inno Setup Compiler

### Paso 2: Compilar el script
- File > Open > Seleccionar `installer_script.iss`
- Build > Compile (o F9)

### Paso 3: El instalador se generará en:
```
Output\POS_Setup.exe
```

**Tamaño aproximado:** 80-150 MB (según dependencias)

---

## 📤 Distribución

### Archivo generado:
```
Output\POS_Setup.exe
```

### Para compartir:
1. **USB/Disco externo:**
   - Copiar `POS_Setup.exe`
   - Incluir `INSTRUCCIONES_INSTALACION.txt`

2. **Descarga online:**
   - Subir a Google Drive, Dropbox, OneDrive
   - Compartir enlace

3. **CD/DVD:**
   - Grabar con software de grabación
   - Incluir carpeta `database\` con scripts SQL

---

## 🖥️ Instalación en Computadora Nueva

### Requisitos de la PC destino:
- Windows 10/11 (64 bits)
- MySQL Server 8.0+
- 4 GB RAM mínimo
- 500 MB espacio en disco

### Pasos de instalación:

1. **Instalar MySQL** (si no está instalado)
   - https://dev.mysql.com/downloads/mysql/

2. **Ejecutar POS_Setup.exe**
   - Doble clic
   - Seguir el asistente
   - Ingresar credenciales de MySQL

3. **Configurar Base de Datos**
   - Abrir MySQL Workbench
   - Ejecutar scripts SQL en orden:
     ```
     C:\Program Files\Sistema POS\database\create_tables.sql
     C:\Program Files\Sistema POS\database\add_roles_system.sql
     C:\Program Files\Sistema POS\database\add_user_sessions_table.sql
     ```

4. **Iniciar aplicación**
   - Escritorio > Sistema POS
   - Usuario: `admin` / Contraseña: `admin123`

---

## 🔍 Solución de Problemas

### ❌ Error: "PyInstaller no encontrado"
```powershell
pip install pyinstaller
```

### ❌ Error: "Módulo no encontrado" al ejecutar .exe
Agregar al comando PyInstaller:
```powershell
--hidden-import=nombre_modulo
```

### ❌ Error: "No se puede conectar a MySQL"
- Verificar que MySQL esté ejecutándose
- Editar `C:\Program Files\Sistema POS\config\database.json`

### ❌ Instalador muy grande (>300 MB)
Causas comunes:
- Muchas dependencias innecesarias
- Solución: Usar entorno virtual limpio

### ❌ Antivirus bloquea el .exe
- Normal con ejecutables nuevos
- Agregar excepción en Windows Defender
- Firmar digitalmente el .exe (avanzado)

---

## 📊 Estructura del Instalador

```
POS_Setup.exe (Instalador)
│
├── Archivos del programa
│   ├── POS_Sistema.exe (ejecutable principal)
│   ├── _internal\ (dependencias de Python)
│   ├── assets\ (imágenes, recursos)
│   ├── config\ (configuración)
│   ├── database\ (scripts SQL)
│   └── logs\ (archivos de log)
│
├── Configuración
│   ├── Asistente de instalación
│   ├── Configuración de MySQL
│   └── Creación de accesos directos
│
└── Desinstalador
    └── unins000.exe
```

---

## 🚀 Comandos Rápidos

### Limpiar y reconstruir todo:
```powershell
# Limpiar
Remove-Item -Recurse -Force build, dist
Remove-Item *.spec

# Construir
python build_installer.py

# Compilar instalador (desde Inno Setup)
# File > Compile (F9)
```

### Crear versión portable (sin instalador):
```powershell
# El contenido de dist\POS_Sistema\ puede ejecutarse directamente
# Comprimir en ZIP para distribuir
Compress-Archive -Path dist\POS_Sistema\* -DestinationPath POS_Portable.zip
```

---

## 📝 Notas Importantes

### ⚠️ Antes de distribuir:
- [ ] Probar instalador en PC limpia
- [ ] Verificar conexión a MySQL
- [ ] Probar todas las funciones principales
- [ ] Revisar logs de errores
- [ ] Actualizar número de versión

### 🔒 Seguridad:
- NO incluir contraseñas en database.json
- Usar plantilla database_template.json
- Usuario configura en primera ejecución

### 📄 Documentación incluida:
- `README.md` - Manual de usuario
- `INSTRUCCIONES_INSTALACION.txt` - Guía de instalación
- `CONFIGURACION_BD.txt` - Config de base de datos
- `LICENSE.txt` - Licencia del software

---

## 🎯 Checklist Final

Antes de distribuir el instalador:

- [ ] Compilación exitosa sin errores
- [ ] Ejecutable funciona en PC de desarrollo
- [ ] Instalador creado con Inno Setup
- [ ] Probado en PC sin Python instalado
- [ ] Conexión a MySQL funcional
- [ ] Todos los módulos accesibles
- [ ] Scripts SQL incluidos
- [ ] Documentación completa
- [ ] Versión actualizada en installer_script.iss
- [ ] Información de contacto actualizada

---

## 📞 Soporte

Si tienes problemas durante el proceso:

1. Revisar logs en `build\` y `dist\`
2. Verificar versiones de dependencias
3. Consultar documentación de PyInstaller
4. Revisar Issues de Inno Setup

---

**¡Listo para distribuir tu Sistema POS! 🎉**
