// src/components/LineChart.jsx
import Plot from 'react-plotly.js';

export default function LineChart({ data }) {
  const years = data.map(d => d.year);
  const values = data.map(d => d.indicator_value);

  return (
    <Plot
      data={[{ x: years, y: values, type: 'scatter', mode: 'lines+markers' }]}
      layout={{ title: 'Evolução ao longo dos anos' }}
      style={{ width: '100%', height: '400px' }}
    />
  );
}
