# ✅ Pruebas de Funcionalidades de Códigos de Barras

## Checklist de Pruebas

### 1️⃣ Auto-generación al Crear Producto Nuevo

**Pasos:**
1. Inicia sesión en el sistema
2. Ve a **Inventario** → **Gestionar Productos**
3. Haz clic en **➕ Nuevo Producto**
4. Verifica el formulario

**Resultado Esperado:**
- ✅ El campo **SKU** debe mostrar automáticamente: `PROD-000001` (o el siguiente número disponible)
- ✅ El campo **Código de Barras** debe mostrar un código de 13 dígitos (ej: `7750000010003`)
- ✅ Ambos campos se generan automáticamente al abrir el formulario

**Estado:** [ ] PASS / [ ] FAIL

---

### 2️⃣ Botón "🔄 Auto-generar" (SKU)

**Pasos:**
1. En el formulario de nuevo producto
2. Borra el contenido del campo SKU
3. Haz clic en el botón **🔄 Auto-generar** junto al campo SKU

**Resultado Esperado:**
- ✅ Debe aparecer un mensaje: "Se ha generado el SKU: PROD-XXXXXX"
- ✅ El campo SKU se llena automáticamente
- ✅ El campo Código de Barras también se actualiza automáticamente

**Estado:** [ ] PASS / [ ] FAIL

---

### 3️⃣ Botón "🔄 Generar" (Código de Barras)

**Pasos:**
1. Escribe manualmente un SKU (ej: `PROD-000999`)
2. Haz clic en el botón **🔄 Generar** junto al campo Código de Barras

**Resultado Esperado:**
- ✅ Debe aparecer un mensaje con el código generado
- ✅ El campo Código de Barras se actualiza con un código EAN-13 válido
- ✅ El código debe empezar con `775` (prefijo de Perú)

**Estado:** [ ] PASS / [ ] FAIL

---

### 4️⃣ Validación: SKU Vacío al Generar Código de Barras

**Pasos:**
1. Borra el campo SKU
2. Haz clic en **🔄 Generar** en el código de barras

**Resultado Esperado:**
- ✅ Debe aparecer advertencia: "Primero debes ingresar o generar un SKU..."
- ✅ No debe generar ningún código de barras

**Estado:** [ ] PASS / [ ] FAIL

---

### 5️⃣ Formato de SKU con Capacidad Ampliada

**Pasos:**
1. Verifica que los SKUs generados sigan el formato `PROD-XXXXXX`
2. Observa que tiene 6 dígitos (no 3)

**Resultado Esperado:**
- ✅ Formato: `PROD-000001`, `PROD-000002`, etc.
- ✅ Soporta hasta `PROD-999999` (999,999 productos)
- ✅ Los ceros a la izquierda se mantienen

**Estado:** [ ] PASS / [ ] FAIL

---

### 6️⃣ Botón "🖨️ Imprimir" - Sin Módulos Instalados

**Pasos:**
1. Haz clic en **🖨️ Imprimir** junto al código de barras
2. **NOTA:** Si no tienes los módulos instalados, verás un error

**Resultado Esperado:**
- ⚠️ Si no están instalados: Mensaje indicando instalar `python-barcode[images] Pillow pywin32`
- ✅ El mensaje debe ser claro e informativo

**Estado:** [ ] PASS / [ ] FAIL

---

### 7️⃣ Instalar Módulos de Impresión (OPCIONAL)

**Pasos:**
```bash
pip install python-barcode[images] Pillow pywin32
```

**Resultado Esperado:**
- ✅ Los módulos se instalan sin errores
- ✅ Reinicia la aplicación después de instalar

**Estado:** [ ] PASS / [ ] FAIL / [ ] SKIP

---

### 8️⃣ Botón "🖨️ Imprimir" - Con Módulos Instalados (OPCIONAL)

**Pasos:**
1. Asegúrate de tener impresora conectada
2. Genera un producto con código de barras
3. Haz clic en **🖨️ Imprimir**

**Resultado Esperado:**
- ✅ Se genera una etiqueta con:
  - Nombre del producto (arriba)
  - Código de barras visual
  - Número del código (abajo)
