import React, { useEffect, useState } from "react";
import Select from "react-select";
import axios from "axios";

export default function CountrySelector({ onChange }) {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/countries")
      // Se usar "proxy" no package.json, pode ser só axios.get("/countries")
      .then((res) => {
        const opts = res.data.map((c) => ({
          value: c.id,
          label: c.name,
        }));
        setOptions(opts);
      })
      .catch((err) => {
        console.error("Erro ao buscar países:", err);
      });
  }, []);

  return (
    <Select
      options={options}
      onChange={onChange}
      placeholder="Selecione um país"
      isClearable
    />
  );
}
