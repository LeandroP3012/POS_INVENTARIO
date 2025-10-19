# 📦 Dependencias del Sistema POS

## 📋 Resumen Rápido

Tu Sistema POS necesita **solo 2 dependencias externas**:

```
✅ mysql-connector-python  (Conexión a MySQL)
✅ Pillow                   (Manejo de imágenes)
```

Todo lo demás ya viene incluido con Python! 🎉

---

## 🔧 Requisitos del Sistema

### Python
- **Versión mínima:** Python 3.8
- **Recomendado:** Python 3.11 o 3.12
- **Compatible con:** Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

### MySQL
- **Versión mínima:** MySQL 8.0
- **Alternativa:** MariaDB 10.5+
- **Estado:** Debe estar instalado y ejecutándose

### Sistema Operativo
- ✅ **Windows:** 10, 11
- ✅ **Linux:** Ubuntu 20.04+, Fedora, Debian, Arch
- ✅ **macOS:** 10.15 (Catalina) o superior

---

## 📦 Dependencias Requeridas (2)

### 1. mysql-connector-python
**Propósito:** Conectar Python con MySQL

```bash
pip install mysql-connector-python>=8.0.33
```

**Uso en el proyecto:**
- Conexión a la base de datos
- Ejecución de consultas SQL
- Transacciones
- Manejo de errores de BD

**Archivos que lo usan:**
- `database/connection.py`
- Todos los modelos (`models/*.py`)
- Scripts de migración

---

### 2. Pillow (PIL)
**Propósito:** Procesar y mostrar imágenes

```bash
pip install Pillow>=10.0.0
```

**Uso en el proyecto:**
- Cargar logos de empresa
- Mostrar avatares de usuarios
- Redimensionar imágenes
- Convertir formatos de imagen

**Archivos que lo usan:**
- `views/login_view.py` (logo en pantalla de login)
- `views/dashboard_view.py` (avatares y logos)
- `assets/logo_utils.py` (procesamiento de imágenes)

---

## 🐍 Librerías Estándar de Python (Incluidas)

Estas librerías **ya vienen con Python** y NO necesitas instalarlas:

### Interfaz Gráfica
```python
import tkinter as tk          # GUI principal
from tkinter import ttk        # Widgets modernos
from tkinter import messagebox # Diálogos
from tkinter import filedialog # Selección de archivos
```

### Seguridad
```python
import hashlib  # SHA256 para contraseñas
```

### Datos
```python
import json     # Configuraciones JSON
import decimal  # Aritmética precisa para dinero
```

### Fechas y Tiempo
```python
from datetime import datetime, timedelta
```

### Sistema
```python
import os       # Rutas, archivos, directorios
import sys      # Argumentos, paths, exit
import logging  # Sistema de logs
import pathlib  # Rutas modernas
import platform # Info del sistema
```

### Tipado
```python
from typing import Dict, List, Optional, Any, Tuple
```

---

## 📥 Instalación Completa

### Opción 1: Instalación Automática (Recomendada)

```bash
# Navegar a la carpeta del proyecto
cd C:\Users\USER\Desktop\POS

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Opción 2: Instalación Manual

```bash
# Instalar dependencias una por una
pip install mysql-connector-python>=8.0.33
pip install Pillow>=10.0.0
```

### Opción 3: Con Entorno Virtual (Recomendada para producción)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## ✅ Verificar Instalación

### Script de Verificación Completo

```python
# Guardar como: verificar_dependencias.py

import sys

print("=" * 70)
print("🔍 VERIFICACIÓN DE DEPENDENCIAS - SISTEMA POS")
print("=" * 70)

# Verificar Python
print(f"\n✅ Python {sys.version.split()[0]} instalado")
if sys.version_info < (3, 8):
    print("   ⚠️ ADVERTENCIA: Se requiere Python 3.8 o superior")

# Verificar dependencias
dependencias = {
    'mysql.connector': 'mysql-connector-python',
    'PIL': 'Pillow',
    'tkinter': 'tkinter (Python estándar)',
}

print("\n📦 Dependencias:")
for modulo, nombre in dependencias.items():
    try:
        __import__(modulo)
        print(f"   ✅ {nombre}")
    except ImportError:
        print(f"   ❌ {nombre} - NO INSTALADO")
        if modulo != 'tkinter':
            print(f"      Instalar con: pip install {nombre.split()[0]}")

# Verificar librerías estándar
print("\n🐍 Librerías estándar:")
estandar = ['json', 'datetime', 'logging', 'os', 'hashlib', 'decimal']
for lib in estandar:
    try:
        __import__(lib)
        print(f"   ✅ {lib}")
    except:
        print(f"   ❌ {lib}")

print("\n" + "=" * 70)
print("✅ Verificación completada")
print("=" * 70)
```

**Ejecutar:**
```bash
python verificar_dependencias.py
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'tkinter'"

**Windows:**
- Tkinter debería venir con Python
- Reinstalar Python desde python.org, marcando "tcl/tk and IDLE"

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

**Linux (Arch):**
```bash
sudo pacman -S tk
```

**macOS:**
```bash
# Instalar Python desde python.org (ya incluye tkinter)
# O con Homebrew:
brew install python-tk
```

---

### Error: "No module named 'mysql.connector'"

```bash
# Desinstalar si existe versión incorrecta
pip uninstall mysql-connector-python mysql-connector

# Instalar versión correcta
pip install mysql-connector-python
```

---

