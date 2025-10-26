"""
Script para comparar columnas del modelo vs tabla real
"""
import re

print("=" * 70)
print("🔍 ANÁLISIS DE COLUMNAS - products")
print("=" * 70)

# Columnas reales de la tabla (de check_table_structure.py anterior)
columnas_reales = [
    'id', 'sku', 'name', 'description', 'category_id', 'unit_id', 
    'barcode', 'price', 'cost', 'stock_quantity', 'min_stock', 
    'max_stock', 'tax_rate', 'image_path', 'status', 'created_by', 
    'created_at', 'updated_at'
]

# Columnas que usa el modelo (del código que vimos)
columnas_modelo = [
    'id', 'code', 'barcode', 'name', 'description', 'category_id', 
    'supplier_id', 'brand', 'model', 'cost_price', 'sale_price', 
    'wholesale_price', 'min_price', 'current_stock', 'min_stock', 
    'max_stock', 'reorder_point', 'unit', 'weight', 'dimensions', 
    'tax_rate', 'active', 'is_service', 'track_stock', 
    'allow_negative_stock', 'image_path', 'tags', 'attributes', 
    'created_at', 'updated_at', 'created_by'
]

print("\n❌ Columnas que usa el MODELO pero NO existen en la TABLA:")
for col in columnas_modelo:
    if col not in columnas_reales:
        print(f"   - {col}")

print("\n✅ Columnas que existen en la TABLA pero NO usa el MODELO:")
for col in columnas_reales:
    if col not in columnas_modelo:
        print(f"   - {col}")

print("\n📋 MAPEO SUGERIDO (Modelo → Tabla):")
mapeo = {
    'code': 'sku',
    'current_stock': 'stock_quantity',
    'cost_price': 'cost',
    'sale_price': 'price',
    'active': "status = 'active'",
}

for modelo_col, tabla_col in mapeo.items():
    print(f"   p.{modelo_col:20} → p.{tabla_col}")

print("\n" + "=" * 70)
