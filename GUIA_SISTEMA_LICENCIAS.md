# 🔐 GUÍA COMPLETA: SISTEMA DE LICENCIAS

## 📋 Índice
1. [Introducción](#introducción)
2. [Generación de Licencias](#generación-de-licencias)
3. [Distribución de Licencias](#distribución-de-licencias)
4. [Integración en la Aplicación](#integración-en-la-aplicación)
5. [Validación de Licencias](#validación-de-licencias)
6. [Gestión y Control](#gestión-y-control)

---

## 🎯 Introducción

El Sistema POS ahora incluye un **sistema completo de licencias** que te permite:

✅ Generar licencias únicas para cada cliente
✅ Controlar quién puede instalar tu software
✅ Validar automáticamente las licencias durante la instalación
✅ Gestionar y rastrear licencias distribuidas

### 📦 Archivos del Sistema de Licencias:

```
POS/
├── generar_licencias.py          ← Generador de licencias
├── generar_licencias.bat         ← Script automático
├── validar_licencia.py           ← Validador standalone
└── utils/
    └── license_manager.py        ← Módulo para la aplicación
```

---

## 🔨 Generación de Licencias

### Opción A: Script Automático (Recomendado)

```batch
generar_licencias.bat
```

Luego sigue las instrucciones:
1. Cantidad de licencias (ej: 200)
2. Tipo de licencia (Standard/Premium/Enterprise)
3. Prefijo para clientes (ej: "Cliente")

**Nota:** Las licencias son PERMANENTES (de por vida), no expiran.

### Opción B: Script Python Directo

```powershell
python generar_licencias.py
```

### 📊 Resultado de la Generación:

Se crearán 4 tipos de archivos:

#### 1. `licenses_database.json` - Base de Datos Completa
```json
{
  "generated_date": "2025-11-02T...",
  "total_licenses": 200,
  "licenses": [
    {
      "license_number": 1,
      "license_key": "A1B2-C3D4-E5F6-G7H8",
      "activation_code": "1234-5678-90AB-CDEF-...",
      "customer_name": "Cliente0001",
      "license_type": "standard",
      "issue_date": "2025-11-02",
      "expiry_date": "PERMANENTE",
      "validity": "LIFETIME",
      "status": "active"
    }
  ]
}
```

#### 2. `licenses_list.csv` - Lista en Excel
Formato CSV que puedes abrir en Excel para control y seguimiento:
- License Number
- License Key
- Activation Code
- Customer Name
- Type
- Dates
- Status

#### 3. `LICENCIAS_MAESTRAS.txt` - Lista Maestra
**⚠️ CONFIDENCIAL - SOLO PARA TI**

Archivo de texto con todas las licencias en formato legible.
Incluye todas las claves y códigos de activación.

#### 4. `licenses_individual/` - Archivos Individuales
Una carpeta con 200 archivos (uno por licencia):
```
licenses_individual/
├── LICENSE_Cliente0001.txt
├── LICENSE_Cliente0002.txt
├── LICENSE_Cliente0003.txt
...
└── LICENSE_Cliente0200.txt
```

Cada archivo contiene:
```
╔════════════════════════════════════════╗
║     LICENCIA DE SOFTWARE - SISTEMA POS ║
╚════════════════════════════════════════╝

CLAVE DE LICENCIA:
A1B2-C3D4-E5F6-G7H8

CÓDIGO DE ACTIVACIÓN:
1234-5678-90AB-CDEF-1234-5678-90AB-CDEF

VALIDEZ:
Fecha de Emisión:   2025-11-02
Fecha de Expiración: PERMANENTE
Vigencia:           LIFETIME (De por vida)
```

---

## 📤 Distribución de Licencias

### Para Clientes Individuales:

1. **Entregar archivo individual:**
   ```
   licenses_individual/LICENSE_ClienteXXXX.txt
   ```

2. **Enviar por correo:**
   ```
   Asunto: Licencia Sistema POS - Cliente XXXX
   
   Adjunto: LICENSE_Cliente0001.txt
   
   Estimado cliente,
   
   Adjunto encontrará su licencia para el Sistema POS.
   
   Instrucciones:
   1. Ejecutar POS_Setup.exe
   2. Ingresar la clave de licencia cuando se solicite
   3. Ingresar el código de activación
   
   Soporte: soporte@tuempresa.com
   ```

3. **Incluir en USB/CD:**
   - Copiar archivo de licencia junto al instalador

### Control de Distribución:

**Usar `licenses_list.csv` para llevar registro:**

| # | Licencia | Cliente | Fecha Entrega | Estado |
|---|----------|---------|---------------|--------|
| 1 | A1B2-... | Juan Pérez | 2025-11-05 | Entregado |
| 2 | C3D4-... | María López | 2025-11-06 | Entregado |

---

## 🔗 Integración en la Aplicación

### Paso 1: Verificar Licencia al Iniciar

Editar `main.py`:

```python
from utils.license_manager import check_license_on_startup

def main():
    # ... código existente ...
    
    # Verificar licencia ANTES de mostrar ventana principal
    if not check_license_on_startup():
        return  # Salir si no hay licencia válida
    
    # Continuar con la aplicación normal
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
```

### Paso 2: Menú de Licencia (Opcional)

Agregar opción en el menú de configuración:

```python
from utils.license_manager import LicenseManager

def show_license_info():
    manager = LicenseManager()
    license_info = manager.get_license_info()
    
    if license_info:
        message = f"""
        Licencia: {license_info['license_key']}
        Activada: {license_info['activation_date'][:10]}
        Estado: {license_info['status'].upper()}
        """
        messagebox.showinfo("Información de Licencia", message)
    else:
        messagebox.showwarning("Sin Licencia", "No hay licencia activada")
```

---

## ✅ Validación de Licencias

### Validación Manual (Para Soporte):

```powershell
python validar_licencia.py
```

Luego ingresar:
- Clave de licencia
- Código de activación

El script validará y mostrará si es correcta.

### Validación Programática:

```python
from utils.license_manager import LicenseManager

manager = LicenseManager()

# Verificar si está activada
if manager.is_activated():
    print("✅ Licencia válida")
else:
    print("❌ No hay licencia")

# Validar nueva licencia
success, message = manager.activate(
    "A1B2-C3D4-E5F6-G7H8",
    "1234-5678-90AB-CDEF-1234-5678-90AB-CDEF"
)
```

---

## 📊 Gestión y Control

### Base de Datos de Licencias

**`licenses_database.json`** contiene todas las licencias generadas.

**IMPORTANTE:** 
- ⚠️ NO incluir este archivo en el instalador
- ⚠️ NO distribuir a clientes
- ✅ Guardar en lugar seguro con respaldo
- ✅ Usar solo para consultas internas

### Búsqueda de Licencia:

```python
import json

with open('licenses_database.json', 'r') as f:
    data = json.load(f)

# Buscar por clave
license_key = "A1B2-C3D4-E5F6-G7H8"

for lic in data['licenses']:
    if lic['license_key'] == license_key:
        print(f"Cliente: {lic['customer_name']}")
        print(f"Tipo: {lic['license_type']}")
        print(f"Expira: {lic['expiry_date']}")
        break
```

### Marcar Licencia como Usada:

```python
import json

def mark_license_as_used(license_key, customer_info):
    with open('licenses_database.json', 'r') as f:
        data = json.load(f)
    
    for lic in data['licenses']:
        if lic['license_key'] == license_key:
            lic['customer_name'] = customer_info
            lic['activation_date'] = datetime.now().isoformat()
            break
    
    with open('licenses_database.json', 'w') as f:
        json.dump(data, f, indent=2)
```

---

## 🔒 Seguridad

### Clave Secreta

El sistema usa una clave secreta para generar códigos de activación:
```python
SECRET_KEY = "POS_SISTEMA_2025_SECRET"
```

**IMPORTANTE:**
- ⚠️ Cambiar esta clave antes de distribuir
- ⚠️ Usar la MISMA clave en:
  - `generar_licencias.py`
  - `validar_licencia.py`
  - `utils/license_manager.py`

### Cambiar la Clave Secreta:

1. Editar `generar_licencias.py` línea ~13:
   ```python
   def __init__(self, secret_key="TU_CLAVE_SUPER_SECRETA_2025"):
   ```

2. Editar `validar_licencia.py` línea ~12:
   ```python
   def __init__(self, secret_key="TU_CLAVE_SUPER_SECRETA_2025"):
   ```

3. Editar `utils/license_manager.py` línea ~17:
   ```python
   self.secret_key = "TU_CLAVE_SUPER_SECRETA_2025"
   ```

---

## 📝 Tipos de Licencia

Puedes usar diferentes tipos según el cliente:

### Standard
- Licencia básica
- Todas las funciones principales
- Soporte estándar

### Premium
- Funciones adicionales
- Soporte prioritario
- Actualizaciones incluidas

### Enterprise
- Licencia corporativa
- Funciones completas
- Soporte 24/7
- Instalación asistida

---

## 🛠️ Solución de Problemas

### ❌ "Código de activación inválido"
**Causa:** Clave secreta diferente entre generador y validador

**Solución:** Verificar que SECRET_KEY sea idéntica en todos los archivos

### ❌ "Licencia no encontrada"
**Causa:** Archivo `licenses_database.json` no existe

**Solución:** Generar licencias nuevamente

### ❌ "Formato inválido"
**Causa:** Espacios extra o guiones mal colocados

**Solución:** Copiar clave exactamente como aparece (con guiones)

---

## 📞 Soporte

Para personalización o dudas:
- Revisar código fuente con comentarios
- Documentación en cada archivo
- Pruebas con `validar_licencia.py`

---

## ✨ Resumen de Comandos

```powershell
# Generar 200 licencias
generar_licencias.bat

# Validar manualmente
python validar_licencia.py

# Probar diálogo de activación
python utils/license_manager.py
```

---

**¡Sistema de licencias listo para usar! 🎉**

*Última actualización: Noviembre 2025*
