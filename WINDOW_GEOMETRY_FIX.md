# 🪟 Corrección de Geometría de Ventana

## 📋 Resumen
Sistema implementado para mantener el tamaño y posición de la ventana principal al cambiar entre módulos.

## ❌ Problema Original
- **Login muy grande**: Ventana de login se redimensionaba con el sistema responsive
- **Geometría no persistente**: Al cambiar entre módulos (Dashboard ↔ Usuarios ↔ Productos), la ventana volvía a su tamaño inicial, perdiendo el tamaño que el usuario había configurado manualmente

## ✅ Soluciones Implementadas

### 1. Login con Tamaño Fijo
**Archivo**: `views/login_view.py`

```python
def setup_ui(self):
    # ✅ Tamaño fijo: 450x600 (no responsive)
    self.root.geometry("450x600")
    
    # ✅ Centrado en pantalla
    x = (screen_width - 450) // 2
    y = (screen_height - 600) // 2
    self.root.geometry(f"450x600+{x}+{y}")
    
    # ✅ No redimensionable
    self.root.minsize(450, 600)
    self.root.maxsize(450, 600)
    self.root.resizable(False, False)
```

**Widgets con tamaños fijos**:
- Logo: `width=100, height=100`
- Fuente logo: `font=('Segoe UI Emoji', 24)`
- Fuente empresa: `font=('Arial', 16, 'bold')`
- Fuente bienvenida: `font=('Arial', 14)`

### 2. Sistema de Persistencia de Geometría
**Archivo**: `controllers/main_controller.py`

#### Variables de Estado
```python
def __init__(self):
    self.saved_window_geometry = None  # Guarda "1600x900+160+90"
    self.saved_window_state = None     # Guarda "zoomed" o "normal"
```

#### Métodos Implementados

**`_save_window_geometry()`**: Guarda estado actual
```python
def _save_window_geometry(self):
    """Guardar geometría actual de la ventana"""
    try:
        if self.main_window:
            # Guarda formato: "widthxheight+x+y"
            self.saved_window_geometry = self.main_window.geometry()
            # Guarda estado: "zoomed" o "normal"
            self.saved_window_state = self.main_window.state()
    except Exception as e:
        self.logger.error(f"Error guardando geometría: {e}")
```

**`_restore_window_geometry()`**: Restaura estado guardado
```python
def _restore_window_geometry(self):
    """Restaurar geometría guardada de la ventana"""
    try:
        if self.main_window and self.saved_window_geometry:
            # Restaura tamaño y posición
            self.main_window.geometry(self.saved_window_geometry)
            # Restaura estado de maximizado
            if hasattr(self, 'saved_window_state') and self.saved_window_state == 'zoomed':
                self.main_window.state('zoomed')
    except Exception as e:
        self.logger.error(f"Error restaurando geometría: {e}")
```

**`_clear_main_content()`**: Modificado para guardar antes de limpiar
```python
def _clear_main_content(self):
    """Limpiar contenido principal de la ventana"""
    # ✅ PRIMERO: Guardar geometría ANTES de destruir widgets
    self._save_window_geometry()
    
    # Destruir widgets
    for widget in self.main_window.winfo_children():
        if not isinstance(widget, tk.Menu):
            widget.destroy()
```

## 🔧 Módulos Modificados

### Métodos que Ahora Mantienen Geometría

| Método | Descripción | Guarda | Restaura |
|--------|-------------|--------|----------|
| `_back_to_dashboard()` | Volver al dashboard | ✅ Auto | ✅ Sí |
| `_view_products()` | Abrir Productos | ✅ Auto | ✅ Sí |
| `_manage_users()` | Abrir Usuarios | ✅ Auto | ✅ Sí |
| `_manage_roles()` | Abrir Roles | ✅ Auto | ✅ Sí |
| `_view_categories()` | Abrir Categorías | ✅ Manual | ✅ Sí |
| `_view_stock_control()` | Abrir Control Stock | ✅ Manual | ✅ Sí |
| `_new_sale()` | Abrir POS | ✅ Auto | ✅ Sí |
| `_system_config()` | Abrir Configuración | ✅ Auto | ✅ Sí |

### Patrón de Implementación

**Para métodos que usan `_clear_main_content()`**:
```python
def _view_products(self):
    # 1. _clear_main_content() guarda geometría automáticamente
    self._clear_main_content()
    
    # 2. Crear nueva vista
    self.product_view = ProductManagementView(...)
    
    # 3. Registrar callbacks
    self.product_view.bind_callback(...)
    
    # 4. Cargar datos
    self._load_products()
    
    # ✅ 5. RESTAURAR geometría al final
    self._restore_window_geometry()
```

**Para métodos que limpian manualmente**:
```python
def _view_categories(self):
    # ✅ 1. Guardar ANTES de destruir widgets
    self._save_window_geometry()
    
    # 2. Limpiar manualmente
    for widget in self.main_window.winfo_children():
        widget.destroy()
    
    # 3. Crear nueva vista
    category_view = CategoryManagementView(...)
    
    # 4. Cargar datos
    self._load_categories(...)
    
    # ✅ 5. RESTAURAR geometría al final
    self._restore_window_geometry()
```

