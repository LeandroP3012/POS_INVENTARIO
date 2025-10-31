# 🖨️ Integración de Detección de Impresoras para Códigos de Barras

## 📋 Resumen de la Implementación

Se ha integrado la detección automática de tipo de impresora en el módulo de **Gestión de Productos** para imprimir códigos de barras, siguiendo la misma lógica que el módulo de **Ventas**.

---

## 🎯 Funcionalidades Implementadas

### ✅ 1. Detección Automática de Impresora
- Lee la configuración desde `config/system_config.json`
- Detecta si la impresora es **térmica** o **estándar**
- Palabras clave para detección térmica: `thermal`, `térmica`, `termica`, `tp-`, `tm-`, `pos`, `esc/pos`, `epson tm`

### ✅ 2. Impresión en Impresora Térmica
- Usa el módulo `utils.thermal_printer.ThermalPrinter`
- Formato optimizado para impresoras de 80mm
- Comandos ESC/POS nativos
- Corte automático de papel

### ✅ 3. Impresión en Impresora Estándar
- Compatible con impresoras Windows (PDF, Láser, Inkjet)
- Usa `win32print` y `win32ui`
- Centrado automático en la página
- Escalado inteligente

### ✅ 4. Fallback Automático
- Si falla impresión térmica → cambia a estándar
- Si no hay impresora configurada → usa predeterminada del sistema
- Mensajes informativos en cada paso

---

## 📁 Archivos Modificados

### 1. `views/product_form_dialog.py`
**Método:** `print_barcode()`

**Cambios principales:**
```python
# DETECCIÓN DE TIPO DE IMPRESORA
printer_name = None
is_thermal = False

# Leer configuración
config_path = os.path.join('config', 'system_config.json')
system_config = json.load(open(config_path))
printer_name = system_config.get('printer')

# Detectar si es térmica
thermal_keywords = ['thermal', 'térmica', 'termica', 'tp-', 'tm-', 'pos', 'esc/pos', 'epson tm']
is_thermal = any(keyword in printer_name.lower() for keyword in thermal_keywords)

# IMPRESIÓN TÉRMICA
if is_thermal:
    thermal = ThermalPrinter(printer_name)
    success = thermal.print_barcode_image(new_img, name, sku)
    
# IMPRESIÓN ESTÁNDAR
else:
    # Usar win32print...
```

### 2. `utils/thermal_printer.py`
**Nuevo método:** `print_barcode_image(barcode_image, product_name, sku)`

**Funcionalidad:**
```python
def print_barcode_image(self, barcode_image, product_name: str, sku: str) -> bool:
    """
    Imprimir imagen de código de barras en impresora térmica
    
    - Formatea nombre del producto (máx 32 caracteres)
    - Imprime SKU
    - Usa comandos ESC/POS para formato
    - Corta papel automáticamente
    """
```

---

## 🔧 Configuración en `system_config.json`

```json
{
  "printer": "TP-300 Thermal Printer",
  "auto_print": true,
  ...
}
```

**Tipos de impresora detectados:**

| Tipo | Nombre contiene | Método usado |
|------|----------------|--------------|
| **Térmica** | `thermal`, `térmica`, `tp-`, `tm-`, `pos`, `esc/pos` | `ThermalPrinter.print_barcode_image()` |
| **Estándar** | `PDF`, `HP`, `Canon`, etc. | `win32print` + `win32ui` |

---

## 🚀 Flujo de Impresión

```
┌─────────────────────────────────────┐
│ Usuario presiona "🖨️ Imprimir"      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Generar imagen código de barras     │
│ (EAN13 con nombre del producto)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Leer system_config.json              │
│ Obtener nombre de impresora          │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────┴──────┐
        │ ¿Térmica?   │
        └──────┬──────┘
               │
       ┌───────┴───────┐
       │               │
      Sí              No
       │               │
       ▼               ▼
  ┌─────────┐    ┌─────────┐
  │ Térmica │    │Estándar │
  │ ESC/POS │    │win32ui  │
  └────┬────┘    └────┬────┘
       │              │
       └──────┬───────┘
              ▼
    ┌──────────────────┐
    │ ✅ Impreso       │
    └──────────────────┘
```

