# ⚡ COMANDOS RÁPIDOS - CREAR INSTALADOR

## 🎯 Para crear el instalador completo (5 minutos):

```powershell
# Opción 1: Script automático (RECOMENDADO)
.\crear_instalador.bat

# Opción 2: Paso a paso manual
python verificar_instalador.py      # Verificar
python build_installer.py           # Compilar
# Luego abrir Inno Setup y compilar installer_script.iss
```

---

## 📋 Comandos individuales:

```powershell
# Verificar sistema antes de compilar
python verificar_instalador.py

# Crear ejecutable con PyInstaller
python build_installer.py

# Limpiar builds anteriores
Remove-Item -Recurse -Force build, dist
Remove-Item *.spec

# Instalar PyInstaller (si falta)
pip install pyinstaller

# Probar el ejecutable generado
.\dist\POS_Sistema\POS_Sistema.exe

# Abrir carpeta de salida
explorer .\dist\POS_Sistema

# Abrir carpeta del instalador final
explorer .\Output
```

---

## 🔧 Inno Setup (línea de comandos):

```powershell
# Compilar instalador desde PowerShell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss

# Si Inno Setup está en Program Files (no x86)
& "C:\Program Files\Inno Setup 6\ISCC.exe" installer_script.iss
```

---

## 🧹 Limpiar todo:

```powershell
# Eliminar compilaciones anteriores
Remove-Item -Recurse -Force build, dist, Output
Remove-Item *.spec
Remove-Item version_file.txt -ErrorAction SilentlyContinue
```

---

## 🚀 Comando TODO-EN-UNO:

```powershell
# Limpiar, verificar, compilar ejecutable
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue; `
python verificar_instalador.py; `
python build_installer.py
```

---

## 📦 Distribución:

```powershell
# Crear ZIP portable (sin instalador)
Compress-Archive -Path .\dist\POS_Sistema\* -DestinationPath POS_Portable.zip -Force

# Copiar instalador a otra ubicación
Copy-Item .\Output\POS_Setup.exe -Destination D:\Distribución\
```

---

## 🔍 Diagnóstico:

```powershell
# Ver versión de Python
python --version

# Ver versión de PyInstaller
pyinstaller --version

# Listar dependencias instaladas
pip list | Select-String "mysql|openpyxl|reportlab|Pillow|pyinstaller"

# Ver tamaño de archivos
Get-ChildItem .\dist\POS_Sistema -Recurse | Measure-Object -Property Length -Sum

# Ver tamaño del instalador
Get-ChildItem .\Output\*.exe | Format-Table Name, @{Label="Size (MB)"; Expression={"{0:N2}" -f ($_.Length / 1MB)}}
```

---

## 🎓 Personalización:

```powershell
# Editar configuración del instalador
notepad installer_script.iss

# Editar script de compilación
notepad build_installer.py

# Ver logs de compilación
Get-Content .\build\POS_Sistema\warn-POS_Sistema.txt -Tail 50
```

---

## 💾 Backup:

```powershell
# Crear backup del proyecto completo
$date = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path ..\POS -DestinationPath "..\POS_Backup_$date.zip"
```

---

## 🔄 Actualizar versión:

```powershell
# Editar número de versión en installer_script.iss
# Línea 5: #define MyAppVersion "1.0.0"
(Get-Content installer_script.iss) -replace '#define MyAppVersion "1.0.0"', '#define MyAppVersion "1.1.0"' | Set-Content installer_script.iss
```

---

## 🎯 Proceso Completo Automatizado:

```powershell
# Script completo en una línea
Write-Host "🚀 Iniciando proceso completo..." -ForegroundColor Green; `
Remove-Item -Recurse -Force build, dist, Output -ErrorAction SilentlyContinue; `
python verificar_instalador.py; `
if ($LASTEXITCODE -eq 0) { `
    python build_installer.py; `
    if ($LASTEXITCODE -eq 0) { `
        if (Test-Path "C:\Program Files (x86)\Inno Setup 6\ISCC.exe") { `
            & "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss; `
        } `
    } `
}; `
if (Test-Path .\Output\POS_Setup.exe) { `
    Write-Host "✅ Instalador creado exitosamente!" -ForegroundColor Green; `
    explorer .\Output `
} else { `
    Write-Host "❌ Error al crear instalador" -ForegroundColor Red `
}
```

---

## 📝 Notas:

- Todos los comandos deben ejecutarse desde la carpeta raíz del proyecto
- Usar PowerShell (no CMD)
- La primera compilación toma más tiempo (~10 min)
- Compilaciones posteriores son más rápidas (~5 min)

---

**¡Guarda este archivo para referencia rápida! 📌**
