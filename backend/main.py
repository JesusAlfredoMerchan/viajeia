from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import google.generativeai as genai
import requests
import re
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import base64

app = FastAPI(title="ViajeIA API")

# Configurar CORS para permitir peticiones desde el frontend
# En producción, permite todas las conexiones (o especifica tu dominio de Vercel)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if "*" not in ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar API Key de Gemini (usar variable de entorno en producción)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCKLNkxnhxWqbzDFlN5pxgpuuhziINi9Wo")
genai.configure(api_key=GEMINI_API_KEY)

# Configurar API Key de OpenWeatherMap
# Obtén tu API key gratuita en: https://openweathermap.org/api
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "03248d23bd5ad5a2cdf438702eaf90df")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Configurar API Key de Unsplash
# Obtén tu Access Key gratuita en: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "4aAIVujx9_CZOOm2xUNIpfT2uK_aOyeSDqYT7RuLQno")
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

# Función para encontrar el modelo correcto
def get_gemini_model():
    """Intenta encontrar el modelo Gemini 2.5 Flash o la versión más reciente disponible"""
    # Primero, intentar listar modelos disponibles
    try:
        print("Buscando modelos disponibles...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name.split('/')[-1]  # Extraer solo el nombre del modelo
                available_models.append(model_name)
        
        print(f"Modelos disponibles: {', '.join(available_models[:10])}...")  # Mostrar primeros 10
        
        # Buscar modelos que contengan "2.0", "2.5" o "flash" en el nombre
        flash_models = [m for m in available_models if 'flash' in m.lower() and ('2.0' in m or '2.5' in m or 'exp' in m.lower())]
        if flash_models:
            model_name = flash_models[0]
            print(f"✓ Modelo encontrado: {model_name}")
            return genai.GenerativeModel(model_name)
        
        # Si no hay 2.0/2.5, buscar cualquier flash
        any_flash = [m for m in available_models if 'flash' in m.lower()]
        if any_flash:
            model_name = any_flash[0]
            print(f"✓ Usando modelo flash disponible: {model_name}")
            return genai.GenerativeModel(model_name)
            
    except Exception as e:
        print(f"No se pudieron listar modelos: {e}")
    
    # Si no se pudo listar, intentar con nombres conocidos
    model_names = [
        'gemini-2.0-flash-exp',
        'gemini-2.0-flash-thinking-exp',
        'gemini-2.0-flash',
        'gemini-flash-latest',
        'gemini-1.5-flash',
    ]
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✓ Modelo configurado: {model_name}")
            return model
        except Exception as e:
            continue
    
    # Si todo falla, usar el modelo por defecto
    print("⚠ Usando modelo por defecto: gemini-1.5-flash")
    return genai.GenerativeModel('gemini-1.5-flash')

# Inicializar el modelo
print("Inicializando modelo Gemini...")
model = get_gemini_model()
print("✓ Modelo inicializado correctamente\n")

# Función para obtener el clima de una ciudad
def get_weather(city_name: str):
    """
    Obtiene el clima actual de una ciudad usando OpenWeatherMap API
    """
    if WEATHER_API_KEY == "TU_API_KEY_AQUI" or not WEATHER_API_KEY:
        print("⚠ API Key de OpenWeatherMap no configurada")
        return None
    
    try:
        # Limpiar y normalizar el nombre de la ciudad
        city_clean = city_name.strip().title()
        
        # Limpiar la API key de espacios
        api_key_clean = WEATHER_API_KEY.strip()
        
        params = {
            'q': city_clean,
            'appid': api_key_clean,
            'units': 'metric',  # Temperatura en Celsius
            'lang': 'es'  # Respuestas en español
        }
        
        print(f"🌤️ Consultando clima para: {city_clean}")
        print(f"🔑 API Key (primeros 10 chars): {api_key_clean[:10]}...")
        print(f"🔗 URL completa: {WEATHER_API_URL}?q={city_clean}&appid={api_key_clean[:10]}...")
        
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convertir m/s a km/h
                'icon': data['weather'][0]['icon']
            }
            print(f"✓ Clima obtenido: {weather_info['temperature']}°C en {weather_info['city']}")
            return weather_info
        elif response.status_code == 401:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get('message', 'API key inválida o no autorizada')
            print(f"❌ Error 401 - Autenticación fallida")
            print(f"   Mensaje: {error_msg}")
            print(f"   Verifica que tu API key sea correcta y esté activa")
            print(f"   API Key usada: {WEATHER_API_KEY[:10]}...{WEATHER_API_KEY[-4:]}")
            return None
        elif response.status_code == 404:
            print(f"❌ Ciudad no encontrada: {city_clean}")
            print(f"   Intenta con el nombre en inglés o agrega el país (ej: 'Valledupar, CO')")
            return None
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get('message', 'Error desconocido')
            print(f"❌ Error {response.status_code}: {error_msg}")
            return None
    except requests.exceptions.Timeout:
        print(f"❌ Timeout al conectar con OpenWeatherMap")
        return None
    except Exception as e:
        print(f"❌ Error al conectar con OpenWeatherMap: {str(e)}")
        return None

