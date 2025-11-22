# 🚀 Guía Completa: Desplegar ViajeIA en Vercel (GRATIS)

Esta guía te llevará paso a paso para subir tu aplicación ViajeIA a internet usando Vercel, completamente gratis.

---

## 📋 Requisitos Previos

1. ✅ Cuenta de GitHub (gratis): [https://github.com](https://github.com)
2. ✅ Cuenta de Vercel (gratis): [https://vercel.com](https://vercel.com)
3. ✅ Cuenta de Render (gratis para backend): [https://render.com](https://render.com)
4. ✅ Git instalado en tu computadora

---

## 🎯 PASO 1: Preparar el Proyecto

### 1.1 Verificar que tienes Git instalado

Abre PowerShell y ejecuta:
```powershell
git --version
```

Si no está instalado, descárgalo de: [https://git-scm.com](https://git-scm.com)

### 1.2 Inicializar Git en tu proyecto

```powershell
cd "C:\Users\Improtecsa\Desktop\Curso\ViajeIA - Tu Asistente Personal de Viajes"
git init
```

### 1.3 Crear archivo .env.example para el frontend

Crea un archivo `frontend/.env.example` con:
```
REACT_APP_API_URL=http://localhost:8000
```

### 1.4 Crear archivo .env.local para desarrollo local

Crea un archivo `frontend/.env.local` con:
```
REACT_APP_API_URL=http://localhost:8000
```

**⚠️ IMPORTANTE:** El archivo `.env.local` NO debe subirse a GitHub (ya está en .gitignore).

---

## 🎯 PASO 2: Subir el Código a GitHub

### 2.1 Crear un repositorio en GitHub

1. Ve a [https://github.com/new](https://github.com/new)
2. Nombre del repositorio: `viajeia` (o el que prefieras)
3. Descripción: "ViajeIA - Tu Asistente Personal de Viajes"
4. **NO marques** "Add a README file" (ya tienes uno)
5. Haz clic en **"Create repository"**

### 2.2 Conectar tu proyecto local con GitHub

En PowerShell, ejecuta estos comandos (reemplaza `TU_USUARIO` con tu usuario de GitHub):

```powershell
git add .
git commit -m "Primera versión de ViajeIA - Lista para desplegar"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/viajeia.git
git push -u origin main
```

**Nota:** GitHub te pedirá autenticación. Puedes usar:
- Token de acceso personal (recomendado)
- O autenticación con GitHub CLI

---

## 🎯 PASO 3: Desplegar el Backend en Render (GRATIS)

### 3.1 Crear cuenta en Render

1. Ve a [https://render.com](https://render.com)
2. Haz clic en **"Get Started for Free"**
3. Regístrate con tu cuenta de GitHub (es más fácil)

### 3.2 Crear un nuevo Web Service

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub (`viajeia`)
4. Configura el servicio:
   - **Name:** `viajeia-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`

### 3.3 Configurar Variables de Entorno en Render

En la sección **"Environment"**, agrega estas variables:

```
GEMINI_API_KEY=AIzaSyCKLNkxnhxWqbzDFlN5pxgpuuhziINi9Wo
OPENWEATHER_API_KEY=03248d23bd5ad5a2cdf438702eaf90df
UNSPLASH_ACCESS_KEY=4aAIVujx9_CZOOm2xUNIpfT2uK_aOyeSDqYT7RuLQno
UNSPLASH_SECRET_KEY=aulHfu35e6QxnLQGC-sGwPSL0-yZjNIvpOyuEzIFOKY
```

### 3.4 Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu backend
3. Espera 5-10 minutos (la primera vez tarda más)
4. Cuando termine, verás una URL como: `https://viajeia-backend.onrender.com`

**⚠️ IMPORTANTE:** Guarda esta URL, la necesitarás para el frontend.

### 3.5 Verificar que el backend funciona

Abre en tu navegador:
```
https://viajeia-backend.onrender.com/
```

Deberías ver: `{"message":"ViajeIA API está funcionando correctamente"}`

---

## 🎯 PASO 4: Desplegar el Frontend en Vercel (GRATIS)

### 4.1 Crear cuenta en Vercel

1. Ve a [https://vercel.com](https://vercel.com)
2. Haz clic en **"Sign Up"**
3. Regístrate con tu cuenta de GitHub (es más fácil)

### 4.2 Importar tu proyecto

1. En el dashboard de Vercel, haz clic en **"Add New..."**
2. Selecciona **"Project"**
3. Importa tu repositorio de GitHub (`viajeia`)

### 4.3 Configurar el proyecto

Vercel detectará automáticamente que es un proyecto React. Configura:

- **Framework Preset:** Create React App
- **Root Directory:** `frontend`
- **Build Command:** `npm run build` (o déjalo automático)
- **Output Directory:** `build`

### 4.4 Configurar Variables de Entorno

En la sección **"Environment Variables"**, agrega:

```
REACT_APP_API_URL=https://viajeia-backend.onrender.com
```

**⚠️ IMPORTANTE:** Reemplaza `viajeia-backend.onrender.com` con la URL real de tu backend en Render.

### 4.5 Desplegar

1. Haz clic en **"Deploy"**
2. Vercel comenzará a construir y desplegar tu frontend
3. Espera 2-5 minutos
4. Cuando termine, verás una URL como: `https://viajeia.vercel.app`

**🎉 ¡Tu aplicación está online!**

---

## 🎯 PASO 5: Actualizar la URL del Backend en el Código

### 5.1 Actualizar vercel.json

Edita el archivo `vercel.json` en la raíz del proyecto y actualiza la URL del backend:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://TU-BACKEND-URL.onrender.com/api/:path*"
    }
  ]
}
```

### 5.2 Hacer commit y push

```powershell
git add .
git commit -m "Actualizar URL del backend para producción"
git push
```

Vercel detectará automáticamente los cambios y redesplegará.

---

## 🎯 PASO 6: Configurar Dominio Personalizado (OPCIONAL)

### 6.1 En Vercel

1. Ve a tu proyecto en Vercel
2. Ve a **"Settings"** → **"Domains"**
3. Agrega tu dominio personalizado (ej: `viajeia.com`)
4. Sigue las instrucciones para configurar DNS

### 6.2 En Render

1. Ve a tu servicio en Render
2. Ve a **"Settings"** → **"Custom Domain"**
3. Agrega tu dominio personalizado
4. Configura los registros DNS según las instrucciones

---

## ✅ Verificación Final

### Checklist:

- [ ] Backend desplegado en Render y funcionando
- [ ] Frontend desplegado en Vercel y funcionando
- [ ] Variables de entorno configuradas correctamente
- [ ] La aplicación carga correctamente
- [ ] Puedes hacer preguntas y recibir respuestas
- [ ] Las fotos se cargan correctamente
- [ ] El clima se muestra correctamente

---

## 🔧 Solución de Problemas

### Problema: "CORS Error"

**Solución:** Verifica que en `backend/main.py` esté configurado:
```python
origins = ["*"]  # O especifica tu dominio de Vercel
```

### Problema: "API URL not found"

**Solución:** 
1. Verifica que la variable `REACT_APP_API_URL` esté configurada en Vercel
2. Verifica que el backend esté funcionando en Render
3. Espera unos minutos después de cambiar variables de entorno (Vercel necesita reconstruir)

### Problema: "Backend no responde"

**Solución:**
1. Verifica que el backend esté "Live" en Render
2. Render puede poner servicios gratuitos en "sleep" después de 15 minutos de inactividad
3. La primera petición después de sleep puede tardar 30-60 segundos

### Problema: "Build failed"

**Solución:**
1. Revisa los logs en Vercel/Render
2. Verifica que todas las dependencias estén en `package.json` y `requirements.txt`
3. Asegúrate de que no haya errores de sintaxis

---

## 📚 Recursos Adicionales

- **Documentación de Vercel:** [https://vercel.com/docs](https://vercel.com/docs)
- **Documentación de Render:** [https://render.com/docs](https://render.com/docs)
- **GitHub:** [https://github.com](https://github.com)

---

## 🎉 ¡Listo!

Tu aplicación ViajeIA ahora está online y accesible desde cualquier lugar del mundo. 

**URLs importantes:**
- Frontend: `https://viajeia.vercel.app` (o tu dominio personalizado)
- Backend: `https://viajeia-backend.onrender.com`

¡Comparte tu aplicación con el mundo! 🌍✈️

