// src/components/CountrySelector.jsx

import React, { useEffect, useState } from "react";
import Select from "react-select";
import axios from "axios";

export default function CountrySelector({ onChange }) {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    axios
      .get("/countries") // Assumes "proxy" is set in package.json
      .then((res) => {
        const opts = res.data.map((country) => ({
          value: country.id,
          label: country.name,
        }));
        setOptions(opts);
      })
      .catch((err) => {
        console.error("Failed to fetch countries:", err);
      });
  }, []);

  return (
    <Select
      options={options}           // Country options to display
      onChange={onChange}         // Handler to update selected country
      placeholder="Select a country"
      isClearable                 // Allows user to clear the selection
      aria-label="Country selector"
      styles={{
        container: (base) => ({
          ...base,
          width: 300,             // Optional: set fixed width
        }),
      }}
    />
  );
}
