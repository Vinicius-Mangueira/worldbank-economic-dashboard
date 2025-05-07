// src/components/LineChart.jsx

import Plot from 'react-plotly.js';

/**
 * LineChart component
 * Renders a time-series line chart using Plotly
 * @param {Array} data - Array of objects with year and indicator_value
 */
export default function LineChart({ data }) {
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
          name: 'Value',
        },
      ]}
      layout={{
        title: 'Trend Over Time',      // Chart title
        xaxis: { title: 'Year' },      // X-axis label
        yaxis: { title: 'Value' },     // Y-axis label
        margin: { t: 50, l: 50, r: 30, b: 50 },
      }}
      style={{ width: '100%', height: '400px' }}  // Responsive width
      config={{ responsive: true }}
    />
  );
}

