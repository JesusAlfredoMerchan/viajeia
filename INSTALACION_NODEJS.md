# 📦 Guía de Instalación de Node.js para ViajeIA

## Pasos para Instalar Node.js en Windows

### Opción 1: Instalador Oficial (Recomendado)

1. **Descargar Node.js:**
   - Ve a: https://nodejs.org/
   - Descarga la versión **LTS (Long Term Support)** - es la más estable
   - El archivo será algo como `node-v20.x.x-x64.msi`

2. **Ejecutar el Instalador:**
   - Haz doble clic en el archivo descargado
   - Sigue el asistente de instalación
   - **IMPORTANTE:** Asegúrate de marcar la opción "Add to PATH" durante la instalación
   - Haz clic en "Next" hasta completar la instalación

3. **Verificar la Instalación:**
   - Cierra y vuelve a abrir PowerShell/Terminal
   - Ejecuta estos comandos para verificar:
   ```powershell
   node --version
   npm --version
   ```
   - Deberías ver números de versión (ej: v20.10.0 y 10.2.3)

4. **Instalar Dependencias del Frontend:**
   ```powershell
   cd frontend
   npm install
   ```

5. **Ejecutar el Frontend:**
   ```powershell
   npm start
   ```

### Opción 2: Usando Chocolatey (Si ya lo tienes instalado)

Si tienes Chocolatey instalado, puedes instalar Node.js con:
```powershell
choco install nodejs
```

### Opción 3: Usando winget (Windows 10/11)

```powershell
winget install OpenJS.NodeJS.LTS
```

## ⚠️ Notas Importantes

- Después de instalar Node.js, **cierra y vuelve a abrir PowerShell** para que los cambios surtan efecto
- Si después de instalar aún no funciona, reinicia tu computadora
- Node.js incluye npm automáticamente, no necesitas instalarlo por separado

## 🚀 Una vez instalado Node.js

Ejecuta estos comandos en orden:

1. **Backend (en una terminal):**
   ```powershell
   cd backend
   python main.py
   ```

2. **Frontend (en otra terminal):**
   ```powershell
   cd frontend
   npm install
   npm start
   ```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:3000`

