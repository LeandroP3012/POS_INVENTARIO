# 🖨️ Guía de Configuración para GP-L80180 Series

## Problema Identificado

La impresora **GP-L80180 Series** no estaba siendo reconocida como impresora térmica porque el sistema solo buscaba palabras clave como "TP-", "TM-", etc., pero NO incluía "GP-" (Gprinter).

## ✅ Soluciones Implementadas

### 1. Detección Automática Mejorada
Se agregó **'GP-'** y **'GPRINTER'** a la lista de palabras clave para detectar automáticamente impresoras térmicas Gprinter.

### 2. Modo de Impresora Manual
Se agregó la opción **"Modo de Impresora"** en la configuración que permite forzar el tipo de impresora:
- **auto**: Detección automática (recomendado)
- **thermal**: Forzar impresión térmica ESC/POS
- **standard**: Forzar impresión estándar/PDF

## 📋 Pasos para Configurar en la PC con GP-L80180

### Opción 1: Configuración desde la Interfaz (Recomendada)

1. **Abrir el Sistema POS**
   - Ejecuta `main.py` e inicia sesión

2. **Ir a Configuración**
   - Click en el menú de navegación
   - Selecciona **"Configuración"**
   - Ve a la pestaña **"🖨️ Impresión"**

3. **Actualizar Lista de Impresoras**
   - Click en el botón **"🔄 Actualizar Lista de Impresoras"**
   - Verifica que aparezca **"GP-L80180 Series"** en el mensaje

4. **Seleccionar la Impresora**
   - En el desplegable **"Impresora por Defecto"**, selecciona **"GP-L80180 Series"**

5. **Configurar el Modo** (IMPORTANTE)
   - En **"Modo de Impresora"**, selecciona **"thermal"** (forzar térmica)
   - Esto asegura que la impresora use comandos ESC/POS para impresión térmica

6. **Guardar Cambios**
   - Click en **"💾 Guardar Cambios"**
   - Espera el mensaje de confirmación

7. **Probar Impresión**
   - Realiza una venta de prueba
   - Verifica que el ticket se imprima correctamente

### Opción 2: Configuración Manual del Archivo

Si prefieres editar directamente el archivo de configuración:

1. **Navegar a la carpeta del proyecto**
   ```
   cd C:\Users\USER\Desktop\POS
   ```

2. **Editar el archivo de configuración**
   - Abre `config/system_config.json` con un editor de texto

3. **Modificar estos valores**:
   ```json
   {
     "printer": "GP-L80180 Series",
     "printer_mode": "thermal",
     "thermal_printer_keywords": []
   }
   ```

4. **Guardar y cerrar**

5. **Reiniciar el sistema POS**

## 🔍 Verificación de Configuración

### Script de Prueba

Ejecuta el script de verificación en la PC con la GP-L80180:

```bash
python test_gp_l80180.py
```

Este script:
- ✅ Lista todas las impresoras instaladas
- ✅ Verifica si la GP-L80180 está instalada
- ✅ Muestra si se detecta como térmica
- ✅ Proporciona recomendaciones específicas

### Verificación Manual de Impresoras

También puedes ejecutar:

```bash
python verificar_impresoras.py
```

Este script muestra todas las impresoras disponibles en el sistema.

## 🔧 Solución de Problemas

### Problema: La impresora no aparece en la lista

**Causas posibles:**
- La impresora no está instalada en Windows
- Los drivers no están correctamente instalados
- La impresora está apagada o desconectada

**Solución:**
1. Ve a **Configuración de Windows** > **Dispositivos** > **Impresoras y escáneres**
2. Verifica que aparezca **"GP-L80180 Series"**
3. Si no aparece, instala los drivers desde: [sitio oficial de Gprinter]
4. Reinicia el sistema POS y usa **"🔄 Actualizar Lista de Impresoras"**

### Problema: La impresora aparece pero no imprime

**Causas posibles:**
- El modo de impresora está configurado como "standard" en lugar de "thermal"
- La impresora no está configurada como predeterminada
- Hay un problema con los comandos ESC/POS

**Solución:**
1. Verifica que **"Modo de Impresora"** esté en **"thermal"**
2. Asegúrate de seleccionar **"GP-L80180 Series"** en el desplegable
3. Guarda los cambios y reinicia el sistema
4. Realiza una venta de prueba

### Problema: El ticket imprime pero con formato incorrecto

**Causas posibles:**
- El tamaño de papel está mal configurado
- La impresora necesita configuración de ancho

**Solución:**
1. En la configuración, cambia **"Tamaño de Papel"** a **"Recibo (80mm)"**
2. Si el problema persiste, edita `utils/thermal_printer.py` y ajusta:
   ```python
   self.char_width = 48  # Ajustar según tu impresora
   ```

### Problema: Error "No se pudo conectar con la impresora"

**Causas posibles:**
- La impresora está en uso por otra aplicación
- Puerto USB/Red con problemas
- Falta el módulo pywin32

**Solución:**
1. Cierra otras aplicaciones que usen la impresora
2. Reinstala pywin32: `pip install --upgrade pywin32`
3. Verifica la conexión física de la impresora
4. Reinicia la impresora y el sistema

## 📝 Características de la GP-L80180 Series

- **Tipo**: Impresora térmica de recibos
- **Ancho de papel**: 80mm
- **Comandos soportados**: ESC/POS estándar
- **Conexión**: USB / Ethernet / Bluetooth (según modelo)
- **Velocidad**: Alta velocidad de impresión
- **Cortador**: Automático

## 🎯 Configuración Recomendada

Para obtener los mejores resultados con la GP-L80180:

```json
{
  "printer": "GP-L80180 Series",
  "printer_mode": "thermal",
  "paper_size": "Recibo (80mm)",
  "auto_print": true,
  "print_logo": true,
  "print_company_info": true,
  "copies": "1"
}
```

## 📞 Soporte Adicional

Si después de seguir estos pasos aún tienes problemas:

1. Ejecuta `test_gp_l80180.py` y comparte el resultado
2. Revisa los logs en `logs/pos_system.log`
3. Verifica que la impresora funcione con otras aplicaciones (prueba de impresión de Windows)

## 📚 Archivos Modificados

Los siguientes archivos fueron actualizados para soportar la GP-L80180:

- ✅ `utils/ticket_generator.py` - Agregado 'GP-' y 'GPRINTER' a keywords
- ✅ `config/system_config.json` - Agregados campos printer_mode y thermal_printer_keywords
- ✅ `views/configuration_view.py` - Agregada interfaz de configuración de modo de impresora
- ✅ `controllers/configuration_controller.py` - Ya soportaba detección de todas las impresoras

## ✨ Mejoras Implementadas

1. **Detección automática mejorada** para impresoras Gprinter
2. **Modo de impresora configurable** (auto/thermal/standard)
3. **Botón de actualización** de lista de impresoras en tiempo real
4. **Scripts de diagnóstico** para verificar configuración
5. **Guía completa** de configuración y solución de problemas
