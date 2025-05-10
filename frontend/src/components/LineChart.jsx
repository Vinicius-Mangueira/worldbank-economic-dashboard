
import React from 'react';
import Plot from 'react-plotly.js';

/**
 * LineChart component
 * Renders a time-series line chart using Plotly
 *
 * @param {Array<{ year: number, indicator_value: number }>} data - Array of objects with year and indicator_value
 * @param {string} title - Chart title
 */
export default function LineChart({ data, title = 'Trend Over Time' }) {
  // Return nothing if data is absent or empty
  if (!data || !Array.isArray(data) || data.length === 0) {
    return null;
  }

  const years = data.map((d) => d.year);
  const values = data.map((d) => d.indicator_value);

  return (
    <Plot
      data={[
        {
          x: years,                    // X-axis: years
          y: values,                   // Y-axis: indicator values
          type: 'scatter',
          mode: 'lines+markers',
          marker: { color: 'blue' },
          name: title,
        },
      ]}
      layout={{
        title: title,                // Chart title
        xaxis: { title: 'Year' },    // X-axis label
        yaxis: { title: title },     // Y-axis label
        margin: { t: 50, l: 50, r: 30, b: 50 },
      }}
      style={{ width: '100%', height: '400px' }}  // Responsive width
      config={{ responsive: true }}               // Make it responsive on resize
    />
  );
}
