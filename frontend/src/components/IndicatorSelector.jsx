// src/components/IndicatorSelector.jsx

import React from "react";
import Select from "react-select";

/**
 * IndicatorSelector component
 * Receives options, value and onChange props from parent (Dashboard)
 */
export default function IndicatorSelector({ options, value, onChange }) {
  return (
    <Select
      options={options}     // Array of { value, label }
      value={value}         // Current selected option
      onChange={onChange}   // Callback to update parent state
      placeholder="Select an indicator"
      isClearable
      aria-label="Indicator selector"
      styles={{
        container: (base) => ({
          ...base,
          width: 300,
        }),
      }}
    />
  );
}

