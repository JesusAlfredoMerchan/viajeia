import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from './config';
import './App.css';

// Configurar axios con la URL base
const api = axios.create({
  baseURL: config.API_BASE_URL
});

function App() {
  const [showForm, setShowForm] = useState(true);
  const [formData, setFormData] = useState({
    destination: '',
    date: '',
    budget: '',
    preference: ''
  });
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [photos, setPhotos] = useState([]);
  const [weather, setWeather] = useState(null);
  const [exchangeRates, setExchangeRates] = useState(null);
  const [timezoneInfo, setTimezoneInfo] = useState(null);
  const [backgroundImage, setBackgroundImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [lastDestination, setLastDestination] = useState(null);
  const [savedDestinations, setSavedDestinations] = useState([]);
  const [showSavedDestinations, setShowSavedDestinations] = useState(false);

  // Cargar destinos guardados desde localStorage al iniciar
  useEffect(() => {
    const saved = localStorage.getItem('viajeia_saved_destinations');
    if (saved) {
      try {
        setSavedDestinations(JSON.parse(saved));
      } catch (e) {
        console.error('Error al cargar destinos guardados:', e);
      }
    }
  }, []);

  // Guardar destinos en localStorage cuando cambien
  useEffect(() => {
    if (savedDestinations.length > 0) {
      localStorage.setItem('viajeia_saved_destinations', JSON.stringify(savedDestinations));
    }
  }, [savedDestinations]);

  // Función para guardar destino como favorito
  const saveDestination = () => {
    if (!lastDestination && !formData.destination) return;

    const destination = lastDestination || formData.destination;
    const destinationData = {
      id: Date.now().toString(),
      destination: destination,
      date: formData.date,
      budget: formData.budget,
      preference: formData.preference,
      weather: weather,
      timezoneInfo: timezoneInfo,
      exchangeRates: exchangeRates,
      savedAt: new Date().toISOString(),
      conversationCount: conversationHistory.length
    };

    // Verificar si ya existe
    const exists = savedDestinations.find(d => 
      d.destination.toLowerCase() === destination.toLowerCase()
    );

    if (!exists) {
      setSavedDestinations(prev => [destinationData, ...prev]);
    }
  };

  // Función para eliminar destino guardado
  const removeSavedDestination = (id) => {
    setSavedDestinations(prev => prev.filter(d => d.id !== id));
  };

  // Función para cargar un destino guardado
  const loadSavedDestination = (savedDest) => {
    setFormData({
      destination: savedDest.destination,
      date: savedDest.date || '',
      budget: savedDest.budget || '',
      preference: savedDest.preference || ''
    });
    setLastDestination(savedDest.destination);
    setShowSavedDestinations(false);
    setShowForm(false);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (formData.destination && formData.date && formData.budget && formData.preference) {
      // Guardar el destino del formulario como último destino conocido
      setLastDestination(formData.destination);
      setShowForm(false);
    }
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setResponse('');
    setPhotos([]);
    setWeather(null);
    setExchangeRates(null);
    setTimezoneInfo(null);
    
    // Guardar pregunta en el historial temporal
    const newQuestion = {
      question: question,
      timestamp: new Date().toISOString()
    };

    try {
      const res = await api.post('/api/chat', {
        question: question,
        userPreferences: formData,
        lastDestination: lastDestination, // Enviar último destino conocido
        conversationHistory: conversationHistory.slice(-5).map(item => ({
          question: item.question,
          destination: item.destination
        })) // Enviar últimas 5 conversaciones para contexto
      });
      
      setResponse(res.data.response);
      setPhotos(res.data.photos || []);
      setWeather(res.data.weather || null);
      setExchangeRates(res.data.exchange_rates || null);
      setTimezoneInfo(res.data.timezone_info || null);
      
      // Actualizar último destino si se detectó uno nuevo
      const detectedDest = res.data.detected_destination;
      if (detectedDest) {
        setLastDestination(detectedDest);
        // Guardar automáticamente si no existe ya
        const exists = savedDestinations.find(d => 
          d.destination.toLowerCase() === detectedDest.toLowerCase()
        );
        if (!exists && formData.destination) {
          const destinationData = {
            id: Date.now().toString(),
            destination: detectedDest,
            date: formData.date,
            budget: formData.budget,
            preference: formData.preference,
            weather: res.data.weather || null,
            timezoneInfo: res.data.timezone_info || null,
            exchangeRates: res.data.exchange_rates || null,
            savedAt: new Date().toISOString(),
            conversationCount: conversationHistory.length + 1
          };
          setSavedDestinations(prev => [destinationData, ...prev]);
        }
      }
      
      // Usar la primera foto como imagen de fondo
      if (res.data.photos && res.data.photos.length > 0) {
        setBackgroundImage(res.data.photos[0].url);
      } else {
        setBackgroundImage(null);
      }
      
      // Agregar al historial
      setConversationHistory(prev => [
        ...prev,
        {
          ...newQuestion,
          response: res.data.response,
          destination: detectedDest || lastDestination
        }
      ]);
    } catch (error) {
      console.error('Error:', error);
      setResponse('Lo siento, hubo un error al procesar tu solicitud. Por favor, intenta de nuevo.');
      setPhotos([]);
      setWeather(null);
      setExchangeRates(null);
      setTimezoneInfo(null);
      setBackgroundImage(null);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleDownloadPDF = async () => {
    try {
      // Preparar datos para el PDF
      const pdfData = {
        destination: formData.destination || lastDestination || 'Destino',
        date: formData.date || 'No especificada',
        budget: formData.budget || 'No especificado',
        preference: formData.preference || 'No especificada',
        conversationHistory: conversationHistory,
        weather: weather,
        exchange_rates: exchangeRates,
        timezone_info: timezoneInfo,
        photos: photos
      };

      const response = await api.post('/api/generate-itinerary-pdf', pdfData, {
        responseType: 'blob'
      });

      // Crear URL del blob y descargar
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `itinerario_${pdfData.destination.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error al generar PDF:', error);
      alert('Error al generar el PDF. Por favor, intenta de nuevo.');
    }
  };

  return (
    <div className="App" style={{ backgroundImage: backgroundImage ? `url(${backgroundImage})` : 'none' }}>
      <div className="container">
        <header className="header">
          <h1 className="title">ViajeIA - Tu Asistente Personal de Viajes</h1>
          <button
            className="saved-destinations-toggle"
            onClick={() => setShowSavedDestinations(!showSavedDestinations)}
            title="Ver mis viajes guardados"
          >
            <span className="toggle-icon">⭐</span>
            <span className="toggle-text">Mis Viajes Guardados</span>
            {savedDestinations.length > 0 && (
              <span className="toggle-badge">{savedDestinations.length}</span>
            )}
          </button>
        </header>

        <main className="main-content">
          {/* Sección de Destinos Guardados */}
          {showSavedDestinations && (
            <div className="saved-destinations-section">
              <div className="saved-destinations-header">
                <h2 className="saved-destinations-title">⭐ Mis Viajes Guardados</h2>
                <button
                  className="close-saved-btn"
                  onClick={() => setShowSavedDestinations(false)}
                  title="Cerrar"
                >
                  ✕
                </button>
              </div>
              {savedDestinations.length === 0 ? (
                <div className="no-saved-destinations">
                  <p className="no-saved-text">Aún no has guardado ningún destino</p>
                  <p className="no-saved-hint">Los destinos se guardan automáticamente cuando consultas sobre un lugar</p>
                </div>
              ) : (
                <div className="saved-destinations-grid">
                  {savedDestinations.map((dest) => (
                    <div key={dest.id} className="saved-destination-card">
                      <div className="saved-card-header">
                        <h3 className="saved-card-title">📍 {dest.destination}</h3>
                        <button
                          className="remove-saved-btn"
                          onClick={() => removeSavedDestination(dest.id)}
                          title="Eliminar de favoritos"
                        >
                          🗑️
                        </button>
                      </div>
                      <div className="saved-card-body">
                        {dest.date && (
                          <div className="saved-card-info">
                            <span className="saved-info-label">📅 Fecha:</span>
                            <span className="saved-info-value">
                              {new Date(dest.date).toLocaleDateString('es-ES', { 
                                day: 'numeric', 
                                month: 'long', 
                                year: 'numeric' 
                              })}
                            </span>
                          </div>
                        )}
                        {dest.budget && (
                          <div className="saved-card-info">
                            <span className="saved-info-label">💰 Presupuesto:</span>
                            <span className="saved-info-value">{dest.budget}</span>
                          </div>
                        )}
                        {dest.preference && (
                          <div className="saved-card-info">
                            <span className="saved-info-label">🎯 Preferencia:</span>
                            <span className="saved-info-value">{dest.preference}</span>
                          </div>
                        )}
                        {dest.weather && (
                          <div className="saved-card-info">
                            <span className="saved-info-label">🌤️ Clima:</span>
                            <span className="saved-info-value">
                              {dest.weather.temperature}°C - {dest.weather.description}
                            </span>
                          </div>
                        )}
                        {dest.timezoneInfo && (
                          <div className="saved-card-info">
                            <span className="saved-info-label">🕐 Zona Horaria:</span>
                            <span className="saved-info-value">{dest.timezoneInfo.timezone}</span>
                          </div>
                        )}
                        <div className="saved-card-info">
                          <span className="saved-info-label">💬 Consultas:</span>
                          <span className="saved-info-value">{dest.conversationCount || 0}</span>
                        </div>
                        <div className="saved-card-footer">
                          <button
                            className="load-saved-btn"
                            onClick={() => loadSavedDestination(dest)}
                          >
                            Cargar este destino
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {showForm ? (
            <form onSubmit={handleFormSubmit} className="travel-form">
              <div className="form-header">
                <h2 className="form-title">Cuéntanos sobre tu viaje</h2>
                <p className="form-subtitle">Completa este breve formulario para personalizar tu experiencia</p>
              </div>

              <div className="form-group">
                <label htmlFor="destination" className="form-label">
                  <span className="label-icon">📍</span>
                  ¿A dónde quieres viajar?
                </label>
                <input
                  type="text"
                  id="destination"
                  name="destination"
                  className="form-input"
                  placeholder="Ej: París, Tokio, Nueva York..."
                  value={formData.destination}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="date" className="form-label">
                  <span className="label-icon">📅</span>
                  ¿Cuándo?
                </label>
                <input
                  type="date"
                  id="date"
                  name="date"
                  className="form-input"
                  value={formData.date}
                  onChange={handleInputChange}
                  min={new Date().toISOString().split('T')[0]}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="budget" className="form-label">
                  <span className="label-icon">💰</span>
                  ¿Cuál es tu presupuesto aproximado?
                </label>
                <select
                  id="budget"
                  name="budget"
                  className="form-input"
                  value={formData.budget}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Selecciona un rango</option>
                  <option value="economico">Económico (menos de $500 USD)</option>
                  <option value="moderado">Moderado ($500 - $1,500 USD)</option>
                  <option value="alto">Alto ($1,500 - $3,000 USD)</option>
                  <option value="premium">Premium (más de $3,000 USD)</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">
                  <span className="label-icon">🎯</span>
                  ¿Prefieres aventura, relajación o cultura?
                </label>
                <div className="radio-group">
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="preference"
                      value="aventura"
                      checked={formData.preference === 'aventura'}
                      onChange={handleInputChange}
                      required
                    />
                    <span className="radio-label">
                      <span className="radio-emoji">🏔️</span>
                      Aventura
                    </span>
                  </label>
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="preference"
                      value="relajacion"
                      checked={formData.preference === 'relajacion'}
                      onChange={handleInputChange}
                      required
                    />
                    <span className="radio-label">
                      <span className="radio-emoji">🏖️</span>
                      Relajación
                    </span>
                  </label>
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="preference"
                      value="cultura"
                      checked={formData.preference === 'cultura'}
                      onChange={handleInputChange}
                      required
                    />
                    <span className="radio-label">
                      <span className="radio-emoji">🏛️</span>
                      Cultura
                    </span>
                  </label>
                </div>
              </div>

              <button type="submit" className="form-submit-button">
                Continuar con mi planificación
                <span className="button-arrow">→</span>
              </button>
            </form>
          ) : (
            <>
              <div className="user-info-card">
                <div className="user-info-content">
                  <h3 className="user-info-title">Tu viaje</h3>
                  <div className="user-info-details">
                    <span className="info-badge">📍 {formData.destination}</span>
                    <span className="info-badge">📅 {new Date(formData.date).toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
                    <span className="info-badge">💰 {formData.budget}</span>
                    <span className="info-badge">🎯 {formData.preference}</span>
                  </div>
                </div>
                <button 
                  className="edit-button"
                  onClick={() => setShowForm(true)}
                >
                  Editar
                </button>
              </div>

              <form onSubmit={handleChatSubmit} className="question-form">
                <div className="input-group">
                  <textarea
                    className="question-input"
                    placeholder="Haz cualquier pregunta sobre tu viaje... Alex está listo para ayudarte ✈️"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    rows="4"
                    disabled={loading}
                  />
                </div>
                <button
                  type="submit"
                  className="submit-button"
                  disabled={loading || !question.trim()}
                >
                  {loading ? 'Planificando...' : 'Planificar mi viaje'}
                </button>
              </form>

              {/* Historial de Conversaciones */}
              {conversationHistory.length > 0 && (
                <div className="conversation-history">
                  <div className="history-header">
                    <h3 className="history-title">💬 Historial de Conversación</h3>
                    <button
                      className="history-clear-btn"
                      onClick={() => {
                        setConversationHistory([]);
                        setLastDestination(null);
                      }}
                      title="Limpiar historial"
                    >
                      🗑️ Limpiar
                    </button>
                  </div>
                  <div className="history-list">
                    {conversationHistory.map((item, index) => (
                      <div key={index} className="history-item">
                        <div className="history-question">
                          <span className="history-icon">❓</span>
                          <div className="history-content">
                            <div className="history-text">{item.question}</div>
                            {item.destination && (
                              <div className="history-destination">
                                📍 {item.destination}
                              </div>
                            )}
                            <div className="history-time">
                              {new Date(item.timestamp).toLocaleTimeString('es-ES', {
                                hour: '2-digit',
                                minute: '2-digit'
                              })}
                            </div>
                          </div>
                        </div>
                        <button
                          className="history-reuse-btn"
                          onClick={() => setQuestion(item.question)}
                          title="Reutilizar esta pregunta"
                        >
                          ↻
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {response && (
                <>
                  {/* Panel de Información en Tiempo Real */}
                  {(weather || exchangeRates || timezoneInfo) && (
                    <div className="realtime-info-panel">
                      <h3 className="panel-title">📊 Información en Tiempo Real</h3>
                      <div className="info-cards-grid">
                        {weather && (
                          <div className="info-card weather-card">
                            <div className="card-header">
                              <span className="card-icon">🌤️</span>
                              <h4 className="card-title">Clima Actual</h4>
                            </div>
                            <div className="card-content">
                              <div className="weather-main">
                                <span className="temperature">{weather.temperature}°C</span>
                                <span className="feels-like">Sensación: {weather.feels_like}°C</span>
                              </div>
                              <div className="weather-details">
                                <div className="detail-item">
                                  <span className="detail-label">Condiciones:</span>
                                  <span className="detail-value">{weather.description}</span>
                                </div>
                                <div className="detail-item">
                                  <span className="detail-label">Humedad:</span>
                                  <span className="detail-value">{weather.humidity}%</span>
                                </div>
                                <div className="detail-item">
                                  <span className="detail-label">Viento:</span>
                                  <span className="detail-value">{weather.wind_speed} km/h</span>
                                </div>
                                <div className="detail-item">
                                  <span className="detail-label">Ubicación:</span>
                                  <span className="detail-value">{weather.city}, {weather.country}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}

                        {exchangeRates && (
                          <div className="info-card exchange-card">
                            <div className="card-header">
                              <span className="card-icon">💱</span>
                              <h4 className="card-title">Tipo de Cambio</h4>
                            </div>
                            <div className="card-content">
                              <div className="exchange-base">Base: USD</div>
                              <div className="exchange-rates">
                                <div className="rate-item">
                                  <span className="currency">EUR</span>
                                  <span className="rate">{exchangeRates.EUR?.toFixed(2) || 'N/A'}</span>
                                </div>
                                <div className="rate-item">
                                  <span className="currency">GBP</span>
                                  <span className="rate">{exchangeRates.GBP?.toFixed(2) || 'N/A'}</span>
                                </div>
                                <div className="rate-item">
                                  <span className="currency">MXN</span>
                                  <span className="rate">{exchangeRates.MXN?.toFixed(2) || 'N/A'}</span>
                                </div>
                                <div className="rate-item">
                                  <span className="currency">COP</span>
                                  <span className="rate">{exchangeRates.COP?.toFixed(2) || 'N/A'}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}

                        {timezoneInfo && (
                          <div className="info-card timezone-card">
                            <div className="card-header">
                              <span className="card-icon">🕐</span>
                              <h4 className="card-title">Zona Horaria</h4>
                            </div>
                            <div className="card-content">
                              <div className="timezone-main">
                                <div className="current-time">
                                  {new Date(timezoneInfo.datetime).toLocaleTimeString('es-ES', {
                                    hour: '2-digit',
                                    minute: '2-digit',
                                    second: '2-digit'
                                  })}
                                </div>
                                <div className="timezone-name">{timezoneInfo.timezone}</div>
                              </div>
                              <div className="timezone-details">
                                <div className="detail-item">
                                  <span className="detail-label">UTC Offset:</span>
                                  <span className="detail-value">{timezoneInfo.utc_offset}</span>
                                </div>
                                <div className="detail-item">
                                  <span className="detail-label">Abreviatura:</span>
                                  <span className="detail-value">{timezoneInfo.abbreviation}</span>
                                </div>
                                <div className="detail-item">
                                  <span className="detail-label">Fecha:</span>
                                  <span className="detail-value">
                                    {new Date(timezoneInfo.datetime).toLocaleDateString('es-ES', {
                                      day: 'numeric',
                                      month: 'long',
                                      year: 'numeric'
                                    })}
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Fotos del Destino - Ahora debajo de la información en tiempo real */}
                  {photos && photos.length > 0 && (
                    <div className="photos-section">
                      <h3 className="photos-title">📸 Fotos del Destino</h3>
                      <div className="photos-grid">
                        {photos.map((photo, index) => (
                          <div key={photo.id || index} className="photo-card">
                            <img 
                              src={photo.url} 
                              alt={photo.description || 'Foto del destino'}
                              className="photo-image"
                              loading="lazy"
                            />
                            <div className="photo-overlay">
                              <p className="photo-description">
                                {photo.description || 'Hermosa vista del destino'}
                              </p>
                              <p className="photo-credit">
                                Foto por{' '}
                                <a 
                                  href={photo.photographer_url} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="photo-link"
                                >
                                  {photo.photographer}
                                </a>
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="response-area">
                    <div className="response-header">
                      <h2 className="response-title">Respuesta:</h2>
                      <div className="action-buttons-row">
                        {lastDestination && (
                          <button
                            className="save-destination-btn"
                            onClick={saveDestination}
                            disabled={loading}
                            title="Guardar este destino en favoritos"
                          >
                            <span className="btn-icon">⭐</span>
                            <span className="btn-text">Guardar destino</span>
                          </button>
                        )}
                        {conversationHistory.length > 0 && (
                          <button
                            className="download-pdf-btn"
                            onClick={handleDownloadPDF}
                            disabled={loading}
                            title="Descargar itinerario completo en PDF"
                          >
                            <span className="btn-icon">📥</span>
                            <span className="btn-text">Descargar mi itinerario en PDF</span>
                          </button>
                        )}
                      </div>
                    </div>
                    <div className="response-content">
                      {response}
                    </div>
                  </div>
                </>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;

