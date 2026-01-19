# ============================================================================
# Script de Migración de Archivos SQL Antiguos
# Sistema POS - Organización de Base de Datos
# ============================================================================
# Este script mueve los archivos antiguos a la carpeta 'archived'
# ============================================================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ORGANIZACIÓN DE ARCHIVOS SQL - POS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Obtener directorio actual del script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$databasePath = $scriptPath
$archivedPath = Join-Path $databasePath "archived"

# Verificar que estamos en el directorio correcto
if (-not (Test-Path (Join-Path $databasePath "scriptDB.txt"))) {
    Write-Host "❌ ERROR: No se encuentra scriptDB.txt" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde la carpeta database/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "📁 Directorio de trabajo: $databasePath" -ForegroundColor Gray
Write-Host ""

# Crear carpeta archived si no existe
if (-not (Test-Path $archivedPath)) {
    New-Item -ItemType Directory -Path $archivedPath | Out-Null
    Write-Host "✅ Carpeta 'archived' creada" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Carpeta 'archived' ya existe" -ForegroundColor Gray
}

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "Archivos a Archivar:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

# Lista de archivos a mover
$filesToArchive = @(
    "add_roles_system.sql",
    "add_user_sessions_table.sql",
    "create_products_tables.sql",
    "update_user_types.sql",
    "init_database.sql"  # Primera versión del unificado
)

$movedCount = 0
$skippedCount = 0

foreach ($file in $filesToArchive) {
    $sourcePath = Join-Path $databasePath $file
    $destPath = Join-Path $archivedPath $file
    
    if (Test-Path $sourcePath) {
        # Verificar si ya existe en destino
        if (Test-Path $destPath) {
            Write-Host "⚠️  $file" -ForegroundColor Yellow -NoNewline
            Write-Host " (ya existe en archived, omitiendo)" -ForegroundColor Gray
            $skippedCount++
        } else {
            # Mover archivo
            Move-Item -Path $sourcePath -Destination $destPath
            Write-Host "✅ $file" -ForegroundColor Green -NoNewline
            Write-Host " → archived/" -ForegroundColor Gray
            $movedCount++
        }
    } else {
        Write-Host "ℹ️  $file" -ForegroundColor Gray -NoNewline
        Write-Host " (no encontrado, omitiendo)" -ForegroundColor DarkGray
        $skippedCount++
    }
}

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "Archivos Principales (Mantener):" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan

# Lista de archivos que deben permanecer
$mainFiles = @(
    "scriptDB.txt",
    "init_database_compatible.sql",
    "connection.py",
    "er_diagram_dbdiagram.txt",
    "README_SCRIPTS_SQL.md",
    "ANALISIS_COMPLETO.md"
)

foreach ($file in $mainFiles) {
    $filePath = Join-Path $databasePath $file
    if (Test-Path $filePath) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️  $file (no encontrado)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "           RESUMEN DE OPERACIÓN" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Archivos movidos a 'archived': $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
Write-Host "Archivos omitidos: $skippedCount" -ForegroundColor Gray
Write-Host ""

if ($movedCount -gt 0) {
    Write-Host "✅ Organización completada exitosamente" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No se movieron archivos (ya organizados)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "Próximos Pasos:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "1. Revisar README_SCRIPTS_SQL.md para documentación completa" -ForegroundColor White
Write-Host "2. Ejecutar scriptDB.txt si es instalación nueva" -ForegroundColor White
Write-Host "3. Ejecutar init_database_compatible.sql para agregar roles" -ForegroundColor White
Write-Host "4. Verificar con las consultas del README" -ForegroundColor White
Write-Host ""

# Mostrar contenido de archived si hay archivos
if ($movedCount -gt 0) {
    Write-Host "📦 Contenido de 'archived/':" -ForegroundColor Cyan
    Get-ChildItem -Path $archivedPath -Filter "*.sql" | ForEach-Object {
        Write-Host "   - $($_.Name)" -ForegroundColor Gray
    }
    Write-Host ""
}

Write-Host "Presiona Enter para salir..." -ForegroundColor Gray
Read-Host

