# 📦 Módulo de Inventario/Productos - Sistema POS

## 🎯 Descripción

Módulo completo de gestión de productos e inventario con control de permisos integrado, diseñado para el Sistema POS.

## ✨ Características

### Gestión de Productos
- ✅ **CRUD Completo**: Crear, leer, actualizar y eliminar productos
- 📊 **Control de Stock**: Seguimiento en tiempo real del inventario
- 💰 **Gestión de Precios**: Precio de venta, costo y cálculo automático de margen
- 🏷️ **Categorización**: Organización por categorías y unidades de medida
- 🔍 **Búsqueda Avanzada**: Búsqueda por nombre, SKU o código de barras
- 📈 **Alertas de Stock**: Notificaciones de stock bajo, agotado o exceso
- 📝 **Historial de Movimientos**: Registro completo de entradas/salidas

### Seguridad y Permisos
- 🔐 **Control de Acceso**: Integrado con el sistema de permisos
- 👥 **Permisos Granulares**:
  - `inventory.view` - Ver productos
  - `inventory.create` - Crear productos
  - `inventory.edit` - Editar productos
  - `inventory.delete` - Eliminar productos
  - `inventory.stock` - Gestionar stock
  - `inventory.reports` - Ver reportes
  - `inventory.export` - Exportar datos

## 🚀 Instalación

### 1. Crear las Tablas de Base de Datos

Ejecuta el script de migración:

```bash
python migrate_products_tables.py
```

Este script creará las siguientes tablas:
- `categories` - Categorías de productos
- `units` - Unidades de medida
- `products` - Productos
- `product_movements` - Movimientos de inventario

También insertará datos de ejemplo:
- 8 categorías por defecto
- 10 unidades de medida
- 5 productos de ejemplo

### 2. Verificar Permisos

Asegúrate de que los permisos estén configurados en `models/role_model.py`:

```python
AVAILABLE_PERMISSIONS = {
    'Inventario': [
        'inventory.view',
        'inventory.create',
        'inventory.edit',
        'inventory.delete',
        'inventory.stock',
        'inventory.reports',
        'inventory.export'
    ],
    # ... otros permisos
}
```

### 3. Configurar Roles

Asigna permisos a los roles desde **Gestión de Roles**:

#### Ejemplo: Rol "Gerente de Inventario"
```python
permissions = [
    'inventory.view',
    'inventory.create',
    'inventory.edit',
    'inventory.stock',
    'inventory.reports',
    'dashboard.view'
]
```

#### Ejemplo: Rol "Vendedor"
```python
permissions = [
    'inventory.view',  # Solo ver productos
    'dashboard.view'
]
```

## 📖 Uso

### Acceder al Módulo

1. Iniciar sesión con un usuario que tenga permiso `inventory.view`
2. En el dashboard, hacer clic en **"📦 Registro de Productos"**

### Crear un Producto

1. Clic en **"➕ Nuevo Producto"**
2. Completar el formulario:
   - **SKU**: Código único (requerido)
   - **Nombre**: Nombre del producto (requerido)
   - **Descripción**: Descripción detallada (opcional)
   - **Categoría**: Seleccionar categoría (requerido)
   - **Unidad**: Seleccionar unidad de medida (requerido)
   - **Precio de Venta**: Precio al público (requerido)
   - **Costo**: Costo de adquisición (requerido)
   - **Stock**: Cantidad inicial
   - **Stock Mínimo/Máximo**: Para alertas automáticas
   - **Código de Barras**: Opcional
   - **Tasa de Impuesto**: Porcentaje de IVA
3. Clic en **"💾 Guardar"**

### Editar un Producto

1. Seleccionar un producto de la lista
2. Clic en **"✏️ Editar"** en el panel derecho
3. Modificar los campos necesarios
4. Guardar cambios

### Ajustar Stock

1. Seleccionar un producto
2. Clic en **"📊 Ajustar Stock"**
3. Ingresar:
   - **Cantidad**: Positivo para agregar, negativo para quitar
   - **Tipo**: Ajuste manual, compra, venta, etc.
   - **Notas**: Motivo del ajuste
4. Guardar

### Búsqueda de Productos

- Usar la barra de búsqueda en la parte superior
- Busca por: nombre, SKU o código de barras
- Resultados en tiempo real mientras escribes

## 🎨 Interfaz

### Panel Principal
- **Lista de Productos**: Tabla con todos los productos
- **Panel de Detalles**: Información detallada del producto seleccionado
- **Estadísticas**: Total de productos, stock bajo, productos agotados

### Indicadores Visuales

| Color | Estado | Significado |
|-------|--------|-------------|
| ✅ Verde | Normal | Stock suficiente |
| ⚠️ Naranja | Stock Bajo | Stock por debajo del mínimo |
| 🚫 Rojo | Agotado | Sin stock disponible |

### Cálculos Automáticos

- **Margen de Ganancia**: `((Precio - Costo) / Costo) * 100`
- **Estado de Stock**:
  - Normal: Stock > Stock Mínimo
  - Bajo: Stock ≤ Stock Mínimo
  - Agotado: Stock = 0

## 📊 Estructura de Datos

### Tabla `products`

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    unit_id INT NOT NULL,
    barcode VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    stock_quantity DECIMAL(10, 2) DEFAULT 0,
    min_stock DECIMAL(10, 2) DEFAULT 0,
    max_stock DECIMAL(10, 2) DEFAULT 0,
    tax_rate DECIMAL(5, 2) DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Tabla `product_movements`

Registra todos los movimientos de inventario:

```sql
CREATE TABLE product_movements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    movement_type ENUM('purchase', 'sale', 'adjustment', 'return', 'transfer'),
    quantity DECIMAL(10, 2) NOT NULL,
    previous_stock DECIMAL(10, 2) NOT NULL,
    new_stock DECIMAL(10, 2) NOT NULL,
    notes TEXT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Archivos del Módulo

### Modelos
- `models/product_model.py` - Modelo de datos de productos

### Controladores
- `controllers/product_controller.py` - Lógica de negocio

### Vistas
- `views/product_management_view.py` - Vista principal
- `views/product_form_dialog.py` - Diálogo crear/editar

### Base de Datos
- `database/create_products_tables.sql` - Script SQL
- `migrate_products_tables.py` - Script de migración

## 🎯 Próximos Pasos

### Mejoras Sugeridas

1. **Módulo de Ventas** - Integrar con el módulo de productos
2. **Módulo de Compras** - Gestión de compras a proveedores
3. **Reportes** - Reportes de inventario y movimientos
4. **Importación/Exportación** - CSV/Excel
5. **Códigos de Barras** - Generación e impresión
6. **Imágenes** - Subir fotos de productos
7. **Variantes** - Productos con variantes (tallas, colores)
8. **Lotes y Vencimientos** - Control de lotes y fechas

## 🐛 Solución de Problemas

### Error: "No se pueden crear las tablas"
```bash
# Verificar conexión a la base de datos
python -c "from database.connection import DatabaseConnection; db = DatabaseConnection(); print('✅ OK' if db.connect() else '❌ Error')"
```

### Error: "No tienes permisos para acceder"
1. Ir a **Gestión de Roles**
2. Editar el rol del usuario
3. Marcar el permiso `inventory.view`
4. Guardar cambios
5. Cerrar sesión y volver a iniciar

### Error: "SKU ya existe"
- Cada producto debe tener un SKU único
- Cambiar el SKU por uno diferente

## 📞 Soporte

Para reportar problemas o sugerencias:
- Revisar el archivo `logs/pos_system.log`
- Contactar al administrador del sistema

---

**¡El módulo de inventario está listo para producción! 🎉**
