# 🔍 Instrucciones de Diagnóstico - Permisos No Se Guardan

## 📋 **QUÉ HACER AHORA**

### **Paso 1: Ejecutar la Aplicación**

```bash
python main.py
```

---

### **Paso 2: Reproducir el Problema**

1. **Ve a**: Dashboard → Administración → Gestionar Roles
2. **Selecciona**: "Gerente de Personal" (o cualquier rol)
3. **Click en**: 🔓 Permisos
4. **Marca algunos checkboxes** (los que están en VERDE ahora)
5. **Click en**: 💾 Guardar Permisos

---

### **Paso 3: Observar los Logs en la Consola**

Deberías ver algo como esto:

```
================================================================================
💾 GUARDAR PERMISOS - INICIADO
================================================================================

🔍 DIAGNÓSTICO DE VARIABLES:
   Total de permission_vars: 60
   Tipo de permission_vars: <class 'dict'>

📊 PERMISOS SELECCIONADOS: X/60

🔍 ESTADO DE VARIABLES (primeros 10):
   users.view: True (tipo: <class 'tkinter.BooleanVar'>)
   users.create: False (tipo: <class 'tkinter.BooleanVar'>)
   users.edit: True (tipo: <class 'tkinter.BooleanVar'>)
   ...

📝 LISTA DE PERMISOS SELECCIONADOS:
   ✓ users.view
   ✓ users.edit
   ...

🔧 GUARDANDO EN self.result...
✅ self.result establecido
   Tipo: <class 'list'>
   Longitud: X
   Contenido (primeros 5): ['users.view', 'users.edit', ...]
   self.result is None: False
   bool(self.result): True
================================================================================

🔒 Cerrando diálogo...
✅ Diálogo cerrado

================================================================================
📥 DIÁLOGO CERRADO - PROCESANDO RESULTADO
================================================================================
🔍 Tipo de dialog.result: <class 'list'>
📊 Valor de dialog.result: ['users.view', 'users.edit', ...]

✅ dialog.result NO es None
📏 Longitud: X

✅ ENTRANDO AL BLOQUE DE ACTUALIZACIÓN
📝 Permisos a guardar: ['users.view', 'users.edit', ...]
📌 Actualizando permisos del rol 3

DEBUG UPDATE_ROLE - Actualizando rol ID: 3

================================================================================
🔄 ROLE_MODEL.UPDATE_ROLE - INICIADO
================================================================================
📌 Role ID: 3
📦 Datos recibidos: {'permissions': ['users.view', ...]}
...
```

---

## 🚨 **ESCENARIOS POSIBLES**

### **Escenario A: `self.result` está vacío (longitud 0)**

```
📊 PERMISOS SELECCIONADOS: 0/60
✅ self.result establecido
   Longitud: 0
   bool(self.result): False
```

**PROBLEMA**: Las variables `BooleanVar` NO se están actualizando cuando haces click en los checkboxes.

**CAUSA**: El callback `command` del checkbox no está funcionando.

**SOLUCIÓN**: Revisar si los checkboxes tienen el callback configurado correctamente.

---

### **Escenario B: `dialog.result` es None**

```
🔍 Tipo de dialog.result: <class 'NoneType'>
📊 Valor de dialog.result: None
❌ dialog.result ES None
```

**PROBLEMA**: `self.result` no se está transfiriendo al objeto `dialog`.

**CAUSA**: Posible problema con la referencia del diálogo.

---

### **Escenario C: No entra al bloque de actualización**

```
⚠️ NO ENTRA AL BLOQUE DE ACTUALIZACIÓN
   Razón: dialog.result es []
   Lista vacía: True
```

**PROBLEMA**: `dialog.result` es una lista vacía.

**CAUSA**: Los checkboxes NO están marcados (todas las variables en False).

---

### **Escenario D: UPDATE retorna False**

```
✅ ENTRANDO AL BLOQUE DE ACTUALIZACIÓN
...
📊 RESULTADO DE UPDATE_ROLE:
   Success: False
   Message: Errores de validación: ...
```

**PROBLEMA**: La validación está rechazando los permisos.

**CAUSA**: Permisos inválidos o problema en la validación.

---

## 📝 **QUÉ REPORTAR**

Por favor, **copia y pega** la salida completa de la consola desde:

```
💾 GUARDAR PERMISOS - INICIADO
```

Hasta:

```
📊 RESULTADO DE UPDATE_ROLE:
```

Esto me dirá exactamente dónde está fallando el proceso.

---

## 🔧 **PRUEBAS ADICIONALES**

### **Prueba 1: Verificar que los checkboxes cambian de estado**

Cuando haces click en un checkbox, debería cambiar visualmente de:
- ☐ (sin marcar) a ☑️ (marcado con checkmark verde)

Si NO cambia visualmente, el problema es en el widget del checkbox.

---

### **Prueba 2: Verificar cuántos permisos están marcados**

Mira el contador en la esquina superior derecha:
- Debería cambiar de `0/60` a `X/60` cuando marcas checkboxes

Si NO cambia, los callbacks no están funcionando.

---

### **Prueba 3: Marcar "Seleccionar Todo"**

1. Click en botón "✅ Seleccionar Todo"
2. Deberías ver `60/60 permisos`
3. Guardar

Si esto funciona pero marcar individualmente no, el problema está en los checkboxes individuales.

---

## 🎯 **SIGUIENTE PASO**

**Ejecuta la aplicación** y **comparte los logs completos** de la consola.

Con eso podré identificar exactamente en qué paso se está perdiendo la información.

---

*Creado: 28 de octubre de 2025*