# Función para detectar nombres de ciudades/destinos en el texto
def detect_destination(text: str, user_prefs=None):
    """
    Detecta posibles destinos mencionados en el texto o en las preferencias del usuario
    """
    destinations = []
    
    # Primero, verificar si hay un destino en las preferencias del usuario
    if user_prefs and user_prefs.destination:
        destinations.append(user_prefs.destination)
    
    # Buscar patrones comunes de ciudades (palabras capitalizadas que no son inicio de oración)
    # Lista de ciudades comunes para mejorar la detección
    common_cities = [
        'paris', 'parís', 'london', 'londres', 'tokyo', 'tokio', 'new york', 'nueva york',
        'barcelona', 'madrid', 'rome', 'roma', 'amsterdam', 'berlin', 'prague', 'praga',
        'vienna', 'viena', 'athens', 'atenas', 'lisbon', 'lisboa', 'dublin', 'dublín',
        'copenhagen', 'copenhague', 'stockholm', 'estocolmo', 'oslo', 'helsinki', 'helsinki',
        'warsaw', 'varsovia', 'budapest', 'budapest', 'bucharest', 'bucarest', 'sofia', 'sofía',
        'moscow', 'moscú', 'istanbul', 'estambul', 'dubai', 'dubái', 'singapore', 'singapur',
        'hong kong', 'hong kong', 'seoul', 'seúl', 'beijing', 'pekín', 'shanghai', 'shanghái',
        'sydney', 'sídney', 'melbourne', 'melbourne', 'auckland', 'auckland', 'rio de janeiro',
        'são paulo', 'sao paulo', 'buenos aires', 'lima', 'bogotá', 'bogota', 'santiago',
        'mexico city', 'ciudad de méxico', 'mexico', 'méxico', 'cancun', 'cancún', 'miami',
        'los angeles', 'san francisco', 'chicago', 'boston', 'toronto', 'vancouver', 'montreal',
        'cairo', 'el cairo', 'johannesburg', 'johannesburgo', 'cape town', 'ciudad del cabo'
    ]
    
    text_lower = text.lower()
    
    # Buscar ciudades comunes en el texto
    for city in common_cities:
        if city in text_lower:
            destinations.append(city.title())
    
    # Si no encontramos nada, intentar extraer palabras capitalizadas (posibles nombres de ciudades)
    if not destinations:
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        # Filtrar palabras comunes que no son ciudades
        exclude_words = ['Alex', 'ViajeIA', 'Viaje', 'Tu', 'Tu', 'Mi', 'Me', 'El', 'La', 'Los', 'Las']
        potential_cities = [w for w in words if w not in exclude_words and len(w) > 3]
        if potential_cities:
            destinations.extend(potential_cities[:2])  # Tomar máximo 2 candidatos
    
    return destinations[0] if destinations else None

