// src/components/CountrySelector.jsx
import { useState, useEffect } from 'react'
import axios from 'axios'

export default function CountrySelector({ onChange }) {
  const [countries, setCountries] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get('/countries')
      .then(res => setCountries(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p>Carregando países…</p>

  return (
    <select onChange={e => onChange(e.target.value)}>
      <option value="">Selecione um país</option>
      {countries.map(c => (
        <option key={c.code} value={c.code}>
          {c.name}
        </option>
      ))}
    </select>
  )
}
