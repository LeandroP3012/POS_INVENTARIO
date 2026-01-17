# Script PowerShell para aplicar la corrección de IGV
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "APLICAR CORRECCION DE IGV EN REPORTES" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script agregara el campo 'include_tax' a la tabla 'sales'" -ForegroundColor Yellow
Write-Host ""

# Solicitar contraseña
$password = Read-Host "Ingresa la contraseña de MySQL (root)" -AsSecureString
$plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Ejecutar script SQL
Write-Host ""
Write-Host "Aplicando cambios a la base de datos..." -ForegroundColor Yellow

$sqlScript = Get-Content "database\add_include_tax_field.sql" -Raw

try {
    # Ejecutar usando mysql
    $sqlScript | mysql -u root -p"$plainPassword" pos_system 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host "CORRECCION APLICADA EXITOSAMENTE" -ForegroundColor Green
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Ahora puedes usar el sistema normalmente." -ForegroundColor Green
        Write-Host "Las ventas sin IGV se guardaran correctamente." -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "ERROR: No se pudo aplicar la correccion" -ForegroundColor Red
        Write-Host "Verifica que MySQL este corriendo y la contraseña sea correcta" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona Enter para continuar..."
Read-Host
