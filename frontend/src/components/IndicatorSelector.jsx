// src/components/IndicatorSelector.jsx

import React, { useEffect, useState } from "react";
import Select from "react-select";
import axios from "axios";

/**
 * IndicatorSelector component
 * Fetches indicator options from the backend and renders a dropdown
 */
export default function IndicatorSelector({ onChange }) {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    axios
      .get("/indicators")
      .then((res) => {
        const opts = res.data.map((indicator) => ({
          value: indicator.id,
          label: indicator.name,
        }));
        setOptions(opts);
      })
      .catch((err) => {
        console.error("Failed to fetch indicators:", err);
      });
  }, []);

  return (
    <Select
      options={options}           // Indicator options
      onChange={onChange}         // Callback when selection changes
      placeholder="Select an indicator"
      isClearable                 // Allow clearing the selection
      aria-label="Indicator selector"
      styles={{
        container: (base) => ({
          ...base,
          width: 300,             // Optional: consistent dropdown width
        }),
      }}
    />
  );
}
