# 🚀 Despliegue Rápido - ViajeIA

## Resumen Ejecutivo

Esta guía te ayudará a desplegar ViajeIA en **menos de 30 minutos** usando servicios gratuitos.

---

## 📦 Archivos Creados para el Despliegue

✅ **Configuración Frontend:**
- `frontend/src/config.js` - Configuración de API URL
- `frontend/vercel.json` - Configuración de Vercel
- `frontend/.env.example` - Ejemplo de variables de entorno

✅ **Configuración Backend:**
- `backend/Procfile` - Para Render/Heroku
- `render.yaml` - Configuración de Render

✅ **Configuración General:**
- `vercel.json` - Configuración principal de Vercel
- `.gitignore` - Actualizado para producción

✅ **Documentación:**
- `GUIA_DESPLIEGUE_VERCEL.md` - Guía completa paso a paso

---

## ⚡ Pasos Rápidos

### 1. Subir a GitHub (5 minutos)

```powershell
git init
git add .
git commit -m "Preparado para despliegue"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/viajeia.git
git push -u origin main
```

### 2. Desplegar Backend en Render (10 minutos)

1. Ve a [render.com](https://render.com)
2. New → Web Service
3. Conecta tu repo de GitHub
4. Configura:
   - **Name:** `viajeia-backend`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agrega variables de entorno (ver `GUIA_DESPLIEGUE_VERCEL.md`)
6. Deploy

### 3. Desplegar Frontend en Vercel (5 minutos)

1. Ve a [vercel.com](https://vercel.com)
2. Import Project
3. Selecciona tu repo de GitHub
4. Configura:
   - **Root Directory:** `frontend`
   - **Framework:** Create React App
5. Agrega variable de entorno:
   - `REACT_APP_API_URL` = URL de tu backend en Render
6. Deploy

### 4. Actualizar vercel.json (2 minutos)

Edita `vercel.json` y actualiza la URL del backend en la sección `rewrites`.

---

## ✅ Checklist Final

- [ ] Código subido a GitHub
- [ ] Backend desplegado en Render
- [ ] Frontend desplegado en Vercel
- [ ] Variables de entorno configuradas
- [ ] Aplicación funcionando correctamente

---

## 🔗 URLs Importantes

- **Frontend:** `https://viajeia.vercel.app`
- **Backend:** `https://viajeia-backend.onrender.com`

---

## 📚 Documentación Completa

Para instrucciones detalladas, consulta: **`GUIA_DESPLIEGUE_VERCEL.md`**