# Función para obtener tipo de cambio de moneda
def get_exchange_rate(base_currency="USD"):
    """
    Obtiene el tipo de cambio actual usando ExchangeRate-API
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Retornar las tasas más comunes
            rates = {
                'USD': data['rates'].get('USD', 1),
                'EUR': data['rates'].get('EUR', 1),
                'GBP': data['rates'].get('GBP', 1),
                'JPY': data['rates'].get('JPY', 1),
                'MXN': data['rates'].get('MXN', 1),
                'COP': data['rates'].get('COP', 1),  # Pesos colombianos
            }
            print(f"💱 Tipo de cambio obtenido (base: {base_currency})")
            return rates
        else:
            print(f"⚠ Error al obtener tipo de cambio: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠ Error al conectar con ExchangeRate API: {str(e)}")
        return None

# Función para obtener información de zona horaria
def get_timezone_info(city_name: str, country_code: str = None):
    """
    Obtiene información de zona horaria usando mapeo directo (más confiable)
    """
    try:
        from datetime import datetime
        import pytz
        
        # Mapeo completo de códigos de país a zonas horarias
        country_timezone_map = {
            'CO': 'America/Bogota',  # Colombia
            'US': 'America/New_York',  # Estados Unidos
            'MX': 'America/Mexico_City',  # México
            'ES': 'Europe/Madrid',  # España
            'FR': 'Europe/Paris',  # Francia
            'GB': 'Europe/London',  # Reino Unido
            'IT': 'Europe/Rome',  # Italia
            'DE': 'Europe/Berlin',  # Alemania
            'JP': 'Asia/Tokyo',  # Japón
            'CN': 'Asia/Shanghai',  # China
            'BR': 'America/Sao_Paulo',  # Brasil
            'AR': 'America/Buenos_Aires',  # Argentina
            'CL': 'America/Santiago',  # Chile
            'PE': 'America/Lima',  # Perú
            'EC': 'America/Guayaquil',  # Ecuador
            'VE': 'America/Caracas',  # Venezuela
            'UY': 'America/Montevideo',  # Uruguay
            'PY': 'America/Asuncion',  # Paraguay
            'BO': 'America/La_Paz',  # Bolivia
            'CR': 'America/Costa_Rica',  # Costa Rica
            'PA': 'America/Panama',  # Panamá
            'GT': 'America/Guatemala',  # Guatemala
            'CU': 'America/Havana',  # Cuba
            'DO': 'America/Santo_Domingo',  # República Dominicana
            'PR': 'America/Puerto_Rico',  # Puerto Rico
            'CA': 'America/Toronto',  # Canadá
            'AU': 'Australia/Sydney',  # Australia
            'NZ': 'Pacific/Auckland',  # Nueva Zelanda
            'ZA': 'Africa/Johannesburg',  # Sudáfrica
            'EG': 'Africa/Cairo',  # Egipto
            'MA': 'Africa/Casablanca',  # Marruecos
            'TR': 'Europe/Istanbul',  # Turquía
            'RU': 'Europe/Moscow',  # Rusia
            'IN': 'Asia/Kolkata',  # India
            'TH': 'Asia/Bangkok',  # Tailandia
            'SG': 'Asia/Singapore',  # Singapur
            'MY': 'Asia/Kuala_Lumpur',  # Malasia
            'ID': 'Asia/Jakarta',  # Indonesia
            'PH': 'Asia/Manila',  # Filipinas
            'VN': 'Asia/Ho_Chi_Minh',  # Vietnam
            'KR': 'Asia/Seoul',  # Corea del Sur
            'TW': 'Asia/Taipei',  # Taiwán
            'HK': 'Asia/Hong_Kong',  # Hong Kong
        }
        
        # Usar mapeo directo si tenemos código de país
        if country_code and country_code.upper() in country_timezone_map:
            tz_name = country_timezone_map[country_code.upper()]
            try:
                # Obtener hora usando pytz (más confiable que API externa)
                tz = pytz.timezone(tz_name)
                now = datetime.now(tz)
                utc_offset = now.strftime('%z')
                # Formatear offset como +HH:MM
                if utc_offset:
                    offset_formatted = f"{utc_offset[:3]}:{utc_offset[3:]}"
                else:
                    offset_formatted = '+00:00'
                
                print(f"🕐 Información de zona horaria obtenida: {tz_name}")
                return {
                    'timezone': tz_name,
                    'datetime': now.isoformat(),
                    'utc_offset': offset_formatted,
                    'abbreviation': now.strftime('%Z') or tz_name.split('/')[-1][:3].upper()
                }
            except Exception as e:
                print(f"⚠ Error al obtener zona horaria con pytz: {str(e)}")
        
        # Si no tenemos código de país o falla, usar UTC local
        try:
            utc_now = datetime.utcnow()
            print(f"🕐 Usando UTC como zona horaria")
            return {
                'timezone': 'UTC',
                'datetime': utc_now.isoformat() + '+00:00',
                'utc_offset': '+00:00',
                'abbreviation': 'UTC'
            }
        except Exception as e:
            print(f"⚠ Error al obtener UTC: {str(e)}")
            return None
            
    except ImportError:
        # Si pytz no está instalado, usar método simple
        print("⚠ pytz no está instalado, usando método alternativo")
        try:
            from datetime import datetime, timezone
            utc_now = datetime.now(timezone.utc)
            return {
                'timezone': 'UTC',
                'datetime': utc_now.isoformat(),
                'utc_offset': '+00:00',
                'abbreviation': 'UTC'
            }
        except:
            return None
    except Exception as e:
        print(f"⚠ Error al obtener información de zona horaria: {str(e)}")
        return None

# Función para obtener fotos del destino desde Unsplash
def get_destination_photos(destination_name: str, count: int = 3):
    """
    Obtiene fotos hermosas de un destino usando Unsplash API
    """
    if not UNSPLASH_ACCESS_KEY or UNSPLASH_ACCESS_KEY == "TU_ACCESS_KEY_AQUI":
        print("⚠ API Key de Unsplash no configurada")
        return []
    
    try:
        headers = {
            'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
        }
        
        params = {
            'query': destination_name,
            'per_page': count,
            'orientation': 'landscape',  # Fotos horizontales para mejor visualización
            'order_by': 'popular'  # Las más populares primero
        }
        
        response = requests.get(UNSPLASH_API_URL, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            photos = []
            
            for photo in data.get('results', [])[:count]:
                photos.append({
                    'id': photo.get('id'),
                    'url': photo['urls']['regular'],  # Tamaño regular para buena calidad
                    'thumb': photo['urls']['thumb'],  # Miniatura para carga rápida
                    'description': photo.get('description') or photo.get('alt_description', ''),
                    'photographer': photo['user']['name'],
                    'photographer_url': photo['user']['links']['html']
                })
            
            print(f"📸 Obtenidas {len(photos)} fotos de {destination_name}")
            return photos
        elif response.status_code == 401:
            print(f"❌ Error 401 - Unsplash API key inválida")
            return []
        else:
            print(f"⚠ Error al obtener fotos de Unsplash: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠ Error al conectar con Unsplash: {str(e)}")
        return []

class UserPreferences(BaseModel):
    destination: str = ""
    date: str = ""
    budget: str = ""
    preference: str = ""

class QuestionRequest(BaseModel):
    question: str
    userPreferences: Optional[UserPreferences] = None
    lastDestination: Optional[str] = None  # Último destino mencionado
    conversationHistory: List[Dict[str, Any]] = []  # Historial de conversaciones recientes

class ResponseModel(BaseModel):
    response: str
    photos: List[Dict[str, Any]] = []  # Lista de fotos del destino
    weather: Optional[Dict[str, Any]] = None  # Información del clima
    exchange_rates: Optional[Dict[str, Any]] = None  # Tipo de cambio
    timezone_info: Optional[Dict[str, Any]] = None  # Información de zona horaria
    detected_destination: Optional[str] = None  # Destino detectado en esta conversación

class ItineraryRequest(BaseModel):
    destination: str
    date: str
    budget: str
    preference: str
    conversationHistory: List[Dict[str, Any]] = []
    weather: Optional[Dict[str, Any]] = None
    exchange_rates: Optional[Dict[str, Any]] = None
    timezone_info: Optional[Dict[str, Any]] = None
    photos: List[Dict[str, Any]] = []

@app.get("/")
def read_root():
    return {"message": "ViajeIA API está funcionando con Gemini"}

@app.get("/test-weather")
def test_weather():
    """
    Endpoint de prueba para verificar la API de clima
    """
    test_city = "London"  # Ciudad de prueba
    
    # Probar directamente con requests para ver el error completo
    try:
        params = {
            'q': test_city,
            'appid': WEATHER_API_KEY.strip(),
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "message": "API de clima funcionando correctamente",
                "weather": {
                    "city": data['name'],
                    "temperature": round(data['main']['temp']),
                    "description": data['weather'][0]['description']
                },
                "api_key_length": len(WEATHER_API_KEY),
                "api_key_preview": f"{WEATHER_API_KEY[:10]}...{WEATHER_API_KEY[-4:]}"
            }
        else:
            error_data = response.json() if response.text else {}
            return {
                "status": "error",
                "error_code": response.status_code,
                "error_message": error_data.get('message', 'Error desconocido'),
                "full_error": error_data,
                "api_key_length": len(WEATHER_API_KEY),
                "api_key_preview": f"{WEATHER_API_KEY[:10]}...{WEATHER_API_KEY[-4:]}",
                "url_tested": f"{WEATHER_API_URL}?q={test_city}&appid={WEATHER_API_KEY[:10]}..."
            }
    except Exception as e:
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "api_key_configured": WEATHER_API_KEY != "TU_API_KEY_AQUI" and bool(WEATHER_API_KEY)
        }

@app.post("/api/chat", response_model=ResponseModel)
async def chat(request: QuestionRequest):
    """
    Endpoint para procesar preguntas sobre viajes usando Gemini AI
    """
    try:
        # Detectar destino - usar último destino conocido si no se detecta uno nuevo
        detected_destination = detect_destination(request.question, request.userPreferences)
        
        # Si no se detecta un destino pero hay un último destino conocido, usarlo
        if not detected_destination and request.lastDestination:
            detected_destination = request.lastDestination
            print(f"📍 Usando último destino conocido: {detected_destination}")
        
        weather_info = None
        destination_photos = []
        exchange_rates = None
        timezone_info = None
        
        if detected_destination:
            print(f"🌍 Detectado destino: {detected_destination}, obteniendo información en tiempo real...")
            
            # Obtener clima
            try:
                weather_info = get_weather(detected_destination)
                # El mensaje de éxito ya se imprime dentro de get_weather()
            except Exception as e:
                print(f"⚠ Error al obtener clima (continuando sin él): {str(e)}")
                weather_info = None
            
            # Obtener fotos del destino
            try:
                destination_photos = get_destination_photos(detected_destination, count=3)
                if destination_photos:
                    print(f"✓ Fotos obtenidas: {len(destination_photos)} fotos de {detected_destination}")
                else:
                    print("⚠ No se pudieron obtener fotos (continuando sin fotos)")
            except Exception as e:
                print(f"⚠ Error al obtener fotos (continuando sin ellas): {str(e)}")
                destination_photos = []
            
            # Obtener tipo de cambio
            try:
                exchange_rates = get_exchange_rate("USD")
            except Exception as e:
                print(f"⚠ Error al obtener tipo de cambio (continuando sin él): {str(e)}")
                exchange_rates = None
            
            # Obtener información de zona horaria
            try:
                country_code = weather_info.get('country') if weather_info else None
                timezone_info = get_timezone_info(detected_destination, country_code)
            except Exception as e:
                print(f"⚠ Error al obtener zona horaria (continuando sin ella): {str(e)}")
                timezone_info = None
        
        # Construir contexto del historial de conversaciones
        history_context = ""
        if request.conversationHistory and len(request.conversationHistory) > 0:
            history_context = "\n\nCONTEXTO DE CONVERSACIONES ANTERIORES:\n"
            for i, conv in enumerate(request.conversationHistory[-3:], 1):  # Últimas 3 conversaciones
                history_context += f"Conversación {i}:\n"
                history_context += f"  Pregunta: {conv.get('question', 'N/A')}\n"
                if conv.get('destination'):
                    history_context += f"  Destino mencionado: {conv.get('destination')}\n"
            history_context += "\nUsa este contexto para entender referencias a conversaciones anteriores. "
            history_context += "Si el usuario pregunta sobre 'allí', 'ese lugar', 'el transporte', etc., "
            history_context += "se refiere al último destino mencionado en las conversaciones anteriores."
        
        # Construir contexto de preferencias del usuario
        preferences_context = ""
        if request.userPreferences:
            prefs = request.userPreferences
            if prefs.destination or prefs.date or prefs.budget or prefs.preference:
                preferences_context = "\n\nINFORMACIÓN DEL VIAJE DEL USUARIO:\n"
                if prefs.destination:
                    preferences_context += f"• Destino: {prefs.destination}\n"
                if prefs.date:
                    preferences_context += f"• Fecha: {prefs.date}\n"
                if prefs.budget:
                    preferences_context += f"• Presupuesto: {prefs.budget}\n"
                if prefs.preference:
                    preference_map = {
                        "aventura": "Aventura 🏔️",
                        "relajacion": "Relajación 🏖️",
                        "cultura": "Cultura 🏛️"
                    }
                    pref_display = preference_map.get(prefs.preference, prefs.preference)
                    preferences_context += f"• Preferencia de viaje: {pref_display}\n"
                preferences_context += "\nUsa esta información para personalizar tu respuesta y hacer recomendaciones específicas."
        
        # Agregar información del clima al contexto
        weather_context = ""
        if weather_info:
            weather_context = f"""

