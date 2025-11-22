# 🔧 Solución para Error 401 de OpenWeatherMap

## Problema
Error 401 (Unauthorized) al intentar usar la API de OpenWeatherMap.

## Posibles Causas y Soluciones

### 1. API Key Recién Creada (Más Común)
**Problema:** Las API keys de OpenWeatherMap pueden tardar hasta **2 horas** en activarse completamente.

**Solución:**
- Espera 10-60 minutos y vuelve a intentar
- Si después de 2 horas sigue fallando, verifica los siguientes puntos

### 2. Verificar que la API Key Esté Activa
1. Ve a: https://home.openweathermap.org/api_keys
2. Verifica que tu API key aparezca como "Active"
3. Si dice "Pending", espera a que se active

### 3. Verificar la API Key en el Código
Abre `backend/main.py` y verifica que la línea 25 tenga:
```python
WEATHER_API_KEY = "601714baa4a5b57143e20704e14050be"
```

### 4. Probar la API Key Directamente
Abre tu navegador y prueba esta URL (reemplaza TU_API_KEY con tu clave):
```
https://api.openweathermap.org/data/2.5/weather?q=London&appid=601714baa4a5b57143e20704e14050be&units=metric
```

Si funciona, deberías ver un JSON con datos del clima.
Si no funciona, el problema es con la API key.

### 5. Verificar Límites de la Cuenta
- Ve a: https://home.openweathermap.org/subscriptions
- Verifica que tengas un plan activo (Free tier está bien)
- Verifica que no hayas excedido los límites

### 6. Probar con el Endpoint de Prueba
He agregado un endpoint de prueba. Reinicia el backend y visita:
```
http://localhost:8000/test-weather
```

Esto te dirá si la API key está funcionando correctamente.

## Verificación Rápida

1. ✅ API key copiada correctamente (sin espacios)
2. ✅ API key marcada como "Active" en OpenWeatherMap
3. ✅ Esperaste al menos 10 minutos desde que creaste la API key
4. ✅ El backend fue reiniciado después de agregar la API key

## Si Nada Funciona

1. Genera una nueva API key en OpenWeatherMap
2. Reemplázala en el código
3. Espera 10-30 minutos
4. Reinicia el backend

