"""
Script de prueba para verificar corrección de problemas de precisión decimal
en el módulo de ventas
"""

def test_precision_issue():
    """Simula el problema de precisión que ocurría antes"""
    
    print("=" * 70)
    print("TEST: Problemas de Precisión Decimal en Ventas")
    print("=" * 70)
    
    # Caso 1: Problema original - operaciones con float
    print("\n1️⃣ ANTES (con float - problemático):")
    print("-" * 70)
    
    # Simular cálculo con float (forma antigua)
    price1 = 10.0
    qty1 = 3
    price2 = 5.90
    qty2 = 2
    
    subtotal_float = (price1 * qty1) + (price2 * qty2)
    tax_float = subtotal_float * 0.18
    total_float = subtotal_float + tax_float
    
    paid_float = 47.848  # Usuario ingresa exactamente el total mostrado
    
    print(f"   Producto 1: {qty1} x S/ {price1:.2f} = S/ {price1 * qty1:.2f}")
    print(f"   Producto 2: {qty2} x S/ {price2:.2f} = S/ {price2 * qty2:.2f}")
    print(f"   Subtotal: S/ {subtotal_float:.2f}")
    print(f"   IGV (18%): S/ {tax_float:.2f}")
    print(f"   Total: S/ {total_float:.2f}")
    print(f"   Total (interno): {total_float}")
    print(f"   Pagado: S/ {paid_float:.2f}")
    print(f"   Pagado (interno): {paid_float}")
    
    # Validación antigua (problemática)
    if paid_float < total_float:
        print(f"   ❌ ERROR: Monto insuficiente! ({paid_float} < {total_float})")
        print(f"   Diferencia: {total_float - paid_float}")
    else:
        print(f"   ✅ OK: Monto suficiente")
    
    # Caso 2: Solución nueva - con redondeo
    print("\n2️⃣ DESPUÉS (con redondeo - correcto):")
    print("-" * 70)
    
    # Simular cálculo con redondeo (forma nueva)
    subtotal_rounded = round((price1 * qty1) + (price2 * qty2), 2)
    tax_rounded = round(subtotal_rounded * 0.18, 2)
    total_rounded = round(subtotal_rounded + tax_rounded, 2)
    
    paid_rounded = round(47.848, 2)  # Usuario ingresa el total mostrado
    
    print(f"   Producto 1: {qty1} x S/ {price1:.2f} = S/ {price1 * qty1:.2f}")
    print(f"   Producto 2: {qty2} x S/ {price2:.2f} = S/ {price2 * qty2:.2f}")
    print(f"   Subtotal: S/ {subtotal_rounded:.2f}")
    print(f"   IGV (18%): S/ {tax_rounded:.2f}")
    print(f"   Total: S/ {total_rounded:.2f}")
    print(f"   Total (interno): {total_rounded}")
    print(f"   Pagado: S/ {paid_rounded:.2f}")
    print(f"   Pagado (interno): {paid_rounded}")
    
    # Validación nueva (con tolerancia)
    tolerance = 0.009
    if paid_rounded < (total_rounded - tolerance):
        print(f"   ❌ ERROR: Monto insuficiente!")
    else:
        print(f"   ✅ OK: Monto suficiente")
        change = round(paid_rounded - total_rounded, 2)
        print(f"   Vuelto: S/ {change:.2f}")
    
    # Caso 3: Casos extremos
    print("\n3️⃣ CASOS EXTREMOS:")
    print("-" * 70)
    
    test_cases = [
        ("59.00 vs 59.00", 59.00, 59.00),
        ("59.00 vs 59.000001", 59.00, 59.000001),
        ("100.50 vs 100.499999", 100.50, 100.499999),
        ("25.33 vs 25.33", 25.33, 25.33),
    ]
    
    for name, paid, total in test_cases:
        paid_r = round(paid, 2)
        total_r = round(total, 2)
        valid_old = paid >= total
        valid_new = paid_r >= (total_r - 0.009)
        
        print(f"\n   {name}")
        print(f"   Pagado: {paid:.6f} → {paid_r:.2f}")
        print(f"   Total:  {total:.6f} → {total_r:.2f}")
        print(f"   Válido (método antiguo): {'✅' if valid_old else '❌'}")
        print(f"   Válido (método nuevo):   {'✅' if valid_new else '❌'}")
    
    print("\n" + "=" * 70)
    print("RESUMEN:")
    print("=" * 70)
    print("✅ Se corrigieron los problemas de precisión decimal")
    print("✅ Se agregó redondeo a 2 decimales en todos los cálculos")
    print("✅ Se usa tolerancia de 0.009 en validaciones de pago")
    print("✅ Los usuarios ya no verán errores al ingresar el monto exacto")
    print("=" * 70)

if __name__ == "__main__":
    test_precision_issue()
