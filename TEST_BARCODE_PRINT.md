# Test de Impresión de Código de Barras

## Instrucciones para Debug

Cuando vayas a imprimir un código de barras desde el módulo "Editar Producto":

### 1. Abre la aplicación desde PowerShell:
```powershell
cd c:\Users\USER\Desktop\POS
python main.py
```

### 2. Ve al módulo de productos y edita/crea un producto

### 3. Cuando hagas clic en "Imprimir", revisa la consola de PowerShell

Deberías ver algo como:

```
🔍 DEBUG - Valores para impresión:
   Nombre: Guantes de Box
   SKU: PROD-000005
   Código de Barras: 7750000000052

🖨️ Imprimiendo código de barras en impresora térmica...
   Producto: Guantes de Box
   SKU: PROD-000005
   Código de Barras: 7750000000052
   📊 Imprimiendo código de barras: 7750000000052
   ✓ Línea de código de barras agregada al contenido
   ✅ Código de barras enviado exitosamente
```

## ¿Qué buscar?

1. **Si el "Código de Barras" muestra el SKU** (ej: PROD-000005 en lugar de 7750000000052):
   - Significa que el código de barras no se generó correctamente
   - Verifica que hayas hecho clic en "Generar" antes de "Imprimir"

2. **Si muestra "Usando impresión estándar"**:
   - Tu impresora NO se detectó como térmica
   - La imagen completa (con el código de barras visual) se imprimirá
   - Esto está bien para impresoras normales

3. **Si muestra "Imprimiendo código de barras en impresora térmica"**:
   - Tu impresora SÍ se detectó como térmica
   - Solo se enviará texto a la impresora
   - Deberías ver el código EAN-13 en la impresión

## Solución si el código de barras no aparece:

Si ves en la consola que dice:
```
📊 Imprimiendo código de barras: 7750000000052
```

Pero en el papel impreso solo aparece el SKU, puede ser que:

1. **La impresora térmica no soporta el comando DOUBLE SIZE**
   - Algunos modelos ignoran este comando
   - El código se imprime pero muy pequeño o con el font normal

2. **El código se está cortando**
   - 13 dígitos pueden ser mucho para algunas térmicas de 58mm
   - Prueba con una de 80mm si es posible

3. **Encoding CP437 tiene problemas con números**
   - Poco probable pero puede pasar
   - Probaremos otro encoding si es necesario

## Envía este debug:

Copia y pega TODO lo que salga en la consola cuando imprimas, desde:
```
🔍 DEBUG - Valores para impresión:
```

Hasta:
```
✅ Código de barras enviado exitosamente
```

O hasta el error que aparezca.
