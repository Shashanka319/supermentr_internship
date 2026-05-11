/**
 * WeatherService - Handles all interactions with the OpenWeatherMap API
 * @typedef {import('../types/weather.types').WeatherData} WeatherData
 * @typedef {import('../types/weather.types').WeatherError} WeatherError
 */

const API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather';
const TIMEOUT_MS = 10000; // 10 seconds

class WeatherService {
  /**
   * Fetches weather data for a given location
   * @param {string} location - City name or coordinates
   * @returns {Promise<WeatherData>} Weather data object
   * @throws {WeatherError} On API errors, timeouts, or network failures
   */
  async fetchWeather(location) {
    const apiKey = process.env.OPENWEATHER_API_KEY;
    
    if (!apiKey) {
      throw this._createError(
        'api',
        'API key is not configured. Please set OPENWEATHER_API_KEY environment variable.'
      );
    }

    // Construct request URL with query parameters
    const url = new URL(API_BASE_URL);
    url.searchParams.append('q', location);
    url.searchParams.append('appid', apiKey);
    url.searchParams.append('units', 'metric');

    // Set up AbortController for timeout handling
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
      const response = await fetch(url.toString(), {
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle HTTP error responses
      if (!response.ok) {
        if (response.status === 404) {
          throw this._createError(
            'not_found',
            'Location not found. Please check the spelling and try again.',
            response.status
          );
        }

        const errorData = await response.json().catch(() => ({}));
        throw this._createError(
          'api',
          `API error (${response.status}): ${errorData.message || response.statusText}`,
          response.status
        );
      }

      // Parse and transform successful response
      const data = await response.json();
      return this._transformResponse(data);

    } catch (error) {
      clearTimeout(timeoutId);

      // Handle abort/timeout errors
      if (error.name === 'AbortError') {
        throw this._createError(
          'timeout',
          'Request timed out. Please check your connection and try again.'
        );
      }

      // Re-throw if already a WeatherError
      if (error.type) {
        throw error;
      }

      // Handle network errors
      throw this._createError(
        'network',
        'Network error. Please check your internet connection.',
        undefined,
        error
      );
    }
  }

  /**
   * Validates API key configuration
   * @returns {boolean} True if API key is configured
   */
  isConfigured() {
    return !!process.env.OPENWEATHER_API_KEY;
  }

  /**
   * Transforms OpenWeatherMap API response to WeatherData structure
   * @private
   * @param {Object} response - Raw API response
   * @returns {WeatherData} Transformed weather data
   */
  _transformResponse(response) {
    return {
      location: `${response.name}, ${response.sys.country}`,
      temperature: response.main.temp,
      conditions: response.weather[0].description,
      icon: response.weather[0].icon,
      humidity: response.main.humidity,
      windSpeed: response.wind.speed,
      timestamp: response.dt,
    };
  }

  /**
   * Creates a structured WeatherError object
   * @private
   * @param {'timeout' | 'network' | 'api' | 'not_found'} type - Error type
   * @param {string} message - User-friendly error message
   * @param {number} [statusCode] - HTTP status code if applicable
   * @param {Error} [originalError] - Original error object for debugging
   * @returns {WeatherError} Structured error object
   */
  _createError(type, message, statusCode, originalError) {
    const error = {
      type,
      message,
    };

    if (statusCode !== undefined) {
      error.statusCode = statusCode;
    }

    if (originalError) {
      error.originalError = originalError;
    }

    return error;
  }
}

module.exports = WeatherService;
