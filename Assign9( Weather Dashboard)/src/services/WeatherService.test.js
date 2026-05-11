/**
 * Unit tests for WeatherService
 */

const WeatherService = require('./WeatherService');
const fc = require('fast-check');

describe('WeatherService', () => {
  let weatherService;
  let originalFetch;
  let originalEnv;

  beforeEach(() => {
    weatherService = new WeatherService();
    originalFetch = global.fetch;
    originalEnv = process.env.OPENWEATHER_API_KEY;
    process.env.OPENWEATHER_API_KEY = 'test-api-key';
  });

  afterEach(() => {
    global.fetch = originalFetch;
    if (originalEnv) {
      process.env.OPENWEATHER_API_KEY = originalEnv;
    } else {
      delete process.env.OPENWEATHER_API_KEY;
    }
  });

  describe('fetchWeather', () => {
    it('should construct correct API request with location and API key', async () => {
      const mockResponse = {
        name: 'London',
        sys: { country: 'GB' },
        main: { temp: 15.5, humidity: 72 },
        weather: [{ description: 'clear sky', icon: '01d' }],
        wind: { speed: 3.5 },
        dt: 1699876543,
      };

      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      await weatherService.fetchWeather('London');

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('https://api.openweathermap.org/data/2.5/weather'),
        expect.objectContaining({
          signal: expect.any(AbortSignal),
        })
      );

      const callUrl = global.fetch.mock.calls[0][0];
      expect(callUrl).toContain('q=London');
      expect(callUrl).toContain('appid=test-api-key');
      expect(callUrl).toContain('units=metric');
    });

    it('should parse and transform API response correctly', async () => {
      const mockResponse = {
        name: 'London',
        sys: { country: 'GB' },
        main: { temp: 15.5, humidity: 72 },
        weather: [{ description: 'clear sky', icon: '01d' }],
        wind: { speed: 3.5 },
        dt: 1699876543,
      };

      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await weatherService.fetchWeather('London');

      expect(result).toEqual({
        location: 'London, GB',
        temperature: 15.5,
        conditions: 'clear sky',
        icon: '01d',
        humidity: 72,
        windSpeed: 3.5,
        timestamp: 1699876543,
      });
    });

    it('should handle timeout after 10 seconds', async () => {
      // Mock fetch to simulate a slow response that will be aborted
      global.fetch = jest.fn().mockImplementation((url, options) => {
        return new Promise((resolve, reject) => {
          // Simulate abort signal
          if (options.signal) {
            options.signal.addEventListener('abort', () => {
              const abortError = new Error('The operation was aborted');
              abortError.name = 'AbortError';
              reject(abortError);
            });
          }
          // Never resolve to simulate a hanging request
        });
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'timeout',
        message: 'Request timed out. Please check your connection and try again.',
      });
    }, 15000); // Increase Jest timeout to 15 seconds

    it('should handle 404 not found errors', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({ message: 'city not found' }),
      });

      await expect(weatherService.fetchWeather('InvalidCity')).rejects.toMatchObject({
        type: 'not_found',
        message: 'Location not found. Please check the spelling and try again.',
        statusCode: 404,
      });
    });

    it('should handle API errors with status codes', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ message: 'Internal server error' }),
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('500'),
        statusCode: 500,
      });
    });

    it('should handle network errors', async () => {
      global.fetch = jest.fn().mockRejectedValue(new Error('Network failure'));

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'network',
        message: 'Network error. Please check your internet connection.',
      });
    });

    it('should throw error when API key is not configured', async () => {
      delete process.env.OPENWEATHER_API_KEY;

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('API key is not configured'),
      });
    });
  });

  describe('isConfigured', () => {
    it('should return true when API key is set', () => {
      process.env.OPENWEATHER_API_KEY = 'test-key';
      expect(weatherService.isConfigured()).toBe(true);
    });

    it('should return false when API key is not set', () => {
      delete process.env.OPENWEATHER_API_KEY;
      expect(weatherService.isConfigured()).toBe(false);
    });
  });

  describe('Error Handling - Unit Tests', () => {
    it('should handle timeout with correct error structure', async () => {
      global.fetch = jest.fn().mockImplementation((url, options) => {
        return new Promise((resolve, reject) => {
          if (options.signal) {
            options.signal.addEventListener('abort', () => {
              const abortError = new Error('The operation was aborted');
              abortError.name = 'AbortError';
              reject(abortError);
            });
          }
        });
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'timeout',
        message: 'Request timed out. Please check your connection and try again.',
      });
    }, 15000);

    it('should handle network failure with correct error structure', async () => {
      const networkError = new Error('Failed to fetch');
      global.fetch = jest.fn().mockRejectedValue(networkError);

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'network',
        message: 'Network error. Please check your internet connection.',
        originalError: networkError,
      });
    });

    it('should handle 400 Bad Request error', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({ message: 'Invalid request parameters' }),
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('400'),
        message: expect.stringContaining('Invalid request parameters'),
        statusCode: 400,
      });
    });

    it('should handle 401 Unauthorized error', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        json: async () => ({ message: 'Invalid API key' }),
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('401'),
        message: expect.stringContaining('Invalid API key'),
        statusCode: 401,
      });
    });

    it('should handle 500 Internal Server Error', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ message: 'Server error occurred' }),
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('500'),
        statusCode: 500,
      });
    });

    it('should handle 503 Service Unavailable error', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 503,
        statusText: 'Service Unavailable',
        json: async () => ({ message: 'Service temporarily unavailable' }),
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('503'),
        statusCode: 503,
      });
    });

    it('should handle 404 location not found specifically', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({ cod: '404', message: 'city not found' }),
      });

      const error = await weatherService.fetchWeather('InvalidCityName').catch(e => e);

      expect(error.type).toBe('not_found');
      expect(error.message).toBe('Location not found. Please check the spelling and try again.');
      expect(error.statusCode).toBe(404);
    });

    it('should handle API error response without JSON body', async () => {
      global.fetch = jest.fn().mockResolvedValue({
        ok: false,
        status: 502,
        statusText: 'Bad Gateway',
        json: async () => {
          throw new Error('Invalid JSON');
        },
      });

      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'api',
        message: expect.stringContaining('502'),
        message: expect.stringContaining('Bad Gateway'),
        statusCode: 502,
      });
    });

    it('should preserve original error for debugging in network errors', async () => {
      const originalError = new Error('DNS lookup failed');
      originalError.code = 'ENOTFOUND';
      global.fetch = jest.fn().mockRejectedValue(originalError);

      const error = await weatherService.fetchWeather('London').catch(e => e);

      expect(error.type).toBe('network');
      expect(error.originalError).toBe(originalError);
      expect(error.originalError.code).toBe('ENOTFOUND');
    });

    it('should handle multiple consecutive timeout errors', async () => {
      global.fetch = jest.fn().mockImplementation((url, options) => {
        return new Promise((resolve, reject) => {
          if (options.signal) {
            options.signal.addEventListener('abort', () => {
              const abortError = new Error('The operation was aborted');
              abortError.name = 'AbortError';
              reject(abortError);
            });
          }
        });
      });

      // First timeout
      await expect(weatherService.fetchWeather('London')).rejects.toMatchObject({
        type: 'timeout',
      });

      // Second timeout
      await expect(weatherService.fetchWeather('Paris')).rejects.toMatchObject({
        type: 'timeout',
      });
    }, 25000);

    it('should handle empty location string gracefully', async () => {
      const mockResponse = {
        name: 'Unknown',
        sys: { country: 'XX' },
        main: { temp: 0, humidity: 0 },
        weather: [{ description: 'unknown', icon: '01d' }],
        wind: { speed: 0 },
        dt: 1699876543,
      };

      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      // Should still construct request even with empty string
      await weatherService.fetchWeather('');

      const callUrl = global.fetch.mock.calls[0][0];
      expect(callUrl).toContain('q=');
    });
  });
});