INFORMACIÓN DEL CLIMA ACTUAL:
• Ciudad: {weather_info['city']}, {weather_info['country']}
• Temperatura: {weather_info['temperature']}°C (sensación térmica: {weather_info['feels_like']}°C)
• Condiciones: {weather_info['description']}
• Humedad: {weather_info['humidity']}%
• Viento: {weather_info['wind_speed']} km/h

IMPORTANTE: Incluye esta información del clima en tu respuesta, especialmente en la sección de CONSEJOS LOCALES. 
Menciona qué ropa llevar y qué actividades son mejores según el clima actual."""

        # Agregar información de tipo de cambio
        exchange_context = ""
        if exchange_rates:
            exchange_context = f"""

INFORMACIÓN DE TIPO DE CAMBIO (USD como base):
• 1 USD = {exchange_rates.get('EUR', 'N/A'):.2f} EUR
• 1 USD = {exchange_rates.get('GBP', 'N/A'):.2f} GBP
• 1 USD = {exchange_rates.get('MXN', 'N/A'):.2f} MXN (Pesos Mexicanos)
• 1 USD = {exchange_rates.get('COP', 'N/A'):.2f} COP (Pesos Colombianos)

IMPORTANTE: Incluye esta información en la sección de ESTIMACIÓN DE COSTOS para ayudar al usuario a entender los precios locales."""

        # Agregar información de zona horaria
        timezone_context = ""
        if timezone_info:
            timezone_context = f"""

