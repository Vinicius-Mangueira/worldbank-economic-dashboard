// src/api.js

import axios from 'axios';

// Create an axios instance with a 15-second timeout and base URL
const apiClient = axios.create({
  baseURL: '/',     // Relies on the proxy in package.json pointing to http://localhost:8000
  timeout: 15000,   // 15 seconds timeout for slower endpoints
});

/**
 * Fetch the list of countries from the backend.
 * @returns {Promise<Array<{value: string, label: string}>>}
 */
export async function fetchCountries() {
  const res = await apiClient.get('/countries');
  // Map API response to { value, label } format for react-select
  return res.data.map((c) => ({ value: c.code, label: c.name }));
}

/**
 * Fetch the list of indicators from the backend.
 * @returns {Promise<Array<{value: string, label: string}>>}
 */
export async function fetchIndicators() {
  const res = await apiClient.get('/indicators');
  // Map API response to { value, label } format for react-select
  return res.data.map((i) => ({ value: i.code, label: i.name }));
}

/**
 * Fetch historical data for a given country and indicator.
 * @param {string} countryCode - ISO code of the country.
 * @param {string} indicatorCode - World Bank indicator code.
 * @param {number} startYear - Start year for data.
 * @param {number} endYear - End year for data.
 * @returns {Promise<Array<{year: number, value: number}>>}
 */
export async function fetchData(countryCode, indicatorCode, startYear, endYear) {
  const res = await apiClient.get('/data', {
    params: {
      country: countryCode,
      indicator: indicatorCode,
      start: startYear,
      end: endYear,
    },
  });
  // Expecting format: [{ year: 2000, value: 1000 }, …]
  return res.data;
}

/**
 * Fetch forecast data for a given country and indicator.
 * @param {string} countryCode - ISO code of the country.
 * @param {string} indicatorCode - World Bank indicator code.
 * @param {number} yearsAhead - Number of years to forecast.
 * @returns {Promise<Array<{year: number, forecast: number}>>}
 */
export async function fetchForecast(countryCode, indicatorCode, yearsAhead) {
  const res = await apiClient.get('/forecast', {
    params: {
      country: countryCode,
      indicator: indicatorCode,
      years_ahead: yearsAhead,
    },
  });
  // Expecting format: [{ year: 2023, forecast: 1100 }, …]
  return res.data;
}

