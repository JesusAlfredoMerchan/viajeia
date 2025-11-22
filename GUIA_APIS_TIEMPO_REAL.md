# 📊 Guía: APIs de Información en Tiempo Real

## APIs que Usaremos

### 1. Tipo de Cambio de Moneda
**API:** ExchangeRate-API (gratuita, sin API key para uso básico)
- URL: https://api.exchangerate-api.com/v4/latest/
- Límite: 1,500 solicitudes/mes (gratis)
- Sin necesidad de API key para uso básico

### 2. Diferencia Horaria
**API:** WorldTimeAPI (gratuita, sin API key)
- URL: http://worldtimeapi.org/api/timezone/
- Sin límites conocidos
- Sin necesidad de API key

### 3. Temperatura Actual
**API:** OpenWeatherMap (ya configurada)
- Ya está integrada y funcionando

## Funcionalidades

Cuando el usuario pregunte sobre un destino, Alex incluirá automáticamente:
- **Tipo de cambio:** Conversión de moneda local a USD/EUR
- **Diferencia horaria:** Hora actual y diferencia con la zona horaria del usuario
- **Temperatura:** Ya implementada con OpenWeatherMap

## Configuración

No se requiere configuración adicional - las APIs son gratuitas y no necesitan API keys.

