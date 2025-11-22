# 🔧 Solución para Problemas con npm en PowerShell

## Problema
Si ves el error: "No se puede cargar el archivo npm.ps1 porque la ejecución de scripts está deshabilitada", aquí están las soluciones:

## ✅ Solución 1: Usar el PATH configurado (Recomendado)

En PowerShell, ejecuta este comando antes de usar npm:

```powershell
$env:Path = "C:\Program Files\nodejs;" + $env:Path
```

Luego puedes usar npm normalmente:
```powershell
npm install
npm start
```

## ✅ Solución 2: Usar el archivo .bat

He creado un archivo `ejecutar-npm.bat` en la carpeta frontend. Puedes usarlo así:

```powershell
.\ejecutar-npm.bat install
.\ejecutar-npm.bat start
```

O simplemente:
```cmd
ejecutar-npm install
ejecutar-npm start
```

## ✅ Solución 3: Usar cmd.exe en lugar de PowerShell

Abre **Símbolo del sistema** (cmd.exe) en lugar de PowerShell y ejecuta:
```cmd
cd frontend
npm install
npm start
```

## ✅ Solución 4: Cambiar política de ejecución (Requiere permisos de administrador)

Si tienes permisos de administrador, puedes cambiar la política de ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego cierra y vuelve a abrir PowerShell.

## 🚀 Comandos para Ejecutar la Aplicación

### Backend (Terminal 1):
```powershell
cd backend
python main.py
```

### Frontend (Terminal 2):
```powershell
cd frontend
$env:Path = "C:\Program Files\nodejs;" + $env:Path
npm start
```

La aplicación se abrirá automáticamente en `http://localhost:3000`

