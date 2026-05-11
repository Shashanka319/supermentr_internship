/**
 * Type definitions for Weather API Integration
 * These JSDoc type definitions provide type safety and IDE autocomplete support
 */

/**
 * Standardized weather data structure
 * @typedef {Object} WeatherData
 * @property {string} location - City name and country code (e.g., "London, GB")
 * @property {number} temperature - Temperature in Celsius
 * @property {string} conditions - Weather condition description (e.g., "clear sky")
 * @property {string} icon - Weather icon code from OpenWeatherMap
 * @property {number} humidity - Humidity percentage (0-100)
 * @property {number} windSpeed - Wind speed in meters per second
 * @property {number} timestamp - Unix timestamp of when the data was recorded
 */

/**
 * Structured error information for weather API failures
 * @typedef {Object} WeatherError
 * @property {'timeout' | 'network' | 'api' | 'not_found'} type - Error category
 * @property {string} message - User-friendly error message
 * @property {number} [statusCode] - HTTP status code if applicable
 * @property {Error} [originalError] - Original error object for debugging
 */

// Export empty object to make this a module
export {};
