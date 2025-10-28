# Script de instalación para módulo de reportes
# Ejecutar: .\install_reports_dependencies.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INSTALACIÓN MÓDULO DE REPORTES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Instalando dependencias necesarias..." -ForegroundColor Yellow
Write-Host ""

# Instalar tkcalendar
Write-Host "1️⃣ Instalando tkcalendar (widget de calendario)..." -ForegroundColor Green
pip install tkcalendar

Write-Host ""
Write-Host "2️⃣ Instalando matplotlib (gráficos)..." -ForegroundColor Green
pip install matplotlib

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Verificando instalación..." -ForegroundColor Yellow
Write-Host ""

pip list | Select-String "tkcalendar"
pip list | Select-String "matplotlib"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎉 ¡TODO LISTO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora puedes:" -ForegroundColor White
Write-Host "  1. Ejecutar main.py" -ForegroundColor White
Write-Host "  2. Ir al menú Reportes" -ForegroundColor White
Write-Host "  3. Generar tu primer reporte" -ForegroundColor White
Write-Host ""
Write-Host "📚 Lee REPORTS_MODULE_README.md para más información" -ForegroundColor Cyan
Write-Host ""
