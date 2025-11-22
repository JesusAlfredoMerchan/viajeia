# ViajeIA - Tu Asistente Personal de Viajes

Aplicación web moderna para planificación de viajes con arquitectura separada de frontend y backend.

## 🏗️ Estructura del Proyecto

```
ViajeIA/
├── frontend/          # Aplicación React
│   ├── public/
│   ├── src/
│   └── package.json
└── backend/           # API Python con FastAPI
    ├── main.py
    └── requirements.txt
```

## 🚀 Instalación y Ejecución

### ⚡ Inicio Rápido (Recomendado)

Para iniciar automáticamente tanto el backend como el frontend:

**Opción 1: PowerShell (Recomendado)**
```powershell
.\iniciar-aplicacion.ps1
```

**Opción 2: CMD/Batch**
```cmd
iniciar-aplicacion.bat
```

Esto abrirá dos ventanas separadas, una para cada servicio.

Para detener los servicios:
```powershell
.\detener-aplicacion.ps1
```

---

### Instalación Manual

### Backend (Python)

1. Navega a la carpeta backend:
```bash
cd backend
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activa el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecuta el servidor:
```bash
python main.py
```

El backend estará disponible en `http://localhost:8000`

### Frontend (React)

1. Navega a la carpeta frontend:
```bash
cd frontend
```

2. **Si usas PowerShell y tienes problemas con la política de ejecución**, ejecuta primero:
```powershell
$env:Path = "C:\Program Files\nodejs;" + $env:Path
```

3. Instala las dependencias:
```bash
npm install
```

4. Ejecuta la aplicación:
```bash
npm start
```

El frontend estará disponible en `http://localhost:3000`

> **Nota:** Si encuentras problemas con npm en PowerShell, consulta el archivo `SOLUCION_NPM.md` para más alternativas.

## 🎨 Características

- ✨ Interfaz moderna con diseño azul y blanco
- 💬 Campo de texto para preguntas sobre viajes
- 🚀 Botón "Planificar mi viaje" para enviar consultas
- 📝 Área de respuestas para mostrar las sugerencias
- 🔄 Integración entre frontend y backend
- 🤖 **Powered by Google Gemini 2.5 Flash** - Respuestas inteligentes sobre viajes

## 🛠️ Tecnologías

- **Frontend**: React 18
- **Backend**: Python con FastAPI
- **IA**: Google Gemini 2.5 Flash
- **Estilos**: CSS moderno con gradientes

## 📝 Notas

- Asegúrate de tener Node.js y Python instalados
- El backend debe estar ejecutándose antes de usar el frontend
- El proxy está configurado para redirigir las peticiones del frontend al backend
- Si tienes problemas con npm en PowerShell, consulta `SOLUCION_NPM.md`
- **Importante**: Después de actualizar el código, instala las nuevas dependencias: `pip install -r requirements.txt` en la carpeta backend

## 🎯 Scripts de Inicio Rápido

- `iniciar-aplicacion.ps1` - Inicia backend y frontend automáticamente (PowerShell)
- `iniciar-aplicacion.bat` - Inicia backend y frontend automáticamente (CMD)
- `detener-aplicacion.ps1` - Detiene todos los servicios

