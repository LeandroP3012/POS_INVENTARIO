# ⚡ INICIO RÁPIDO: SISTEMA DE LICENCIAS

## 🎯 Crear 200 Licencias en 3 Pasos

### 1️⃣ Generar Licencias
```batch
generar_licencias.bat
```
- Cantidad: 200
- Tipo: Standard (opción 1)
- Prefijo: Cliente
- **Validez: PERMANENTE (de por vida)**

### 2️⃣ Archivos Generados
```
✅ licenses_individual/          ← Entregar a clientes
✅ licenses_list.csv             ← Control en Excel
✅ LICENCIAS_MAESTRAS.txt        ← Tu lista completa (CONFIDENCIAL)
✅ licenses_database.json        ← Base de datos (NO distribuir)
```

### 3️⃣ Distribuir a Clientes
Cada cliente recibe:
```
licenses_individual/LICENSE_ClienteXXXX.txt
```

Este archivo contiene:
- 🔑 Clave de Licencia: `XXXX-XXXX-XXXX-XXXX`
- 🔐 Código de Activación: `XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX`

---

## 📋 Ejemplo de Licencia Generada

```
╔════════════════════════════════════════╗
║   LICENCIA DE SOFTWARE - SISTEMA POS   ║
╚════════════════════════════════════════╝

Cliente: Cliente0001

CLAVE DE LICENCIA:
A1B2-C3D4-E5F6-G7H8

CÓDIGO DE ACTIVACIÓN:
1234-5678-90AB-CDEF-1234-5678-90AB-CDEF

VALIDEZ:
Fecha de Emisión:   2025-11-02
Fecha de Expiración: PERMANENTE
Vigencia: LIFETIME (De por vida)
```

---

## 🔗 Integrar en la Aplicación

### Editar `main.py` (1 línea):

```python
from utils.license_manager import check_license_on_startup

# Al inicio de tu aplicación, antes de mostrar la ventana:
if not check_license_on_startup():
    sys.exit()  # Salir si no hay licencia
```

**¡Eso es todo!** La aplicación ahora pedirá licencia en el primer inicio.

---

## 🧪 Probar el Sistema

### 1. Generar licencias de prueba:
```powershell
python generar_licencias.py
# Cantidad: 5 (para prueba)
```

### 2. Probar validación:
```powershell
python validar_licencia.py
# Copiar clave y código de un archivo LICENSE_ClienteXXXX.txt
```

### 3. Probar diálogo:
```powershell
python utils/license_manager.py
```

---

## 📊 Gestión de Licencias

### Ver licencias en Excel:
```
Abrir: licenses_list.csv
```

Columnas:
- License Number
- License Key  
- Activation Code
- Customer Name
- Type
- Issue Date
- Expiry Date

### Llevar control:
Agregar columnas:
- Cliente Real
- Fecha Entrega
- Email Cliente
- Estado (Entregada/Pendiente)

---

## 🎁 Cómo Entregar al Cliente

### Por Email:
```
Para: cliente@empresa.com
Asunto: Su Licencia - Sistema POS

Estimado cliente,

Adjunto encontrará su licencia para el Sistema POS.

Durante la instalación necesitará:
• Clave de Licencia (ver archivo adjunto)
• Código de Activación (ver archivo adjunto)

El sistema solicitará estos datos automáticamente.

Saludos,
Soporte Técnico
```

Adjuntar: `LICENSE_ClienteXXXX.txt`

### En USB junto al instalador:
```
USB:/
├── POS_Setup.exe
└── TU_LICENCIA.txt  (renombrar LICENSE_ClienteXXXX.txt)
```

---

## 🔐 Seguridad

### ⚠️ Archivos CONFIDENCIALES (solo para ti):
- ❌ `licenses_database.json`
- ❌ `LICENCIAS_MAESTRAS.txt`
- ❌ `generar_licencias.py`
- ❌ `validar_licencia.py`

### ✅ Archivos para distribuir:
- ✅ `licenses_individual/LICENSE_*.txt` (uno por cliente)
- ✅ `POS_Setup.exe` (instalador)

---

## ⚙️ Personalización

### Tipos de licencia disponibles:
1. **Standard** - Básica
2. **Premium** - Con extras
3. **Enterprise** - Completa

**Nota:** Todas las licencias son PERMANENTES (de por vida).

### Cambiar clave secreta (IMPORTANTE):
Buscar en 3 archivos:
1. `generar_licencias.py` → `secret_key="TU_CLAVE_AQUI"`
2. `validar_licencia.py` → `secret_key="TU_CLAVE_AQUI"`
3. `utils/license_manager.py` → `secret_key="TU_CLAVE_AQUI"`

**Debe ser la MISMA en los 3 archivos**

---

## 📞 Comandos Útiles

```powershell
# Generar licencias
generar_licencias.bat

# Validar manualmente
python validar_licencia.py

# Probar diálogo
python utils/license_manager.py

# Ver licencia activada
# (después de activar en la app)
notepad config/license.json
```

---

## ❓ Preguntas Frecuentes

### ¿Puedo generar más licencias después?
✅ Sí, ejecuta `generar_licencias.bat` nuevamente

### ¿Las licencias expiran?
✅ NO, son PERMANENTES (de por vida)

### ¿Puedo bloquear una licencia?
✅ Sí, edita `licenses_database.json` y cambia `"status": "revoked"`

### ¿Funcionan en cualquier PC?
✅ Sí, las licencias son universales (no atadas a hardware)

### ¿Se puede usar una licencia en varias PCs?
⚠️ Técnicamente sí, pero puedes modificar el código para limitarlo

---

## 🎯 Resumen

| Acción | Comando |
|--------|---------|
| Generar 200 licencias | `generar_licencias.bat` |
| Entregar a cliente | Enviar `LICENSE_ClienteXXXX.txt` |
| Integrar en app | Agregar 2 líneas en `main.py` |
| Validar manualmente | `python validar_licencia.py` |

---

**¡Sistema de licencias listo! 🚀**

📖 Para más detalles: `GUIA_SISTEMA_LICENCIAS.md`
