# Solución: Formato SKU PROD-XXXXXX y Generación de Códigos de Barras EAN-13

## Problema Reportado

El usuario reportó dos problemas:
1. **Autoincremento no funcionaba**: No reconocía el último PROD-XXXXXX para generar el siguiente
2. **Código de barras siempre mostraba 000001**: A pesar de poner 000002 en el SKU, el EAN-13 se generaba con 000001

## Causa Raíz

El código estaba usando `code` como nombre de columna, pero la tabla `products` usa **`sku`** como nombre de columna.

```sql
-- ❌ INCORRECTO (lo que estaba en el código)
SELECT code FROM products WHERE code LIKE 'PROD-%'

-- ✅ CORRECTO (solución aplicada)
SELECT sku FROM products WHERE sku LIKE 'PROD-%'
```

## Cambios Realizados

### 1. Archivo: `models/product_model.py`

#### Método `generate_next_code()`:
- **Antes**: Usaba columna `code`
- **Ahora**: Usa columna `sku`

```python
# Query actualizada (línea ~38)
query = """
    SELECT sku 
    FROM products 
    WHERE sku LIKE 'PROD-%'
      AND LENGTH(sku) = 11
      AND SUBSTRING(sku, 6) REGEXP '^[0-9]+$'
    ORDER BY CAST(SUBSTRING(sku, 6) AS UNSIGNED) DESC 
    LIMIT 1
"""
```

**Lógica del autoincremento:**
1. Busca el SKU más alto que empiece con `PROD-` y tenga 6 dígitos después
2. Extrae el número después del guión (ej: `PROD-000003` → `000003`)
3. Incrementa en 1 (ej: `3 + 1 = 4`)
4. Formatea con 6 dígitos: `PROD-{4:06d}` → `PROD-000004`

#### Método `generate_barcode_from_code()`:
- **Mejorado**: Ahora extrae correctamente el número del SKU PROD-XXXXXX

```python
if code.startswith('PROD-'):
    parts = code.split('-')
    if len(parts) == 2 and parts[1].isdigit():
        number = int(parts[1])  # Extrae solo el número
```

**Ejemplo de generación:**
- SKU: `PROD-000002`
- Número extraído: `2`
- Base EAN-13: `775` + `000000002` = `775000000002` (12 dígitos)
- Dígito verificador: calculado automáticamente
- **Código de barras final**: `7750000000021` (13 dígitos)

### 2. Logging Mejorado

Se agregaron logs informativos para depuración:

```python
self.logger.info(f"🔍 Buscando último código PROD-XXXXXX en base de datos...")
self.logger.info(f"   Último código encontrado: {last_code}")
self.logger.info(f"   Último número: {last_number}")
self.logger.info(f"   ✅ Siguiente número: {next_number}")
self.logger.info(f"   📦 Código generado: {next_code}")
```

## Formato Actual

### SKU (Identificador Visual)
```
Formato: PROD-XXXXXX
Ejemplo: PROD-000001, PROD-000002, PROD-000123
Máximo:  PROD-999999 (hasta 999,999 productos)
```

### Código de Barras EAN-13
```
Formato: 775 + número_sku (9 dígitos) + dígito_verificador
Ejemplo: 
  - SKU: PROD-000001 → Barcode: 7750000000014
  - SKU: PROD-000002 → Barcode: 7750000000021
  - SKU: PROD-123456 → Barcode: 7750001234562
```

**Estructura EAN-13:**
- Posiciones 1-3: `775` (código de país - Perú)
- Posiciones 4-12: `000000XXX` (número del SKU con padding)
- Posición 13: Dígito verificador (calculado automáticamente)

## Verificación de Funcionamiento

### Test 1: Autoincremento
```python
from models.product_model import ProductModel

product_model = ProductModel()
sku = product_model.generate_next_code()
# Si el último es PROD-000003, genera: PROD-000004 ✅
```

### Test 2: Código de Barras
```python
from models.product_model import ProductModel

product_model = ProductModel()

# Prueba con diferentes SKU
barcode1 = product_model.generate_barcode_from_code("PROD-000001")
# Resultado: 7750000000014 ✅

barcode2 = product_model.generate_barcode_from_code("PROD-000002")
# Resultado: 7750000000021 ✅ (diferente al anterior)

barcode3 = product_model.generate_barcode_from_code("PROD-123456")
# Resultado: 7750001234562 ✅
```

## Estado Actual de la Base de Datos

Según verificación en `check_products_db.py`:

```
📊 Total de productos: 9
📊 Productos con formato PROD-XXXXXX: 8
📊 Productos con formato P###: 1

✅ Último código encontrado: PROD-000003
   Siguiente sería: PROD-000004
```

## Compatibilidad

El sistema mantiene **compatibilidad con formato antiguo P###**:

```python
elif code.startswith('P') and code[1:].isdigit():
    # Compatibilidad con formato antiguo P###
    number = int(code[1:])
```

Productos antiguos con formato `P001`, `P002`, etc. seguirán funcionando correctamente.

## Scripts de Prueba Creados

1. **`test_sku_barcode_generation.py`**: Prueba generación de SKU y códigos de barras
2. **`check_products_db.py`**: Verifica estructura de tabla y productos existentes

## Solución Confirmada ✅

- ✅ Autoincremento funciona correctamente
- ✅ Códigos de barras se generan con el número correcto del SKU
- ✅ Cada SKU diferente genera un código de barras EAN-13 diferente
- ✅ Formato PROD-XXXXXX implementado correctamente
- ✅ Compatibilidad con formato antiguo P### mantenida

---

**Fecha de implementación**: 31 de Octubre, 2025  
**Archivos modificados**: `models/product_model.py`