- ✅ Se envía a la impresora configurada
- ✅ Mensaje de confirmación: "Código de barras enviado a la impresora..."

**Estado:** [ ] PASS / [ ] FAIL / [ ] SKIP

---

### 9️⃣ Crear Producto Completo

**Pasos:**
1. Usa los valores auto-generados (SKU y código de barras)
2. Llena los demás campos:
   - Nombre: "Producto de Prueba"
   - Categoría: Selecciona una
   - Unidad: Selecciona una
   - Precio: 100.00
   - Costo: 50.00
3. Haz clic en **💾 Guardar**

**Resultado Esperado:**
- ✅ El producto se guarda correctamente
- ✅ El margen de ganancia se calcula (100%)
- ✅ El SKU y código de barras se guardan en la base de datos
- ✅ Mensaje: "Producto creado exitosamente"

**Estado:** [ ] PASS / [ ] FAIL

---

### 🔟 Editar Producto Existente

**Pasos:**
1. Ve a la lista de productos
2. Selecciona el producto que acabas de crear
3. Haz clic en **✏️ Editar**

**Resultado Esperado:**
- ✅ El formulario se abre con los datos del producto
- ✅ El SKU mantiene el formato `PROD-XXXXXX`
- ✅ El código de barras se mantiene igual
- ✅ Los botones de generación siguen funcionando

**Estado:** [ ] PASS / [ ] FAIL

---

### 1️⃣1️⃣ Secuencia de SKUs

**Pasos:**
1. Crea 3 productos nuevos consecutivos
2. Verifica los SKUs generados

**Resultado Esperado:**
- ✅ Producto 1: `PROD-000001`
- ✅ Producto 2: `PROD-000002`
- ✅ Producto 3: `PROD-000003`
- ✅ Los números son consecutivos sin saltos

**Estado:** [ ] PASS / [ ] FAIL

---

### 1️⃣2️⃣ Validación de Código de Barras EAN-13

**Pasos:**
1. Genera un código de barras
2. Verifica su estructura

**Resultado Esperado:**
- ✅ Tiene exactamente 13 dígitos
- ✅ Empieza con `775` (Perú)
- ✅ El último dígito es el verificador (calculado automáticamente)
- ✅ Ejemplo: `7750000010003`
  - `775` = País
  - `000001000` = Basado en SKU
  - `3` = Dígito verificador

**Estado:** [ ] PASS / [ ] FAIL

---

## 📊 Resumen de Pruebas

| # | Funcionalidad | Estado | Notas |
|---|---------------|--------|-------|
| 1 | Auto-generación inicial | [ ] | |
| 2 | Botón auto-generar SKU | [ ] | |
| 3 | Botón generar código | [ ] | |
| 4 | Validación SKU vacío | [ ] | |
| 5 | Formato ampliado | [ ] | |
| 6 | Botón imprimir (sin módulos) | [ ] | |
| 7 | Instalar módulos | [ ] | Opcional |
| 8 | Botón imprimir (con módulos) | [ ] | Opcional |
| 9 | Crear producto completo | [ ] | |
| 10 | Editar producto | [ ] | |
| 11 | Secuencia de SKUs | [ ] | |
| 12 | Validación EAN-13 | [ ] | |

---

## 🐛 Reportar Problemas

Si encuentras algún error, anota:
1. **Qué funcionalidad estabas probando**
2. **Qué esperabas que pasara**
3. **Qué pasó realmente**
4. **Mensaje de error** (si lo hay)
5. **Captura de pantalla** (si es posible)

---

## ✨ Mejoras Implementadas

- ✅ SKU auto-generado con formato `PROD-XXXXXX` (999,999 productos)
- ✅ Código de barras EAN-13 auto-generado
- ✅ Botones para regenerar SKU y código de barras
- ✅ Botón para imprimir etiquetas con código de barras
- ✅ Validación de formato EAN-13 con dígito verificador
- ✅ Soporte para impresoras configuradas en el sistema
- ✅ Documentación completa en `BARCODE_PRINTING.md`

---

**Fecha de prueba:** _______________
**Probado por:** _______________
**Versión:** 1.0
