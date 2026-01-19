# ✅ ACTUALIZACIÓN: LICENCIAS PERMANENTES

## 🎯 Cambios Realizados

Se ha actualizado el **Sistema de Licencias** para que todas las licencias sean **PERMANENTES (de por vida)**, eliminando la fecha de expiración.

---

## 📝 Archivos Modificados

### 1. **`generar_licencias.py`**
- ✅ Eliminada solicitud de "días de validez"
- ✅ Campo `expiry_date` ahora es `"PERMANENTE"`
- ✅ Campo `validity_days` reemplazado por `validity: "LIFETIME"`
- ✅ Mensajes actualizados para indicar licencias permanentes

### 2. **`validar_licencia.py`**
- ✅ Algoritmo hash actualizado (compatible con Inno Setup)
- ✅ Usa `simple_hash` en lugar de SHA256

### 3. **`utils/license_manager.py`**
- ✅ Algoritmo hash actualizado (compatible con Inno Setup)
- ✅ Usa `simple_hash` en lugar de SHA256

### 4. **`GUIA_SISTEMA_LICENCIAS.md`**
- ✅ Documentación actualizada
- ✅ Ejemplos con `"PERMANENTE"` y `"LIFETIME"`

### 5. **`INICIO_RAPIDO_LICENCIAS.md`**
- ✅ Instrucciones actualizadas
- ✅ Ejemplos de licencias permanentes

---

## 🚀 Cómo Usar

### Generar 200 Licencias Permanentes:

```powershell
generar_licencias.bat
```

El sistema te preguntará:
- ✅ Cantidad: `200`
- ✅ Tipo: `1` (Standard)
- ✅ Prefijo: `Cliente`
- ❌ **YA NO pregunta días de validez** (todas son permanentes)

### Formato de Licencias Generadas:

```json
{
  "license_key": "A1B2-C3D4-E5F6-G7H8",
  "activation_code": "1234-5678-90AB-CDEF-...",
  "issue_date": "2025-11-02",
  "expiry_date": "PERMANENTE",
  "validity": "LIFETIME"
}
```

### Archivo Individual para Cliente:

```
VALIDEZ:
──────────────────────────────────────────
Fecha de Emisión:   2025-11-02
Fecha de Expiración: PERMANENTE
Vigencia:           LIFETIME
```

---

## 🧪 Probar el Sistema

### Opción 1: Prueba Rápida (5 licencias)
```powershell
PROBAR_LICENCIAS_PERMANENTES.bat
```

Este script:
- Genera 5 licencias de prueba
- Muestra el contenido de la primera
- Verifica que la expiración sea "PERMANENTE"

### Opción 2: Generar Producción (200 licencias)
```powershell
generar_licencias.bat
```

---

## 📊 Estructura de Archivos Generados

```
POS/
├── licenses_database.json          ← Base de datos JSON (200 licencias)
├── licenses_list.csv               ← Lista Excel (fácil de revisar)
├── LICENCIAS_MAESTRAS.txt          ← Lista completa (CONFIDENCIAL)
└── licenses_individual/            ← 200 archivos para distribuir
    ├── LICENSE_Cliente0001.txt
    ├── LICENSE_Cliente0002.txt
    ├── ...
    └── LICENSE_Cliente0200.txt
```

---

## 🔐 Validación en el Instalador

El **instalador (`installer_script.iss`)** ya está configurado para:

1. ✅ Solicitar licencia ANTES de instalar
2. ✅ Validar con algoritmo compatible
3. ✅ Guardar licencia en `config/license.json`
4. ✅ **NO verificar fecha de expiración** (son permanentes)

---

## 📋 Checklist de Distribución

### Antes de Distribuir:

- [ ] Generar 200 licencias con `generar_licencias.bat`
- [ ] Verificar archivos en `licenses_individual/`
- [ ] Compilar instalador con Inno Setup (`installer_script.iss`)
- [ ] Probar instalación con una licencia de prueba
- [ ] Verificar que no aparece fecha de expiración

### Entregar a Cada Cliente:

- [ ] Archivo: `LICENSE_ClienteXXXX.txt`
- [ ] Instalador: `POS_Setup.exe`
- [ ] Instrucciones: Email o documento

---

## 💾 Backup Importante

**Guarda en lugar SEGURO:**

```
✅ LICENCIAS_MAESTRAS.txt          ← Todas las licencias
✅ licenses_database.json          ← Base de datos completa
✅ generar_licencias.py            ← Generador (por si necesitas más)
```

**NO distribuyas estos archivos**, solo los individuales de `licenses_individual/`.

---

## 🎯 Ventajas de Licencias Permanentes

| Ventaja | Descripción |
|---------|-------------|
| ✅ **Sin renovaciones** | Clientes NO necesitan renovar anualmente |
| ✅ **Simplicidad** | No hay que gestionar expiraciones |
| ✅ **Satisfacción** | Clientes tienen acceso de por vida |
| ✅ **Menos soporte** | No hay tickets de "mi licencia expiró" |

---

## ⚠️ Si Necesitas Licencias con Expiración

Si en el futuro necesitas agregar expiraciones:

1. Modificar `generar_licencias.py` (línea ~80)
2. Agregar validación de fecha en `utils/license_manager.py`
3. Actualizar `installer_script.iss`

**Por ahora:** Todas las licencias son permanentes.

---

## 📞 Comandos Rápidos

```powershell
# Prueba rápida (5 licencias)
PROBAR_LICENCIAS_PERMANENTES.bat

# Generar producción (200 licencias)
generar_licencias.bat

# Validar manualmente una licencia
python validar_licencia.py

# Ver licencia activada en la app
notepad config\license.json
```

---

## ✅ Resumen

- 🔑 **Licencias:** PERMANENTES (no expiran)
- 📦 **Formato:** Igual (XXXX-XXXX-XXXX-XXXX)
- 🔐 **Validación:** En el instalador (bloquea si inválida)
- 📁 **Distribución:** Un archivo por cliente
- 💾 **Control:** Lista maestra + Excel

---

**¡Sistema de licencias permanentes listo! 🚀**

Siguiente paso: Ejecutar `PROBAR_LICENCIAS_PERMANENTES.bat` para verificar.
