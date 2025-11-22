# Script para detener Backend y Frontend de ViajeIA
# Ejecuta: .\detener-aplicacion.ps1

Write-Host "Deteniendo servicios de ViajeIA..." -ForegroundColor Yellow
Write-Host ""

# Detener procesos de Python (Backend)
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*ViajeIA*" -or $_.CommandLine -like "*main.py*" }
if ($pythonProcesses) {
    Write-Host "Deteniendo Backend..." -ForegroundColor Yellow
    $pythonProcesses | Stop-Process -Force
    Write-Host "✓ Backend detenido" -ForegroundColor Green
} else {
    Write-Host "Backend no estaba ejecutándose" -ForegroundColor Gray
}

# Detener procesos de Node (Frontend)
$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*react-scripts*" }
if ($nodeProcesses) {
    Write-Host "Deteniendo Frontend..." -ForegroundColor Yellow
    $nodeProcesses | Stop-Process -Force
    Write-Host "✓ Frontend detenido" -ForegroundColor Green
} else {
    Write-Host "Frontend no estaba ejecutándose" -ForegroundColor Gray
}

# Detener procesos de uvicorn (si están corriendo)
$uvicornProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" }
if ($uvicornProcesses) {
    Write-Host "Deteniendo servidor uvicorn..." -ForegroundColor Yellow
    $uvicornProcesses | Stop-Process -Force
    Write-Host "✓ Servidor uvicorn detenido" -ForegroundColor Green
}

Write-Host ""
Write-Host "Servicios detenidos" -ForegroundColor Green
Write-Host ""
Write-Host "Nota: Si las ventanas de PowerShell/CMD siguen abiertas, ciérralas manualmente" -ForegroundColor Yellow

