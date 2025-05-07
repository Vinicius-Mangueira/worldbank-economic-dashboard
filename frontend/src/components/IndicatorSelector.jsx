import React, { useEffect, useState } from "react";
import Select from "react-select";
import axios from "axios";

export default function IndicatorSelector({ onChange }) {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/indicators")
      // Ou axios.get("/indicators") se usar proxy
      .then((res) => {
        const opts = res.data.map((i) => ({
          value: i.id,
          label: i.name,
        }));
        setOptions(opts);
      })
      .catch((err) => {
        console.error("Erro ao buscar indicadores:", err);
      });
  }, []);

  return (
    <Select
      options={options}
      onChange={onChange}
      placeholder="Selecione um indicador"
      isClearable
    />
  );
}