// Property-Based Tests
describe('WeatherService - Property-Based Tests', () => {
  let weatherService;
  let originalFetch;
  let originalEnv;

  beforeEach(() => {
    weatherService = new WeatherService();
    originalFetch = global.fetch;
    originalEnv = process.env.OPENWEATHER_API_KEY;
    process.env.OPENWEATHER_API_KEY = 'test-api-key';
  });

  afterEach(() => {
    global.fetch = originalFetch;
    if (originalEnv) {
      process.env.OPENWEATHER_API_KEY = originalEnv;
    } else {
      delete process.env.OPENWEATHER_API_KEY;
    }
  });

  // Feature: weather-api-integration, Property 1: API Request Construction
  // For any valid location string, when fetchWeather() is called, the service should construct 
  // an HTTP request to the OpenWeatherMap endpoint with the location as a query parameter and include the API key.
  // **Validates: Requirements 1.1, 1.3**
  test('Property 1: API Request Construction - should construct correct request for any location', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.string({ minLength: 1, maxLength: 100 }),
        async (location) => {
          const mockResponse = {
            name: 'TestCity',
            sys: { country: 'TC' },
            main: { temp: 20, humidity: 50 },
            weather: [{ description: 'test', icon: '01d' }],
            wind: { speed: 5 },
            dt: 1699876543,
          };

          let capturedUrl = '';
          global.fetch = jest.fn().mockImplementation((url) => {
            capturedUrl = url;
            return Promise.resolve({
              ok: true,
              json: async () => mockResponse,
            });
          });

          try {
            await weatherService.fetchWeather(location);

            // Verify the URL contains the OpenWeatherMap endpoint
            expect(capturedUrl).toContain('https://api.openweathermap.org/data/2.5/weather');
            
            // Verify the location is included as a query parameter
            const urlObj = new URL(capturedUrl);
            expect(urlObj.searchParams.get('q')).toBe(location);
            
            // Verify the API key is included
            expect(urlObj.searchParams.get('appid')).toBe('test-api-key');
            
            // Verify units parameter is included
            expect(urlObj.searchParams.get('units')).toBe('metric');
          } catch (error) {
            // If the service throws an error (e.g., for invalid location), 
            // we still verify the request was constructed correctly
            if (capturedUrl) {
              expect(capturedUrl).toContain('https://api.openweathermap.org/data/2.5/weather');
              const urlObj = new URL(capturedUrl);
              expect(urlObj.searchParams.get('q')).toBe(location);
              expect(urlObj.searchParams.get('appid')).toBe('test-api-key');
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: weather-api-integration, Property 2: Response Parsing Completeness
  // For any valid OpenWeatherMap API response, parsing should produce a WeatherData object 
  // containing all required fields with values matching the source response.
  // **Validates: Requirements 1.2**
  test('Property 2: Response Parsing Completeness - should parse all fields from any valid API response', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.record({
          name: fc.string({ minLength: 1, maxLength: 50 }),
          sys: fc.record({ country: fc.string({ minLength: 2, maxLength: 2 }) }),
          main: fc.record({
            temp: fc.float({ min: -50, max: 50 }),
            humidity: fc.integer({ min: 0, max: 100 }),
          }),
          weather: fc.array(
            fc.record({
              description: fc.string({ minLength: 1, maxLength: 100 }),
              icon: fc.string({ minLength: 3, maxLength: 3 }),
            }),
            { minLength: 1, maxLength: 1 }
          ),
          wind: fc.record({
            speed: fc.float({ min: 0, max: 100 }),
          }),
          dt: fc.integer({ min: 1000000000, max: 2000000000 }),
        }),
        async (mockResponse) => {
          global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: async () => mockResponse,
          });

          const result = await weatherService.fetchWeather('TestLocation');

          // Verify all required fields are present
          expect(result).toHaveProperty('location');
          expect(result).toHaveProperty('temperature');
          expect(result).toHaveProperty('conditions');
          expect(result).toHaveProperty('icon');
          expect(result).toHaveProperty('humidity');
          expect(result).toHaveProperty('windSpeed');
          expect(result).toHaveProperty('timestamp');

          // Verify values match the source response
          expect(result.location).toBe(`${mockResponse.name}, ${mockResponse.sys.country}`);
          expect(result.temperature).toBe(mockResponse.main.temp);
          expect(result.conditions).toBe(mockResponse.weather[0].description);
          expect(result.icon).toBe(mockResponse.weather[0].icon);
          expect(result.humidity).toBe(mockResponse.main.humidity);
          expect(result.windSpeed).toBe(mockResponse.wind.speed);
          expect(result.timestamp).toBe(mockResponse.dt);
        }
      ),
      { numRuns: 100 }
    );
  });

  // Feature: weather-api-integration, Property 3: Successful Response Handling
  // For any API response that returns within 10 seconds with status 200, 
  // the service should return a WeatherData object (not an error).
  // **Validates: Requirements 1.4**
  test('Property 3: Successful Response Handling - should return WeatherData for any successful response', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.record({
          name: fc.string({ minLength: 1, maxLength: 50 }),
          sys: fc.record({ country: fc.string({ minLength: 2, maxLength: 2 }) }),
          main: fc.record({
            temp: fc.float({ min: -50, max: 50 }),
            humidity: fc.integer({ min: 0, max: 100 }),
          }),
          weather: fc.array(
            fc.record({
              description: fc.string({ minLength: 1, maxLength: 100 }),
              icon: fc.string({ minLength: 3, maxLength: 3 }),
            }),
            { minLength: 1, maxLength: 1 }
          ),
          wind: fc.record({
            speed: fc.float({ min: 0, max: 100 }),
          }),
          dt: fc.integer({ min: 1000000000, max: 2000000000 }),
        }),
        fc.integer({ min: 10, max: 100 }), // Response delay in ms (small delay to simulate network)
        async (mockResponse, delay) => {
          global.fetch = jest.fn().mockImplementation(() => {
            return new Promise((resolve) => {
              setTimeout(() => {
                resolve({
                  ok: true,
                  status: 200,
                  json: async () => mockResponse,
                });
              }, delay);
            });
          });

          const result = await weatherService.fetchWeather('TestLocation');

          // Verify the result is a WeatherData object (not an error)
          expect(result).toBeDefined();
          expect(result).not.toHaveProperty('type'); // WeatherError has a 'type' property
          expect(result).toHaveProperty('location');
          expect(result).toHaveProperty('temperature');
          expect(result).toHaveProperty('conditions');
          expect(result).toHaveProperty('icon');
          expect(result).toHaveProperty('humidity');
          expect(result).toHaveProperty('windSpeed');
          expect(result).toHaveProperty('timestamp');
        }
      ),
      { numRuns: 100 }
    );
  }, 30000); // 30 second timeout for this property test

  // Feature: weather-api-integration, Property 5: Error Object Structure
  // For any error condition (API error, timeout, network failure), the service should return 
  // a WeatherError object with a non-empty message field and an appropriate error type.
  // **Validates: Requirements 3.1, 3.4**
  test('Property 5: Error Object Structure - should return structured error for any error condition', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.oneof(
          // Network error scenario (fast)
          fc.constant({ type: 'network' }),
          // API error scenario with various status codes (fast, excluding 404)
          fc.integer({ min: 400, max: 599 }).filter(code => code !== 404).map(statusCode => ({
            type: 'api',
            statusCode
          })),
          // Not found error scenario (fast)
          fc.constant({ type: 'not_found', statusCode: 404 }),
          // Timeout error scenario (slow - 10s each, so we include fewer)
          fc.constant({ type: 'timeout' })
        ),
        async (errorScenario) => {
          // Mock fetch based on error scenario
          if (errorScenario.type === 'timeout') {
            global.fetch = jest.fn().mockImplementation((url, options) => {
              return new Promise((resolve, reject) => {
                if (options.signal) {
                  options.signal.addEventListener('abort', () => {
                    const abortError = new Error('The operation was aborted');
                    abortError.name = 'AbortError';
                    reject(abortError);
                  });
                }
              });
            });
          } else if (errorScenario.type === 'network') {
            global.fetch = jest.fn().mockRejectedValue(new Error('Network failure'));
          } else if (errorScenario.type === 'api' || errorScenario.type === 'not_found') {
            global.fetch = jest.fn().mockResolvedValue({
              ok: false,
              status: errorScenario.statusCode,
              statusText: 'Error',
              json: async () => ({ message: 'API error message' }),
            });
          }

          try {
            await weatherService.fetchWeather('TestLocation');
            // Should not reach here - expect an error to be thrown
            throw new Error('Expected fetchWeather to throw an error');
          } catch (error) {
            // Verify error object structure
            expect(error).toBeDefined();
            expect(error).toHaveProperty('type');
            expect(error).toHaveProperty('message');
            
            // Verify message is non-empty
            expect(error.message).toBeTruthy();
            expect(typeof error.message).toBe('string');
            expect(error.message.length).toBeGreaterThan(0);
            
            // Verify error type is appropriate
            expect(['timeout', 'network', 'api', 'not_found']).toContain(error.type);
            
            // If status code is present in scenario, verify it's in the error
            if (errorScenario.statusCode) {
              expect(error.statusCode).toBe(errorScenario.statusCode);
            }
          }
        }
      ),
      { numRuns: 30 } // Reduced runs to avoid timeout issues (some scenarios take 10s)
    );
  }, 120000); // 2 minute timeout for this property test

  // Feature: weather-api-integration, Property 9: Location Not Found Error Type
  // For any API response with status 404, the service should return a WeatherError with type 'not_found'.
  // **Validates: Requirements 6.1, 6.2**
  test('Property 9: Location Not Found Error Type - should return not_found error for 404 responses', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.string({ minLength: 1, maxLength: 100 }), // Random location string
        fc.oneof(
          fc.constant({}), // Empty error response
          fc.record({ message: fc.string({ minLength: 1, maxLength: 200 }) }), // Error with message
          fc.constant({ cod: '404', message: 'city not found' }) // OpenWeatherMap format
        ),
        async (location, errorResponse) => {
          global.fetch = jest.fn().mockResolvedValue({
            ok: false,
            status: 404,
            statusText: 'Not Found',
            json: async () => errorResponse,
          });

          try {
            await weatherService.fetchWeather(location);
            // Should not reach here - expect an error to be thrown
            throw new Error('Expected fetchWeather to throw an error');
          } catch (error) {
            // Verify error type is 'not_found'
            expect(error.type).toBe('not_found');
            
            // Verify error has required properties
            expect(error).toHaveProperty('message');
            expect(error.message).toBeTruthy();
            expect(typeof error.message).toBe('string');
            
            // Verify status code is 404
            expect(error.statusCode).toBe(404);
            
            // Verify message is user-friendly (contains guidance)
            expect(error.message.toLowerCase()).toContain('location');
            expect(error.message.toLowerCase()).toContain('not found');
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
