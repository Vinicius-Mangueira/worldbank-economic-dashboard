// src/pages/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import CountrySelector from '../components/CountrySelector';
import IndicatorSelector from '../components/IndicatorSelector';
import LineChart from '../components/LineChart';
import { fetchCountries, fetchIndicators, fetchData, fetchForecast } from '../api';

export default function Dashboard() {
  const [countries, setCountries] = useState([]);
  const [indicators, setIndicators] = useState([]);
  const [country, setCountry] = useState(null);
  const [indicator, setIndicator] = useState(null);
  const [range, setRange] = useState({ start: 2000, end: 2022 });
  const [data, setData] = useState([]);
  const [forecast, setForecast] = useState([]);

  // Load country and indicator options on component mount
  useEffect(() => {
    fetchCountries().then(setCountries);
    fetchIndicators().then(setIndicators);
  }, []);

  // Fetch data when country or indicator or date range changes
  useEffect(() => {
    if (country && indicator) {
      fetchData(country.value, indicator.value, range.start, range.end)
        .then(setData)
        .catch((err) => console.error('Error fetching data:', err));
    }
  }, [country, indicator, range]);

  // Handle forecast generation
  const handleForecast = async () => {
    if (country && indicator) {
      try {
        const fc = await fetchForecast(country.value, indicator.value, 5);
        setForecast(fc);
      } catch (err) {
        console.error('Error generating forecast:', err);
      }
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>📊 Economic Dashboard</h1>

      {/* Selectors for country and indicator */}
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

      {/* Time range input */}
      <div style={{ marginBottom: 20 }}>
        <label>
          From:
          <input
            type="number"
            value={range.start}
            onChange={(e) =>
              setRange((r) => ({ ...r, start: +e.target.value }))
            }
            style={{ width: 80, marginRight: 8, marginLeft: 5 }}
          />
        </label>
        <label>
          To:
          <input
            type="number"
            value={range.end}
            onChange={(e) =>
              setRange((r) => ({ ...r, end: +e.target.value }))
            }
            style={{ width: 80, marginLeft: 5 }}
          />
        </label>
      </div>

      {/* Forecast button */}
      <button onClick={handleForecast} disabled={!country || !indicator}>
        Generate 5-Year Forecast
      </button>

      {/* Main chart */}
      {data.length > 0 && (
        <div style={{ marginTop: 30 }}>
          <LineChart
            data={data.map((d) => ({ year: d.year, indicator_value: d.value }))}
          />
        </div>
      )}

      {/* Forecast chart */}
      {forecast.length > 0 && (
        <div style={{ marginTop: 30 }}>
          <LineChart
            data={forecast.map((d) => ({
              year: d.year,
              indicator_value: d.forecast,
            }))}
          />
        </div>
      )}
    </div>
  );
}