INFORMACIÓN DE ZONA HORARIA:
• Zona horaria: {timezone_info['timezone']}
• Hora actual: {timezone_info['datetime'][:19]} (formato: YYYY-MM-DD HH:MM:SS)
• UTC Offset: {timezone_info['utc_offset']}
• Abreviación: {timezone_info['abbreviation']}

IMPORTANTE: Incluye esta información en la sección de CONSEJOS LOCALES para ayudar al usuario a planificar su viaje considerando la diferencia horaria."""

        # Crear el prompt para Gemini con personalidad de Alex
        prompt = f"""Eres Alex, el consultor personal de viajes de ViajeIA. Tienes una personalidad entusiasta, amigable y experta en viajes.

INSTRUCCIONES DE PERSONALIDAD Y ESTILO:
1. PRESENTACIÓN: Siempre te presentas como "Alex, tu consultor personal de viajes" en tu primera interacción o cuando sea apropiado
2. TONO: Sé entusiasta, amigable y cercano. Usa un lenguaje cálido y profesional
3. EMOJIS: Incluye emojis de viajes relevantes en tus respuestas (✈️ 🏨 🗺️ 🌍 🎒 🍽️ 🎯 📍 🏛️ 🌴 etc.)
4. ESTRUCTURA OBLIGATORIA: SIEMPRE debes responder con esta estructura exacta, usando estos símbolos y títulos:
   » ALOJAMIENTO: [recomendaciones de hoteles, hostales, o alojamientos]
   Þ COMIDA LOCAL: [recomendaciones de restaurantes y platos típicos]
   u LUGARES IMPERDIBLES: [sitios y atracciones que no se pueden perder]
   D CONSEJOS LOCALES: [tips especiales, secretos locales, recomendaciones de expertos]
   X ESTIMACIÓN DE COSTOS: [breakdown aproximado de gastos por categoría]
