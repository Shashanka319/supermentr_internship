# Weather API Integration

A React-based weather application that fetches and displays current weather data using the OpenWeatherMap API.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure API key:
   - Copy `.env.example` to `.env`
   - Add your OpenWeatherMap API key to `.env`:
     ```
     OPENWEATHER_API_KEY=your_actual_api_key
     ```

3. Run tests:
   ```bash
   npm test
   ```

## Project Structure

```
src/
├── components/     # React UI components
├── services/       # API communication logic
├── types/          # Type definitions (JSDoc)
└── utils/          # Helper functions
```

## Features

- Fetch current weather data for any location
- Display loading states during API requests
- Handle errors with user-friendly messages
- Retry functionality for failed requests
- 10-second timeout for API requests

## Testing

The project uses Jest and React Testing Library for unit tests, and fast-check for property-based testing.

- Run all tests: `npm test`
- Run tests in watch mode: `npm run test:watch`
- Generate coverage report: `npm run test:coverage`
