// src/components/IndicatorSelector.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function IndicatorSelector({ onChange }) {
  const [indicators, setIndicators] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/indicators')
      .then(res => setIndicators(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Carregando indicadores…</p>;

  return (
    <select onChange={e => onChange(e.target.value)}>
      <option value="">Selecione um indicador</option>
      {indicators.map(ind => (
        <option key={ind} value={ind}>
          {ind}
        </option>
      ))}
    </select>
  );
}
