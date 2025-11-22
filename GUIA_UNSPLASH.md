# 📸 Guía: Integración con Unsplash API

## 📝 Cómo Obtener tu API Key Gratuita

### Paso 1: Crear una Cuenta
1. Ve a: https://unsplash.com/developers
2. Haz clic en "Register as a developer" o "Get started"
3. Inicia sesión con tu cuenta de Unsplash (o créala si no tienes)

### Paso 2: Crear una Aplicación
1. Una vez dentro, haz clic en "New Application"
2. Acepta los términos de uso
3. Completa el formulario:
   - **Application name:** ViajeIA
   - **Description:** Aplicación de asistente de viajes
   - **Website URL:** http://localhost:3000 (o tu URL)
   - **Callback URL:** http://localhost:3000

### Paso 3: Obtener tu Access Key
1. Después de crear la aplicación, verás tu **Access Key**
2. **Copia tu Access Key** - la necesitarás para configurar la aplicación
3. También verás tu **Secret Key** (no la necesitas para esto)

### Paso 4: Límites del Plan Gratuito
- 50 solicitudes por hora
- Acceso completo a la API
- Perfecto para desarrollo y uso personal

## 🔑 Configuración en ViajeIA

Una vez que tengas tu Access Key, se configurará en el archivo `backend/main.py` en la variable `UNSPLASH_ACCESS_KEY`.

## 📊 Qué Haremos

La API nos permitirá:
- Buscar fotos por término (nombre de la ciudad)
- Obtener 3 fotos hermosas del destino
- Mostrarlas automáticamente cuando Alex responda

## ✅ Listo para Usar

Una vez configurado, cuando menciones un destino, se mostrarán automáticamente 3 fotos hermosas del lugar.

