# 🔐 Configuración de Variables de Entorno

## Para Desarrollo Local

### Crear archivo `.env`

1. En la carpeta `backend/`, crea un archivo llamado `.env`
2. Agrega las siguientes variables:

```env
# API Key de Gemini (obtén una en: https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=tu_api_key_de_gemini_aqui

# API Key de OpenWeatherMap
OPENWEATHER_API_KEY=03248d23bd5ad5a2cdf438702eaf90df

# API Key de Unsplash
UNSPLASH_ACCESS_KEY=4aAIVujx9_CZOOm2xUNIpfT2uK_aOyeSDqYT7RuLQno
UNSPLASH_SECRET_KEY=aulHfu35e6QxnLQGC-sGwPSL0-yZjNIvpOyuEzIFOKY

# Orígenes permitidos para CORS (para desarrollo local)
ALLOWED_ORIGINS=http://localhost:3000
```

### ⚠️ Importante

- El archivo `.env` NO se sube a GitHub (está en `.gitignore`)
- Reemplaza `tu_api_key_de_gemini_aqui` con tu API key real
- Nunca compartas tu API key públicamente

### Cargar Variables de Entorno

El backend cargará automáticamente las variables del archivo `.env` cuando uses:

```bash
python main.py
```

O si usas un gestor de entorno virtual, asegúrate de que esté activado antes de ejecutar.

---

## Para Producción (Render)

Las variables de entorno se configuran en:
- Render Dashboard → Tu Servicio → Settings → Environment Variables

No necesitas crear un archivo `.env` en producción.