### Error: "PIL cannot import Image"

**Windows:**
```bash
pip uninstall Pillow
pip install Pillow --upgrade
```

**Linux:**
```bash
# Instalar dependencias del sistema
sudo apt-get install libjpeg-dev zlib1g-dev

# Reinstalar Pillow
pip uninstall Pillow
pip install Pillow
```

**macOS:**
```bash
brew install jpeg
pip install Pillow --upgrade
```

---

### Error: "Can't connect to MySQL server"

**Verificar que MySQL está ejecutándose:**

**Windows:**
```bash
net start MySQL80
```

**Linux:**
```bash
sudo systemctl start mysql
sudo systemctl status mysql
```

**macOS:**
```bash
brew services start mysql
```

---

## 🔒 Dependencias de Seguridad

### Actualizar Dependencias

```bash
# Ver versiones actuales
pip list

# Actualizar todas
pip install --upgrade mysql-connector-python Pillow

# Verificar vulnerabilidades conocidas
pip check
```

### Versiones Recomendadas (Octubre 2025)

```
mysql-connector-python==8.0.35
Pillow==10.1.0
```

---

## 📊 Dependencias Opcionales

### Para Generación de Códigos de Barras

```bash
pip install python-barcode[images]
```

**Uso:** Generar códigos de barras para productos

---

### Para Reportes PDF

```bash
pip install reportlab
```

**Uso:** Generar facturas y reportes en PDF

---

### Para Exportar a Excel

```bash
pip install openpyxl pandas
```

**Uso:** Exportar inventario y reportes a Excel

---

### Para Windows (Funcionalidades Avanzadas)

```bash
pip install pywin32
```

**Uso:** Integración profunda con Windows (impresoras, etc.)

---

## 🌍 Entornos de Desarrollo vs Producción

### Desarrollo
```bash
# requirements-dev.txt
mysql-connector-python>=8.0.33
Pillow>=10.0.0
pytest>=7.0.0              # Testing
black>=23.0.0              # Formateo de código
pylint>=2.17.0             # Linting
```

### Producción
```bash
# requirements.txt
mysql-connector-python==8.0.35
Pillow==10.1.0
```

---

## 📝 Archivo requirements.txt Completo

```txt
# =============================================================================
# DEPENDENCIAS DEL SISTEMA POS
# =============================================================================

# Base de datos MySQL
mysql-connector-python>=8.0.33

# Manejo de imágenes
Pillow>=10.0.0

# ─────────────────────────────────────────────────────────────────────────────
# OPCIONALES (descomentar si necesitas)
# ─────────────────────────────────────────────────────────────────────────────

# Códigos de barras
# python-barcode[images]>=0.15.1

# Reportes PDF
# reportlab>=4.0.0

# Excel
# openpyxl>=3.1.0
# pandas>=2.0.0

# Windows
# pywin32>=306
```

---

## 🚀 Guía de Instalación para Nuevos Desarrolladores

### Paso 1: Verificar Python
```bash
python --version
# Debería mostrar 3.8 o superior
```

### Paso 2: Clonar/Descargar Proyecto
```bash
cd C:\Users\USER\Desktop
# Asumiendo que ya tienes la carpeta POS
```

### Paso 3: Crear Entorno Virtual (Opcional pero Recomendado)
```bash
cd POS
python -m venv venv
venv\Scripts\activate  # Windows
```

### Paso 4: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 5: Verificar Instalación
```bash
python verificar_dependencias.py
```

### Paso 6: Configurar Base de Datos
```bash
# Ver archivo database/INSTALACION_RAPIDA.md
```

### Paso 7: Ejecutar Aplicación
```bash
python main.py
```

---

## 📈 Tamaño de Instalación

### Espacio en Disco
```
Python 3.12:               ~100 MB
mysql-connector-python:    ~10 MB
Pillow:                    ~5 MB
Entorno virtual (venv):    ~20 MB
Total aproximado:          ~135 MB
```

### Memoria RAM
```
Aplicación en ejecución:   ~50-80 MB
MySQL Server:              ~200-400 MB
Total aproximado:          ~250-500 MB
```

---

## 🔄 Actualización de Dependencias

### Ver Versiones Instaladas
```bash
pip list
```

### Actualizar Todo
```bash
pip install --upgrade -r requirements.txt
```

### Actualizar Individual
```bash
pip install --upgrade mysql-connector-python
pip install --upgrade Pillow
```

### Congelar Versiones (para producción)
```bash
pip freeze > requirements-lock.txt
```

---

## ✨ Resumen Final

### ✅ Dependencias Requeridas (2)
1. **mysql-connector-python** → Base de datos
2. **Pillow** → Imágenes

### ✅ Instalación Rápida
```bash
pip install mysql-connector-python Pillow
```

### ✅ Con requirements.txt
```bash
pip install -r requirements.txt
```

### ✅ Verificación
```bash
python
>>> import mysql.connector
>>> import PIL
>>> import tkinter
# Si no hay errores, ¡estás listo! 🎉
```

---

## 📞 Soporte

Si tienes problemas con las dependencias:

1. ✅ Verifica la versión de Python (`python --version`)
2. ✅ Actualiza pip (`pip install --upgrade pip`)
3. ✅ Lee la sección de "Solución de Problemas"
4. ✅ Ejecuta `verificar_dependencias.py`

---

**¡Tu Sistema POS está listo para instalarse!** 🚀

*Última actualización: 19 de Octubre 2025*
