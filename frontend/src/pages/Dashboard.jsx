// src/pages/Dashboard.jsx
import { useState, useEffect } from 'react'
import axios from 'axios'
import CountrySelector from '../components/CountrySelector'
import IndicatorSelector from '../components/IndicatorSelector'
import LineChart from '../components/LineChart'

export default function Dashboard() {
  const [country, setCountry] = useState('')
  const [indicator, setIndicator] = useState('')
  const [data, setData] = useState([])

  useEffect(() => {
    if (country && indicator) {
      axios.get(`/data?country=${country}&indicator=${indicator}`)
        .then(res => setData(res.data))
        .catch(console.error)
    }
  }, [country, indicator])

  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">World Bank Dashboard</h1>
      <div className="flex gap-4 mb-6">
        <CountrySelector onChange={setCountry} />
        <IndicatorSelector onChange={setIndicator} />
      </div>
      <LineChart data={data} />
    </div>
  )
}
