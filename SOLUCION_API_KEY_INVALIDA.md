# 🔑 Solución: API Key Inválida de OpenWeatherMap

## Problema
Error 401: "Invalid API key" - La API key no es reconocida como válida.

## Solución Paso a Paso

### Paso 1: Verificar tu API Key en OpenWeatherMap

1. **Inicia sesión** en: https://home.openweathermap.org/
2. Ve a la sección **"API keys"** en el menú lateral
3. Verifica que tu API key aparezca en la lista
4. **IMPORTANTE:** Copia la API key COMPLETA desde el sitio web (no uses la que ya tienes)

### Paso 2: Generar una Nueva API Key (Recomendado)

Si la API key actual no funciona, genera una nueva:

1. En la página de API keys, haz clic en **"Generate"** o **"Create"**
2. Dale un nombre (ej: "ViajeIA")
3. **Copia la nueva API key** inmediatamente (solo se muestra una vez)
4. Espera 10-30 minutos para que se active

### Paso 3: Actualizar la API Key en el Código

1. Abre `backend/main.py`
2. Busca la línea 25:
   ```python
   WEATHER_API_KEY = "601714baa4a5b57143e20704e14050be"
   ```
3. Reemplaza con tu nueva API key:
   ```python
   WEATHER_API_KEY = "TU_NUEVA_API_KEY_AQUI"
   ```
4. **Asegúrate de:**
   - No dejar espacios
   - Copiar la API key completa
   - Usar comillas dobles

### Paso 4: Verificar que la API Key Funcione

1. Espera 10-30 minutos después de crear la API key
2. Prueba en el navegador (reemplaza TU_API_KEY):
   ```
   https://api.openweathermap.org/data/2.5/weather?q=London&appid=TU_API_KEY&units=metric
   ```
3. Si funciona, verás un JSON con datos del clima
4. Si sigue dando error 401, espera más tiempo o genera otra API key

### Paso 5: Reiniciar el Backend

```powershell
# Detén el backend (Ctrl+C)
cd backend
python main.py
```

### Paso 6: Probar

1. Visita: http://localhost:8000/test-weather
2. Debería mostrar el clima de London si todo está bien

## Verificaciones Importantes

- ✅ API key copiada directamente desde OpenWeatherMap (no de memoria)
- ✅ API key completa (sin espacios al inicio o final)
- ✅ Esperaste al menos 10-30 minutos después de crear la API key
- ✅ El backend fue reiniciado después de cambiar la API key
- ✅ La API key está marcada como "Active" en OpenWeatherMap

## Si Nada Funciona

1. **Genera una nueva API key** en OpenWeatherMap
2. **Espera 30-60 minutos** (a veces tarda más)
3. **Prueba la URL directamente** en el navegador antes de usarla en el código
4. Si después de 2 horas sigue sin funcionar, contacta el soporte de OpenWeatherMap