5. PREGUNTAS INTELIGENTES: Si necesitas más información, haz preguntas de seguimiento al inicio o al final
6. EXPERTISE: Demuestra conocimiento experto sobre destinos, hoteles, restaurantes, actividades y planificación de viajes
7. PERSONALIZACIÓN: Si tienes información sobre el viaje del usuario, úsala para dar recomendaciones específicas y relevantes
8. MEMORIA: Recuerda el contexto de conversaciones anteriores. Si el usuario pregunta sobre "allí", "ese lugar", "el transporte", etc., se refiere al último destino mencionado{history_context}{preferences_context}{weather_context}{exchange_context}{timezone_context}

IMPORTANTE: 
- SIEMPRE incluye las 5 secciones con los símbolos exactos (», Þ, u, D, X)
- Cada sección debe tener contenido relevante y útil
- Si alguna sección no aplica completamente, proporciona información relacionada de todas formas
- Usa bullets (•) dentro de cada sección para organizar la información
- Mantén el tono entusiasta y amigable

Pregunta del usuario: {request.question}

Responde como Alex usando SIEMPRE la estructura obligatoria con las 5 secciones. Sé específico, útil y personaliza según la información del usuario si está disponible:"""

        # Generar respuesta con Gemini
        response = model.generate_content(prompt)
        
        # Extraer el texto de la respuesta
        if response.text:
            return ResponseModel(
                response=response.text, 
                photos=destination_photos,
                weather=weather_info,
                exchange_rates=exchange_rates,
                timezone_info=timezone_info,
                detected_destination=detected_destination
            )
        else:
            return ResponseModel(
                response="Lo siento, no pude generar una respuesta. Por favor, intenta de nuevo.", 
                photos=[],
                weather=weather_info,
                exchange_rates=exchange_rates,
                timezone_info=timezone_info,
                detected_destination=detected_destination
            )
            
    except Exception as e:
        # En caso de error, devolver un mensaje amigable
        error_message = str(e)
        print(f"Error al conectar con Gemini: {error_message}")
        
        # Manejar errores de cuota específicamente
        if "429" in error_message or "quota" in error_message.lower() or "rate" in error_message.lower():
            return ResponseModel(
                response="Lo siento, se ha alcanzado el límite de solicitudes. Por favor, espera unos momentos e intenta de nuevo. Si el problema persiste, verifica tu plan de Gemini API.",
                photos=destination_photos,
                weather=weather_info,
                exchange_rates=exchange_rates,
                timezone_info=timezone_info,
                detected_destination=detected_destination
            )
        else:
            return ResponseModel(
                response="Lo siento, hubo un problema al procesar tu pregunta. Por favor, verifica tu conexión a internet e intenta de nuevo.",
                photos=destination_photos,
                weather=weather_info,
                exchange_rates=exchange_rates,
                timezone_info=timezone_info,
                detected_destination=detected_destination
            )

# Función para generar PDF del itinerario
def generate_itinerary_pdf(data: ItineraryRequest):
    """
    Genera un PDF bonito con el itinerario completo
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para el título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    # Logo/Header
    header_text = Paragraph("<b>ViajeIA</b><br/><i>Tu Asistente Personal de Viajes</i>", title_style)
    story.append(header_text)
    story.append(Spacer(1, 0.3*inch))
    
    # Información del viaje
    destination_text = f"<b>Destino:</b> {data.destination}"
    
    # Formatear fecha si es posible
    try:
        from datetime import datetime
        # Intentar diferentes formatos de fecha
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
        formatted_date = data.date
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(data.date, fmt)
                # Meses en español
                months = {
                    1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                    5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
                    9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
                }
                formatted_date = f"{date_obj.day} de {months[date_obj.month]} de {date_obj.year}"
                break
            except:
                continue
    except:
        formatted_date = data.date
    
    date_text = f"<b>Fecha:</b> {formatted_date}"
    budget_text = f"<b>Presupuesto:</b> {data.budget.capitalize() if data.budget else 'No especificado'}"
    preference_text = f"<b>Preferencia:</b> {data.preference.capitalize() if data.preference else 'No especificada'}"
    
    info_data = [
        [Paragraph(destination_text, normal_style), Paragraph(date_text, normal_style)],
        [Paragraph(budget_text, normal_style), Paragraph(preference_text, normal_style)]
    ]
    
    info_table = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e40af')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#2563eb')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Información en tiempo real
    if data.weather or data.exchange_rates or data.timezone_info:
        story.append(Paragraph("📊 Información en Tiempo Real", subtitle_style))
        
        if data.weather:
            weather_text = f"""
            <b>Clima Actual:</b><br/>
            Temperatura: {data.weather.get('temperature', 'N/A')}°C 
            (Sensación: {data.weather.get('feels_like', 'N/A')}°C)<br/>
            Condiciones: {data.weather.get('description', 'N/A')}<br/>
            Humedad: {data.weather.get('humidity', 'N/A')}% | 
            Viento: {data.weather.get('wind_speed', 'N/A')} km/h
            """
            story.append(Paragraph(weather_text, normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        if data.exchange_rates:
            exchange_text = f"""
            <b>Tipo de Cambio (Base USD):</b><br/>
            EUR: {data.exchange_rates.get('EUR', 0):.2f} | 
            GBP: {data.exchange_rates.get('GBP', 0):.2f} | 
            MXN: {data.exchange_rates.get('MXN', 0):.2f} | 
            COP: {data.exchange_rates.get('COP', 0):.2f}
            """
            story.append(Paragraph(exchange_text, normal_style))
            story.append(Spacer(1, 0.2*inch))
        
        if data.timezone_info:
            timezone_text = f"""
            <b>Zona Horaria:</b> {data.timezone_info.get('timezone', 'N/A')}<br/>
            Hora Actual: {data.timezone_info.get('datetime', 'N/A')[:19]}<br/>
            UTC Offset: {data.timezone_info.get('utc_offset', 'N/A')}
            """
            story.append(Paragraph(timezone_text, normal_style))
        
        story.append(Spacer(1, 0.3*inch))
    
    # Recomendaciones de la conversación
    story.append(Paragraph("🗺️ Recomendaciones del Itinerario", subtitle_style))
    
    # Combinar todas las respuestas
    all_responses = []
    for conv in data.conversationHistory:
        if conv.get('response'):
            all_responses.append(conv.get('response'))
    
    if all_responses:
        # Procesar la última respuesta (más completa)
        response_text = all_responses[-1]
        
        # Dividir por líneas para procesar mejor
        lines = response_text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detectar inicio de sección
            if '» ALOJAMIENTO' in line or ('ALOJAMIENTO' in line and '»' in line):
                if current_section:
                    story.append(Paragraph('<br/>'.join(current_content), normal_style))
                    story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph("<b>🏨 ALOJAMIENTO</b>", subtitle_style))
                current_section = 'alojamiento'
                current_content = [line.replace('»', '').replace('ALOJAMIENTO:', '').strip()]
            elif 'Þ COMIDA LOCAL' in line or ('COMIDA LOCAL' in line and 'Þ' in line):
                if current_section:
                    story.append(Paragraph('<br/>'.join(current_content), normal_style))
                    story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph("<b>🍽️ COMIDA LOCAL</b>", subtitle_style))
                current_section = 'comida'
                current_content = [line.replace('Þ', '').replace('COMIDA LOCAL:', '').strip()]
            elif 'u LUGARES IMPERDIBLES' in line or ('LUGARES IMPERDIBLES' in line and 'u' in line):
                if current_section:
                    story.append(Paragraph('<br/>'.join(current_content), normal_style))
                    story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph("<b>📍 LUGARES IMPERDIBLES</b>", subtitle_style))
                current_section = 'lugares'
                current_content = [line.replace('u', '').replace('LUGARES IMPERDIBLES:', '').strip()]
            elif 'D CONSEJOS LOCALES' in line or ('CONSEJOS LOCALES' in line and 'D' in line):
                if current_section:
                    story.append(Paragraph('<br/>'.join(current_content), normal_style))
                    story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph("<b>💡 CONSEJOS LOCALES</b>", subtitle_style))
                current_section = 'consejos'
                current_content = [line.replace('D', '').replace('CONSEJOS LOCALES:', '').strip()]
            elif 'X ESTIMACIÓN DE COSTOS' in line or ('ESTIMACIÓN DE COSTOS' in line and 'X' in line):
                if current_section:
                    story.append(Paragraph('<br/>'.join(current_content), normal_style))
                    story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph("<b>💰 ESTIMACIÓN DE COSTOS</b>", subtitle_style))
                current_section = 'costos'
                current_content = [line.replace('X', '').replace('ESTIMACIÓN DE COSTOS:', '').strip()]
            else:
                # Agregar a contenido actual
                if line and not line.startswith('¡Hola') and not line.startswith('Soy Alex'):
                    current_content.append(line)
        
        # Agregar última sección
        if current_content:
            story.append(Paragraph('<br/>'.join(current_content), normal_style))
    
    # Fotos del destino
    if data.photos and len(data.photos) > 0:
        story.append(PageBreak())
        story.append(Paragraph("📸 Fotos del Destino", subtitle_style))
        story.append(Spacer(1, 0.2*inch))
        
        for photo in data.photos[:6]:  # Máximo 6 fotos
            try:
                # Descargar imagen
                img_url = photo.get('url') or photo.get('thumb', '')
                if img_url:
                    img_response = requests.get(img_url, timeout=15)
                    if img_response.status_code == 200:
                        img_data = BytesIO(img_response.content)
                        # Calcular dimensiones manteniendo proporción
                        try:
                            from PIL import Image as PILImage
                            pil_img = PILImage.open(img_data)
                            img_width, img_height = pil_img.size
                            aspect_ratio = img_height / img_width
                            
                            # Ajustar tamaño máximo
                            max_width = 5.5 * inch
                            max_height = 4 * inch
                            
                            if aspect_ratio > (max_height / max_width):
                                # Imagen más alta
                                width = max_height / aspect_ratio
                                height = max_height
                            else:
                                # Imagen más ancha
                                width = max_width
                                height = max_width * aspect_ratio
                            
                            img_data.seek(0)
                            img = Image(img_data, width=width, height=height)
                        except Exception as img_error:
                            # Si hay error con PIL, usar tamaño fijo
                            print(f"Error al procesar imagen: {str(img_error)}")
                            img_data.seek(0)
                            img = Image(img_data, width=5*inch, height=3.75*inch)
                        story.append(img)
                        
                        # Crédito del fotógrafo
                        credit_text = f"<i>Foto por {photo.get('photographer', 'Desconocido')}</i>"
                        story.append(Paragraph(credit_text, normal_style))
                        story.append(Spacer(1, 0.3*inch))
            except Exception as e:
                print(f"Error al agregar foto al PDF: {str(e)}")
                continue
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = "<i>Generado por ViajeIA - Tu Asistente Personal de Viajes</i>"
    story.append(Paragraph(footer_text, normal_style))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

@app.post("/api/generate-itinerary-pdf")
async def generate_pdf(request: ItineraryRequest):
    """
    Endpoint para generar PDF del itinerario
    """
    try:
        pdf_buffer = generate_itinerary_pdf(request)
        
        # Guardar temporalmente
        import tempfile
        import os
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=os.path.dirname(__file__))
        pdf_buffer.seek(0)
        temp_file.write(pdf_buffer.read())
        temp_file.close()
        
        # Limpiar archivo después de enviarlo
        def cleanup_file():
            try:
                os.unlink(temp_file.name)
            except:
                pass
        
        return FileResponse(
            temp_file.name,
            media_type='application/pdf',
            filename=f'itinerario_{request.destination.replace(" ", "_").replace("/", "_")}.pdf',
            background=None
        )
    except Exception as e:
        import traceback
        print(f"Error al generar PDF: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al generar PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

