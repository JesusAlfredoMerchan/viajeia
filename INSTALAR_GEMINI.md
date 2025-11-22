# 🤖 Integración con Gemini AI

La aplicación ahora está conectada con Google Gemini 1.5 Flash para proporcionar respuestas inteligentes sobre viajes.

> **Nota:** Usamos `gemini-1.5-flash` porque es el modelo recomendado para el tier gratuito y tiene mejores límites de cuota que las versiones experimentales.

## 📦 Instalación de Dependencias

Para que funcione la integración con Gemini, necesitas instalar la nueva dependencia:

### Opción 1: Desde la raíz del proyecto
```powershell
cd backend
pip install -r requirements.txt
```

### Opción 2: Instalar directamente
```powershell
pip install google-generativeai==0.3.2
```

## ✅ Verificación

Una vez instalado, reinicia el backend:

```powershell
cd backend
python main.py
```

Deberías ver el mensaje: "ViajeIA API está funcionando con Gemini"

## 🎯 Cómo Funciona

1. El usuario escribe una pregunta sobre viajes en el frontend
2. La pregunta se envía al backend
3. El backend la procesa con Gemini 2.5 Flash
4. La respuesta inteligente de Gemini se muestra en pantalla

## 🔑 API Key

La API Key de Gemini ya está configurada en el código. Si necesitas cambiarla en el futuro, edita el archivo `backend/main.py` y busca la variable `GEMINI_API_KEY`.

## 🚀 Uso

Simplemente escribe cualquier pregunta sobre viajes y presiona "Planificar mi viaje". Gemini responderá con recomendaciones inteligentes y personalizadas.

Ejemplos de preguntas:
- "¿Qué hoteles recomiendas en París?"
- "Cómo planificar un viaje a Japón con presupuesto limitado"
- "Mejores restaurantes en Barcelona"
- "Itinerario de 5 días en Roma"

