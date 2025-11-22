# 🚀 ViajeIA - Guía de Despliegue

## ✅ Preparación Completada

Tu proyecto está **listo para desplegar** en Vercel y Render. Se han realizado las siguientes configuraciones:

### 📁 Archivos de Configuración Creados

1. **Frontend:**
   - ✅ `frontend/src/config.js` - Configuración de API URL con variables de entorno
   - ✅ `frontend/vercel.json` - Configuración específica de Vercel
   - ✅ `frontend/.env.example` - Plantilla de variables de entorno

2. **Backend:**
   - ✅ `backend/Procfile` - Para servicios como Render/Heroku
   - ✅ `render.yaml` - Configuración automática de Render
   - ✅ Variables de entorno configuradas en el código

3. **General:**
   - ✅ `vercel.json` - Configuración principal de Vercel
   - ✅ `.gitignore` - Actualizado para producción

### 🔧 Cambios Realizados en el Código

1. **Frontend (`frontend/src/App.js`):**
   - ✅ Configuración de axios con URL base desde variables de entorno
   - ✅ Uso de `config.js` para manejar URLs de API

2. **Backend (`backend/main.py`):**
   - ✅ CORS configurado para permitir conexiones desde cualquier origen en producción
   - ✅ API keys ahora usan variables de entorno (más seguro)
   - ✅ Soporte para `ALLOWED_ORIGINS` desde variables de entorno

---

## 📚 Documentación Disponible

### 1. **GUIA_DESPLIEGUE_VERCEL.md** (Recomendado)
   - Guía completa paso a paso
   - Instrucciones detalladas para GitHub, Render y Vercel
   - Solución de problemas comunes
   - Configuración de dominio personalizado

### 2. **DESPLIEGUE_RAPIDO.md**
   - Resumen ejecutivo
   - Pasos rápidos (30 minutos)
   - Checklist final

---

## 🎯 Próximos Pasos

### Paso 1: Subir a GitHub
```powershell
git init
git add .
git commit -m "Preparado para despliegue en Vercel y Render"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/viajeia.git
git push -u origin main
```

### Paso 2: Desplegar Backend en Render
1. Ve a [render.com](https://render.com)
2. Crea un nuevo Web Service
3. Conecta tu repositorio de GitHub
4. Configura las variables de entorno (ver `GUIA_DESPLIEGUE_VERCEL.md`)
5. Deploy

### Paso 3: Desplegar Frontend en Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Importa tu proyecto desde GitHub
3. Configura `REACT_APP_API_URL` con la URL de tu backend
4. Deploy

---

## 🔑 Variables de Entorno Necesarias

### Backend (Render):
```
GEMINI_API_KEY=AIzaSyCKLNkxnhxWqbzDFlN5pxgpuuhziINi9Wo
OPENWEATHER_API_KEY=03248d23bd5ad5a2cdf438702eaf90df
UNSPLASH_ACCESS_KEY=4aAIVujx9_CZOOm2xUNIpfT2uK_aOyeSDqYT7RuLQno
UNSPLASH_SECRET_KEY=aulHfu35e6QxnLQGC-sGwPSL0-yZjNIvpOyuEzIFOKY
ALLOWED_ORIGINS=*
```

### Frontend (Vercel):
```
REACT_APP_API_URL=https://viajeia-backend.onrender.com
```
*(Reemplaza con la URL real de tu backend)*

---

## ⚠️ Notas Importantes

1. **Render Free Tier:**
   - Los servicios gratuitos se "duermen" después de 15 minutos de inactividad
   - La primera petición después del sleep puede tardar 30-60 segundos
   - Considera usar el plan pago si necesitas mejor rendimiento

2. **Vercel Free Tier:**
   - Perfecto para frontend React
   - Despliegues automáticos desde GitHub
   - SSL/HTTPS incluido

3. **Seguridad:**
   - Las API keys están en el código como fallback para desarrollo local
   - En producción, siempre usa variables de entorno
   - No subas archivos `.env` con keys reales a GitHub

---

## 🆘 Soporte

Si encuentras problemas durante el despliegue:

1. Revisa los logs en Render/Vercel
2. Consulta `GUIA_DESPLIEGUE_VERCEL.md` - Sección "Solución de Problemas"
3. Verifica que todas las variables de entorno estén configuradas
4. Asegúrate de que el backend esté "Live" antes de probar el frontend

---

## 🎉 ¡Listo para Desplegar!

Tu aplicación está completamente preparada. Sigue la guía en `GUIA_DESPLIEGUE_VERCEL.md` para el proceso completo.

**¡Buena suerte con tu despliegue!** 🚀

