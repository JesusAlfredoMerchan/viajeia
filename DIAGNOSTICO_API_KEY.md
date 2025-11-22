# 🔍 Diagnóstico: API Keys No Funcionan

## Situación
Tienes dos API keys marcadas como "Active" en OpenWeatherMap, pero ambas dan error 401.

## Posibles Causas

### 1. API Keys Recién Creadas (Más Probable)
**Problema:** Aunque aparezcan como "Active", pueden tardar hasta **2 horas** en activarse completamente.

**Solución:**
- Espera 30-60 minutos más
- Prueba nuevamente

### 2. Problema con la Cuenta/Suscripción
**Problema:** Puede haber un problema con tu cuenta o suscripción.

**Solución:**
1. Ve a: https://home.openweathermap.org/subscriptions
2. Verifica que tengas un plan activo (Free tier está bien)
3. Verifica que no haya restricciones en tu cuenta

### 3. Verificar que las API Keys Estén Correctamente Copiadas
**Problema:** Puede haber espacios o caracteres ocultos.

**Solución:**
1. En OpenWeatherMap, haz clic en el ícono del ojo 👁️ junto a tu API key
2. Copia la API key COMPLETA desde ahí
3. Pégala directamente en el código sin editar

## Pasos de Diagnóstico

### Paso 1: Reiniciar el Backend
```powershell
# Detén el backend (Ctrl+C)
cd backend
python main.py
```

### Paso 2: Probar el Endpoint de Diagnóstico
Visita en tu navegador:
```
http://localhost:8000/test-weather
```

Esto te dará información detallada sobre el error.

### Paso 3: Probar Directamente en el Navegador
Prueba esta URL (reemplaza con tu API key):
```
https://api.openweathermap.org/data/2.5/weather?q=London&appid=03248d23bd5ad5a2cdf438702eaf90df&units=metric
```

Si funciona aquí pero no en el código, hay un problema con cómo se está enviando.

### Paso 4: Verificar en OpenWeatherMap
1. Ve a: https://home.openweathermap.org/api_keys
2. Haz clic en el ícono del ojo 👁️ para ver la API key completa
3. Verifica que sea exactamente la misma que en el código

## Solución Temporal: Desactivar Clima

Si necesitas continuar trabajando mientras se resuelve, puedes comentar temporalmente la función de clima en el código. El resto de la aplicación funcionará sin el clima.

## Contactar Soporte

Si después de 2 horas las API keys siguen sin funcionar:
1. Ve a: https://openweathermap.org/faq#error401
2. Contacta el soporte de OpenWeatherMap
3. Menciona que tus API keys aparecen como "Active" pero dan error 401

