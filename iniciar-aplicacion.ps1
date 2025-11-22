# Script para iniciar automáticamente Backend y Frontend de ViajeIA
# Ejecuta: .\iniciar-aplicacion.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ViajeIA - Iniciando Aplicación" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurar PATH para Node.js
$env:Path = "C:\Program Files\nodejs;" + $env:Path

# Obtener la ruta del script actual
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "$scriptPath\backend\main.py")) {
    Write-Host "Error: No se encuentra backend/main.py" -ForegroundColor Red
    Write-Host "Asegúrate de ejecutar este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "$scriptPath\frontend\package.json")) {
    Write-Host "Error: No se encuentra frontend/package.json" -ForegroundColor Red
    Write-Host "Asegúrate de ejecutar este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Verificación de archivos completada" -ForegroundColor Green
Write-Host ""

# Iniciar Backend
Write-Host "Iniciando Backend (Python FastAPI)..." -ForegroundColor Yellow
$backendPath = "$scriptPath\backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host '=== BACKEND - ViajeIA ===' -ForegroundColor Green; Write-Host 'Servidor en: http://localhost:8000' -ForegroundColor Cyan; Write-Host ''; python main.py" -WindowStyle Normal

# Esperar un poco para que el backend inicie
Start-Sleep -Seconds 2

# Iniciar Frontend
Write-Host "Iniciando Frontend (React)..." -ForegroundColor Yellow
$frontendPath = "$scriptPath\frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; `$env:Path = 'C:\Program Files\nodejs;' + `$env:Path; Write-Host '=== FRONTEND - ViajeIA ===' -ForegroundColor Green; Write-Host 'Aplicación en: http://localhost:3000' -ForegroundColor Cyan; Write-Host ''; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Aplicación iniciada correctamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Se abrirán dos ventanas de PowerShell:" -ForegroundColor Yellow
Write-Host "  - Una para el Backend" -ForegroundColor White
Write-Host "  - Una para el Frontend" -ForegroundColor White
Write-Host ""
Write-Host "Presiona Ctrl+C en cada ventana para detener los servicios" -ForegroundColor Yellow
Write-Host ""

