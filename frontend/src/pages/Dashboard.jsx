// src/pages/Dashboard.jsx
import React, { useState, useEffect } from "react";
import CountrySelector from "../components/CountrySelector";
import IndicatorSelector from "../components/IndicatorSelector";
import LineChart from "../components/LineChart";
import { fetchData } from "../api";

export default function Dashboard() {
  const [country, setCountry] = useState(null);
  const [indicator, setIndicator] = useState(null);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (country && indicator) {
      fetchData(country.value, indicator.value, 2000, 2020)
        .then((data) => setChartData(data))
        .catch((err) => {
          console.error("Erro ao buscar dados:", err);
          setChartData([]);
        });
    }
  }, [country, indicator]);

  return (
    <div style={{ padding: 20, background: "#fafafa" }}>
      <h1>🌍 Dashboard Econômico</h1>

      <div style={{ display: "flex", gap: 20, marginBottom: 20 }}>
        <CountrySelector onChange={setCountry} />
        <IndicatorSelector onChange={setIndicator} />
      </div>

      {chartData.length > 0 ? (
        <LineChart data={chartData} />
      ) : (
        <p>Selecione um país e um indicador para ver o gráfico.</p>
      )}
    </div>
  );
}
