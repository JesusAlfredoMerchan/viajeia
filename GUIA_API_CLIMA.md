# 🌤️ Guía: Integración con OpenWeatherMap API

## 📝 Cómo Obtener tu API Key Gratuita

### Paso 1: Crear una Cuenta
1. Ve a: https://openweathermap.org/api
2. Haz clic en "Sign Up" (Registrarse) en la esquina superior derecha
3. Completa el formulario con:
   - Usuario
   - Email
   - Contraseña
   - Confirma que aceptas los términos

### Paso 2: Verificar tu Email
- Revisa tu bandeja de entrada (y spam)
- Haz clic en el enlace de verificación

### Paso 3: Obtener tu API Key
1. Inicia sesión en: https://home.openweathermap.org/
2. Ve a la sección "API Keys" en el menú
3. Verás una API Key por defecto (o puedes crear una nueva)
4. **Copia tu API Key** - la necesitarás para configurar la aplicación

### Paso 4: Activar el Plan Gratuito
- El plan "Free" está activado automáticamente
- Límites del plan gratuito:
  - 60 llamadas por minuto
  - 1,000,000 llamadas por mes
  - Acceso a datos actuales del clima

## 🔑 Configuración en ViajeIA

Una vez que tengas tu API Key, se configurará en el archivo `backend/main.py` en la variable `OpenWeatherMap`.

## 📊 Qué Información Obtendremos

La API nos proporcionará:
- Temperatura actual
- Descripción del clima (soleado, nublado, lluvioso, etc.)
- Sensación térmica
- Humedad
- Velocidad del viento
- Y más datos útiles para viajeros

## ✅ Listo para Usar

Una vez configurado, Alex automáticamente buscará el clima cuando menciones un destino en tus preguntas.

