# 🚀 CREACIÓN DEL INSTALADOR - GUÍA RÁPIDA

## ✅ Pasos Rápidos (5 minutos)

### 1️⃣ Verificar Sistema
```powershell
python verificar_instalador.py
```
Este comando verifica que todo esté listo.

### 2️⃣ Crear Ejecutable
```powershell
crear_instalador.bat
```
O manualmente:
```powershell
python build_installer.py
```

### 3️⃣ Crear Instalador
- Descargar e instalar **Inno Setup**: https://jrsoftware.org/isdl.php
- Abrir `installer_script.iss` con Inno Setup
- Click en **Build > Compile** (o F9)
- El instalador se creará en `Output\POS_Setup.exe`

### 4️⃣ ¡Listo!
El archivo `Output\POS_Setup.exe` ya puede ser distribuido.

---

## 📋 Requisitos

### En tu PC (para crear el instalador):
- ✅ Windows 10/11
- ✅ Python 3.8+
- ✅ PyInstaller: `pip install pyinstaller`
- ✅ Inno Setup 6.2+

### En la PC donde se instalará:
- ✅ Windows 10/11 (64 bits)
- ✅ MySQL Server 8.0+
- ✅ 4 GB RAM
- ✅ 500 MB espacio en disco

---

## 🛠️ Scripts Incluidos

| Script | Descripción |
|--------|-------------|
| `verificar_instalador.py` | Verifica requisitos antes de compilar |
| `build_installer.py` | Crea el ejecutable con PyInstaller |
| `crear_instalador.bat` | Proceso automático completo |
| `installer_script.iss` | Script de Inno Setup (instalador) |

---

## 📦 Qué se incluye en el instalador

```
POS_Setup.exe
├── Ejecutable principal (POS_Sistema.exe)
├── Dependencias de Python
├── Assets (imágenes, iconos)
├── Scripts SQL (base de datos)
├── Configuración (plantillas)
├── Documentación
└── Desinstalador
```

---

## 🔧 Personalización

### Cambiar información del instalador:
Editar `installer_script.iss`:

```ini
#define MyAppName "Tu Nombre de App"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Tu Empresa S.A."
#define MyAppURL "https://www.tuempresa.com"
```

### Cambiar icono:
1. Crear archivo `icon.ico` (256x256 px)
2. Guardar en `assets/images/icon.ico`
3. Recompilar

---

## 📤 Distribución

### Tamaño aproximado:
- Ejecutable: ~80-120 MB
- Instalador: ~90-140 MB (comprimido)

### Opciones de distribución:
1. **USB/Disco externo** ✅ Más común
2. **Google Drive/OneDrive** ✅ Para descargas
3. **CD/DVD** ✅ Para clientes corporativos
4. **Servidor web** ✅ Para actualizaciones

---

## ❓ Preguntas Frecuentes

### ¿El instalador funciona sin internet?
✅ Sí, todo está incluido excepto MySQL Server.

### ¿Necesito Python en la PC destino?
❌ No, el ejecutable incluye Python.

### ¿La base de datos se instala automáticamente?
❌ No, MySQL debe instalarse manualmente. Los scripts SQL están incluidos.

### ¿Puedo actualizar la aplicación?
✅ Sí, crear nuevo instalador y ejecutar sobre la instalación anterior.

### ¿Cómo desinstalar?
Panel de Control > Programas > Sistema POS > Desinstalar

---

## 🆘 Problemas Comunes

### ❌ "PyInstaller no es un comando reconocido"
```powershell
pip install pyinstaller
```

### ❌ "Error: No module named 'XXX'"
```powershell
pip install -r requirements.txt
```

### ❌ Instalador muy grande (>300 MB)
- Usar entorno virtual limpio
- Revisar dependencias innecesarias

### ❌ Antivirus bloquea el .exe
- Normal con ejecutables nuevos
- Agregar excepción en Windows Defender

---

## 📞 Soporte

Para más ayuda, revisar:
- 📖 `GUIA_INSTALADOR.md` - Guía completa detallada
- 📄 `INSTRUCCIONES_INSTALACION.txt` - Para usuarios finales

---

## ✨ Tips Profesionales

1. **Probar siempre** en una PC limpia antes de distribuir
2. **Actualizar versión** en `installer_script.iss` cada vez
3. **Incluir documentación** clara para usuarios finales
4. **Mantener backups** de cada versión del instalador
5. **Firmar digitalmente** el .exe para evitar warnings (avanzado)

---

**¡Listo para distribuir tu Sistema POS profesionalmente! 🎉**
