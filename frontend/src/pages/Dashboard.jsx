// src/pages/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import CountrySelector from '../components/CountrySelector';
import IndicatorSelector from '../components/IndicatorSelector';
import LineChart from '../components/LineChart';
import { fetchCountries, fetchIndicators, fetchData, fetchForecast } from '../api';

export default function Dashboard() {
  // State hooks for selectors, data, loading, and error
  const [countries, setCountries] = useState([]);
  const [indicators, setIndicators] = useState([]);
  const [country, setCountry] = useState(null);
  const [indicator, setIndicator] = useState(null);
  const [range, setRange] = useState({ start: 2000, end: 2022 });
  const [data, setData] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Load country and indicator options on mount
  useEffect(() => {
    fetchCountries()
      .then(setCountries)
      .catch((err) => console.error('Error loading countries:', err));

    fetchIndicators()
      .then(setIndicators)
      .catch((err) => console.error('Error loading indicators:', err));
  }, []);

  // Fetch data when selections or range change
  useEffect(() => {
    if (country && indicator) {
      setErrorMessage('');           // Clear previous errors
      setLoading(true);
      fetchData(country.value, indicator.value, range.start, range.end)
        .then(setData)
        .catch((err) => {
          console.error('Error fetching data:', err);
          setErrorMessage('Failed to load data. Please try again.');
        })
        .finally(() => setLoading(false));
    }
  }, [country, indicator, range]);

  // Handle forecast generation via button
  const handleForecast = async () => {
    if (!country || !indicator) return;
    setErrorMessage('');
    setLoading(true);
    try {
      const fc = await fetchForecast(country.value, indicator.value, 5);
      setForecast(fc);
    } catch (err) {
      console.error('Error generating forecast:', err);
      setErrorMessage('Failed to generate forecast. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>📊 Economic Dashboard</h1>

      {/* Country and Indicator Selectors */}
      <div style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
        <CountrySelector
          options={countries}
          value={country}
          onChange={setCountry}
        />
        <IndicatorSelector
          options={indicators}
          value={indicator}
          onChange={setIndicator}
        />
      </div>

      {/* Date range inputs */}
      <div style={{ marginBottom: 20, display: 'flex', gap: 16 }}>
        <label>
          From:
          <input
            type="number"
            value={range.start}
            onChange={(e) => setRange((r) => ({ ...r, start: +e.target.value }))}
            style={{ width: 80, marginLeft: 8 }}
          />
        </label>
        <label>
          To:
          <input
            type="number"
            value={range.end}
            onChange={(e) => setRange((r) => ({ ...r, end: +e.target.value }))}
            style={{ width: 80, marginLeft: 8 }}
          />
        </label>
      </div>

      {/* Forecast button and loading state */}
      <button
        onClick={handleForecast}
        disabled={!country || !indicator || loading}
        style={{ marginBottom: 20 }}
      >
        {loading ? 'Loading...' : 'Generate 5-Year Forecast'}
      </button>

      {/* Error message */}
      {errorMessage && (
        <div style={{ color: 'red', marginBottom: 20 }}>
          {errorMessage}
        </div>
      )}

      {/* Render main data chart */}
      {data.length > 0 && !loading && (
        <div style={{ marginBottom: 40 }}>
          <LineChart data={data.map((d) => ({ year: d.year, indicator_value: d.value }))} />
        </div>
      )}

      {/* Render forecast chart */}
      {forecast.length > 0 && !loading && (
        <div>
          <LineChart data={forecast.map((d) => ({ year: d.year, indicator_value: d.forecast }))} />
        </div>
      )}
    </div>
  );
}
