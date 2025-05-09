import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapChart = ({ country }) => {
  // Coordenadas de exemplo; idealmente, obtenha as coordenadas reais do país selecionado
  const position = [0, 0];

  return (
    <div style={{ height: '400px', marginBottom: '20px' }}>
      <MapContainer center={position} zoom={2} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contribuidores'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>{country?.label || 'País selecionado'}</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default MapChart;
