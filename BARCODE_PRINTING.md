# 📊 Sistema de Códigos de Barras

## Características

### 🔄 Generación Automática

#### SKU (Stock Keeping Unit)
- **Formato**: `PROD-XXXXXX` (6 dígitos)
- **Capacidad**: Hasta 999,999 productos
- **Auto-generación**: Al crear un nuevo producto, el SKU se genera automáticamente con el siguiente número disponible
- **Ejemplo**: `PROD-000001`, `PROD-000002`, ..., `PROD-999999`

#### Código de Barras EAN-13
- **Formato**: 13 dígitos según estándar EAN-13
- **Estructura**: 
  - 3 dígitos: Código de país (775 para Perú)
  - 9 dígitos: Número basado en el SKU
  - 1 dígito: Verificador (calculado automáticamente)
- **Generación**: Se genera automáticamente basándose en el SKU
- **Ejemplo**: `7750000010003` (para PROD-000001)

### 🎯 Funcionalidades

1. **Auto-generación al crear producto**
   - Al abrir el formulario de nuevo producto, el SKU y código de barras se generan automáticamente
   - El usuario puede modificarlos si lo desea

2. **Botón "🔄 Auto-generar" (SKU)**
   - Genera un nuevo SKU con el siguiente número disponible
   - Actualiza automáticamente el código de barras asociado

3. **Botón "🔄 Generar" (Código de Barras)**
   - Genera o regenera el código de barras basándose en el SKU actual
   - Útil si se modificó el SKU manualmente

4. **Botón "🖨️ Imprimir"**
   - Imprime el código de barras en la impresora configurada
   - Incluye el nombre del producto
   - Formato optimizado para etiquetas

### 🖨️ Configuración de Impresión

#### Requisitos
Para usar la función de impresión, necesitas instalar las siguientes dependencias:

```bash
pip install python-barcode[images] Pillow pywin32
```

#### Configurar Impresora
1. Ve a **Configuraciones** → **Sistema** → **Impresora**
2. Selecciona la impresora que deseas usar
3. Si no configuras ninguna, se usará la impresora predeterminada del sistema

#### Proceso de Impresión
1. Genera o verifica que tengas un código de barras
2. Haz clic en el botón **🖨️ Imprimir**
3. El sistema generará una etiqueta con:
   - Nombre del producto (arriba)
   - Código de barras EAN-13
   - Número del código (abajo)
4. Se enviará a la impresora configurada

### 🔧 Solución de Problemas

#### Error: "Módulos Requeridos"
**Problema**: No están instaladas las librerías necesarias.
**Solución**: 
```bash
pip install python-barcode[images] Pillow pywin32
```

#### Error: "Impresora no encontrada"
**Problema**: La impresora configurada no está disponible.
**Solución**:
1. Verifica que la impresora esté encendida y conectada
2. Revisa la configuración en el sistema
3. El sistema intentará usar la impresora predeterminada como respaldo

#### El código de barras no se genera
**Problema**: El SKU tiene un formato no reconocido.
**Solución**:
1. Usa el botón "🔄 Auto-generar" para generar un SKU válido
2. O asegúrate de que el SKU siga el formato `PROD-XXXXXX`

### 📝 Notas Importantes

- Los códigos de barras EAN-13 generados son **válidos** y cumplen con el estándar internacional
- El dígito verificador se calcula automáticamente según la especificación EAN-13
- Los códigos generados pueden ser leídos por cualquier escáner de códigos de barras estándar
- Se recomienda usar impresoras de etiquetas para mejores resultados
- Los códigos de barras se guardan en la base de datos junto con el producto

### 🎨 Personalización

#### Modificar el Prefijo de País
En `models/product_model.py`, línea ~43:
```python
barcode_base = f"775{number:0>9}"  # 775 = Perú
```
Cambia `775` por el código de tu país:
- 🇵🇪 Perú: 775
- 🇦🇷 Argentina: 779
- 🇨🇱 Chile: 780
- 🇨🇴 Colombia: 770
- 🇲🇽 México: 750

#### Cambiar el Formato del SKU
En `models/product_model.py`, método `generate_next_sku()`:
```python
return f"PROD-{next_number:06d}"  # 06d = 6 dígitos
```
Puedes cambiar:
- `PROD` por otro prefijo
- `06d` por otro número de dígitos (ej: `08d` para 8 dígitos)

### 🔐 Validación

El sistema valida automáticamente que:
- ✅ El SKU sea único en la base de datos
- ✅ El código de barras tenga 13 dígitos
- ✅ El dígito verificador sea correcto
- ✅ El formato EAN-13 sea válido

---

**Desarrollado para Sistema POS - Gestión de Inventario**
