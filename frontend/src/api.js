// frontend/src/api.js
import axios from 'axios';

// Usa o proxy do package.json para apontar a "/" ao seu FastAPI em :8000
const api = axios.create({
  baseURL: '/',
  timeout: 5000,
});

// exporta funções para cada endpoint
export const fetchCountries = () =>
  api.get('/countries').then(res => res.data);

export const fetchIndicators = () =>
  api.get('/indicators').then(res => res.data);

export const fetchData = (country, indicator, start, end) =>
  api
    .get('/data', { params: { country, indicator, start, end } })
    .then(res => res.data);

export const fetchForecast = (country, indicator, yearsAhead = 5) =>
  api
    .get('/forecast', { params: { country, indicator, years_ahead: yearsAhead } })
    .then(res => res.data);
