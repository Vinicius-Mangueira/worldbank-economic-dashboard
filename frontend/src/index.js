// index.js

// Import Leaflet CSS for MapChart component
import 'leaflet/dist/leaflet.css';
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
