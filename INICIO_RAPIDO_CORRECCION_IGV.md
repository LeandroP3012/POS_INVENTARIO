# ⚡ INSTRUCCIONES RÁPIDAS - Corrección IGV en Reportes

## 🚨 Problema
Los reportes muestran IGV en ventas que fueron hechas SIN IGV.

## ✅ Solución en 3 Pasos

### 1️⃣ Aplicar corrección a la base de datos

**Opción A: Usando el script batch (MÁS FÁCIL)**
```
Doble clic en: APLICAR_CORRECCION_IGV.bat
```

**Opción B: Desde línea de comandos**
```bash
cd C:\Users\USER\Desktop\POS
mysql -u root -p pos_system < database\add_include_tax_field.sql
```

### 2️⃣ Verificar que se aplicó correctamente
```bash
python verificar_correccion_igv.py
```

Deberías ver:
```
✅ Campo 'include_tax' encontrado
✅ Verificación completada exitosamente
✅ CORRECCIÓN APLICADA CORRECTAMENTE
```

### 3️⃣ Probar el sistema

1. Abre el sistema POS
2. Ve a "Nueva Venta"
3. **DESACTIVA el checkbox de IGV** (parte superior derecha)
4. Agrega un producto (ej: S/ 100.00)
5. Procesa la venta
6. Verifica que el total sea S/ 100.00 (SIN los S/ 18.00 de IGV)
7. Ve a Reportes → Reporte de Ventas
8. Verifica que la venta aparezca con IGV = S/ 0.00

---

## 📋 Checklist

- [ ] Ejecuté APLICAR_CORRECCION_IGV.bat
- [ ] Ejecuté verificar_correccion_igv.py
- [ ] Vi "✅ CORRECCIÓN APLICADA CORRECTAMENTE"
- [ ] Hice una venta SIN IGV de prueba
- [ ] El total fue correcto (sin IGV)
- [ ] El reporte muestra la venta sin IGV

---

## ⚠️ Si algo sale mal

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté corriendo
- Abre MySQL Workbench y conecta manualmente

### Error: "Access denied for user 'root'"
- La contraseña de MySQL es incorrecta
- Ejecuta el script SQL desde MySQL Workbench manualmente

### Error: "Unknown database 'pos_system'"
- La base de datos no existe
- Verifica el nombre de tu base de datos

---

## 📚 Documentación Completa

Para más detalles, consulta:
- **SOLUCION_REPORTES_IGV.md** - Guía completa
- **RESUMEN_CORRECCION_IGV.md** - Resumen ejecutivo

---

## 💡 ¿Qué cambia después de aplicar esto?

**ANTES:**
- Ventas sin IGV se guardaban con tax_amount > 0 ❌
- Reportes sumaban IGV de todas las ventas ❌

**DESPUÉS:**
- Ventas sin IGV se guardan con tax_amount = 0 ✅
- Reportes solo suman IGV de ventas que lo incluyen ✅
- Reportes separan ventas con/sin IGV ✅

---

**Tiempo estimado:** 5 minutos  
**¿Afecta ventas anteriores?** No, todas seguirán marcadas como "con IGV" (que es correcto)  
**¿Hay riesgo?** No, solo agrega funcionalidad
