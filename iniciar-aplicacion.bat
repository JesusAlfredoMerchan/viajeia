@echo off
REM Script para iniciar automáticamente Backend y Frontend de ViajeIA
REM Ejecuta: iniciar-aplicacion.bat

echo ========================================
echo   ViajeIA - Iniciando Aplicacion
echo ========================================
echo.

REM Configurar PATH para Node.js
set PATH=C:\Program Files\nodejs;%PATH%

REM Obtener la ruta del script
set SCRIPT_DIR=%~dp0

REM Verificar archivos
if not exist "%SCRIPT_DIR%backend\main.py" (
    echo Error: No se encuentra backend/main.py
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

if not exist "%SCRIPT_DIR%frontend\package.json" (
    echo Error: No se encuentra frontend/package.json
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

echo Verificacion de archivos completada
echo.

REM Iniciar Backend en nueva ventana
echo Iniciando Backend (Python FastAPI)...
start "ViajeIA - Backend" cmd /k "cd /d %SCRIPT_DIR%backend && echo === BACKEND - ViajeIA === && echo Servidor en: http://localhost:8000 && echo. && python main.py"

REM Esperar un poco
timeout /t 2 /nobreak >nul

REM Iniciar Frontend en nueva ventana
echo Iniciando Frontend (React)...
start "ViajeIA - Frontend" cmd /k "cd /d %SCRIPT_DIR%frontend && set PATH=C:\Program Files\nodejs;%PATH% && echo === FRONTEND - ViajeIA === && echo Aplicacion en: http://localhost:3000 && echo. && npm start"

echo.
echo ========================================
echo   Aplicacion iniciada correctamente
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Se abrieron dos ventanas de CMD:
echo   - Una para el Backend
echo   - Una para el Frontend
echo.
echo Presiona Ctrl+C en cada ventana para detener los servicios
echo.
pause