---

## 📊 Mensajes en Consola

### Impresión Térmica Exitosa:
```
🖨️ Impresora configurada: TP-300 Thermal Printer
   ✓ Detectada como impresora TÉRMICA
🖨️ Usando módulo de impresión térmica para código de barras...
🖨️ Imprimiendo código de barras en impresora térmica...
   Producto: Cuaderno Universitario
   SKU: PROD-003
   ✅ Código de barras enviado exitosamente
   ✅ Código de barras enviado a impresora térmica
```

### Impresión Estándar:
```
🖨️ Impresora configurada: Microsoft Print to PDF
   ✓ Detectada como impresora ESTÁNDAR
🖨️ Impresoras disponibles: ['Microsoft Print to PDF', 'HP LaserJet']
🖨️ Iniciando impresión estándar en: Microsoft Print to PDF
```

### Fallback (Térmica → Estándar):
```
🖨️ Impresora configurada: TP-300 Thermal Printer
   ✓ Detectada como impresora TÉRMICA
🖨️ Usando módulo de impresión térmica para código de barras...
   ❌ Error en impresión térmica: [error]
   🔄 Usando impresión estándar...
🖨️ Iniciando impresión estándar en: Microsoft Print to PDF
```

---

## 🧪 Pruebas

### Caso 1: Impresora Térmica (TP-300)
1. Editar producto en módulo de Productos
2. Generar código de barras
3. Presionar "🖨️ Imprimir"
4. **Resultado:** Imprime en térmica con formato ESC/POS

### Caso 2: Impresora PDF
1. Configurar `"printer": "Microsoft Print to PDF"` en `system_config.json`
2. Editar producto
3. Generar código de barras
4. Presionar "🖨️ Imprimir"
5. **Resultado:** Imprime en PDF estándar

### Caso 3: Sin Impresora Configurada
1. Dejar `"printer": ""` en `system_config.json`
2. Generar código de barras
3. Presionar "🖨️ Imprimir"
4. **Resultado:** Usa impresora predeterminada del sistema

---

## ⚙️ Comandos ESC/POS Usados (Térmica)

| Comando | Función |
|---------|---------|
| `ESC @` | Inicializar impresora |
| `ESC a 1` | Alinear al centro |
| `ESC E 1` | Negrita ON |
| `ESC E 0` | Negrita OFF |
| `GS ! 0x11` | Texto doble (alto y ancho) |
| `GS V 66 0` | Corte parcial de papel |

---

## 🐛 Solución de Problemas

### Error: "Módulo thermal_printer no disponible"
**Solución:** El sistema automáticamente usa impresión estándar como fallback

### Error: "Impresora no encontrada"
**Solución:** 
1. Verificar nombre exacto en `system_config.json`
2. Sistema ofrece usar impresora predeterminada
3. Muestra lista de impresoras disponibles

### Error: "pyimage doesn't exist" (resuelto en dashboard)
**Solución aplicada:**
- Pre-cargar imágenes fuera de callbacks
- Usar `master=self.root` en PhotoImage
- Guardar referencia en `canvas.image`

---

## 📝 Notas Importantes

1. **Compatibilidad:** Funciona igual que el módulo de ventas
2. **Configuración centralizada:** Todo se lee desde `system_config.json`
3. **Sin intervención manual:** Detección automática de tipo de impresora
4. **Robusto:** Múltiples niveles de fallback
5. **Informativo:** Mensajes claros en cada paso

---

## 🎉 Estado Final

✅ **Completamente funcional**
✅ **Integrado con sistema de ventas**
✅ **Detección automática de tipo de impresora**
✅ **Fallback inteligente**
✅ **Mensajes informativos en consola**

---

**Fecha de implementación:** 31 de octubre de 2025  
**Módulos afectados:** Gestión de Productos, Impresión Térmica  
**Compatible con:** Windows, Python 3.13, Impresoras ESC/POS 80mm