## 📊 Flujo de Datos

```
┌─────────────────────────────────────────────────────┐
│ 1. Usuario redimensiona ventana manualmente         │
│    Ventana: 1600x900 @ posición (160, 90)          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. Usuario hace clic en "Gestión de Usuarios"      │
│    → _manage_users() se ejecuta                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. _clear_main_content() ejecuta automáticamente   │
│    → _save_window_geometry()                        │
│    saved_window_geometry = "1600x900+160+90"        │
│    saved_window_state = "normal"                    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. Widgets destruidos, nueva vista creada           │
│    UserManagementView(self.main_window, ...)        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 5. _restore_window_geometry() ejecuta al final     │
│    self.main_window.geometry("1600x900+160+90")     │
│    ✅ Ventana mantiene tamaño del usuario           │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 6. Usuario hace clic en "Volver al Dashboard"      │
│    → _back_to_dashboard() se ejecuta                │
│    → Proceso se repite (pasos 3-5)                  │
│    ✅ Dashboard aparece con tamaño 1600x900         │
└─────────────────────────────────────────────────────┘
```

## 🧪 Escenarios de Prueba

### ✅ Caso 1: Transición Dashboard → Producto → Dashboard
1. Dashboard abierto en 1600x900
2. Click en "Gestión de Productos"
3. **Verificar**: Productos abre en 1600x900
4. Click en "Regresar al Dashboard"
5. **Verificar**: Dashboard mantiene 1600x900

### ✅ Caso 2: Ventana Maximizada
1. Dashboard abierto, maximizar ventana (estado "zoomed")
2. Click en "Gestión de Usuarios"
3. **Verificar**: Usuarios abre maximizado
4. Click en "Volver"
5. **Verificar**: Dashboard mantiene maximización

### ✅ Caso 3: Cambio Entre Módulos
1. Dashboard → Productos (redimensionar a 1400x800)
2. Productos → Usuarios
3. **Verificar**: Usuarios abre en 1400x800
4. Usuarios → Roles
5. **Verificar**: Roles abre en 1400x800

### ✅ Caso 4: Login NO se Ve Afectado
1. Cerrar sesión
2. **Verificar**: Login aparece en 450x600 (tamaño fijo)
3. **Verificar**: Login NO es redimensionable
4. Iniciar sesión
5. **Verificar**: Dashboard usa sistema responsive

## 🔍 Formato de Geometría Tkinter

```python
# Formato: "WIDTHxHEIGHT+X+Y"
geometry_string = "1600x900+160+90"

# Componentes:
# - WIDTH: 1600 (ancho en píxeles)
# - HEIGHT: 900 (alto en píxeles)  
# - X: 160 (posición horizontal desde izquierda de pantalla)
# - Y: 90 (posición vertical desde arriba de pantalla)

# Estado de ventana:
state = "zoomed"  # Maximizada
state = "normal"  # Normal/restaurada
```

## ⚠️ Notas Importantes

1. **Login es especial**: NO usa sistema responsive, mantiene tamaño fijo 450x600
2. **Guardado automático**: `_clear_main_content()` guarda geometría automáticamente
3. **Restauración manual**: Cada método de vista debe llamar `_restore_window_geometry()` al final
4. **Estado maximizado**: Se guarda y restaura el estado "zoomed" correctamente
5. **Excepciones controladas**: Todos los métodos tienen try/catch para evitar crashes

## 📝 Checklist de Implementación

- [x] Crear métodos `_save_window_geometry()` y `_restore_window_geometry()`
- [x] Modificar `_clear_main_content()` para guardar geometría
- [x] Revertir login a tamaño fijo (450x600)
- [x] Aplicar restauración en `_back_to_dashboard()`
- [x] Aplicar restauración en `_view_products()`
- [x] Aplicar restauración en `_manage_users()`
- [x] Aplicar restauración en `_manage_roles()`
- [x] Aplicar restauración en `_view_categories()`
- [x] Aplicar restauración en `_view_stock_control()`
- [x] Aplicar restauración en `_new_sale()`
- [x] Aplicar restauración en `_system_config()`
- [x] Documentar cambios (este archivo)

## 🎯 Resultado Final

✅ **Login**: Ventana fija 450x600, no redimensionable, centrada
✅ **Dashboard y Módulos**: Mantienen tamaño y posición al cambiar de vista
✅ **Maximización**: Se preserva el estado maximizado entre transiciones
✅ **UX mejorada**: Usuario puede redimensionar ventana y el tamaño se respeta

---

**Fecha de implementación**: 2024  
**Archivos modificados**: `views/login_view.py`, `controllers/main_controller.py`  
**Sistema**: POS con permisos RBAC y diseño responsive
