# 🌍 World Bank Economic Dashboard

**An interactive data visualization dashboard for analyzing key macroeconomic indicators from the World Bank.**
Built with **React**, **Plotly.js**, **FastAPI**, and **SQLite**.

---

## ✨ Features

* 📈 Visualize time series data (GDP, inflation, unemployment, etc.)
* 🌐 Compare countries or global regions across multiple indicators
* 🗺️ Interactive map with country-level data
* 🔮 Forecast trends using time series models (ARIMA, Prophet)
* 💾 Export filtered datasets as `.csv`

---

## 🛠️ Tech Stack

### Backend

* **Python** & **FastAPI**
* **Pandas** for data processing
* **SQLite** for optional local persistence

### Frontend

* **React** & **Plotly.js**
* **Leaflet.js** for map visualization
* **Axios** for API requests

---

## 🗂️ Project Structure

```
worldbank-economic-dashboard/
├── backend/                # FastAPI backend
│   ├── app.py              # API routes
│   ├── data_loader.py      # ETL scripts for data ingestion
│   ├── forecast.py         # Forecast logic
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── public/             # Static assets
│   ├── src/                # React components and pages
│   │   ├── api.js
│   │   ├── components/
│   │   └── pages/
│   └── package.json        # Frontend dependencies
├── database/               # Optional SQLite database
│   └── dataset.db
├── .gitignore
├── README.md               # This file
└── LICENSE
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Vinicius-Mangueira/worldbank-economic-dashboard.git
cd worldbank-economic-dashboard
```

### 2. Run the Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

### 3. Run the Frontend (React)

```bash
cd ../frontend
npm install
npm start
```

The dashboard will open at `http://localhost:3000`.

---

## 💡 Usage Examples

* **Fetch historical data (cURL):**

  ```bash
  curl "http://127.0.0.1:8000/data?country=BRA&indicator=NY.GDP.PCAP.CD&from=2000&to=2020"
  ```

* **Generate a forecast (cURL):**

  ```bash
  curl -X POST "http://127.0.0.1:8000/forecast" \
    -H 'Content-Type: application/json' \
    -d '{ "country": "BRA", "indicator": "NY.GDP.PCAP.CD", "from": 2000, "to": 2020, "years_ahead": 5 }'
  ```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Developed by Vinícius Mangueira — Student of Data Science & Artificial Intelligence @ UFPB 🇧🇷

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

*Made with ❤️ by Vinícius Mangueira*
