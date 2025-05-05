# 🌍 World Bank Economic Dashboard

**An interactive data visualization dashboard for analyzing key macroeconomic indicators from the World Bank.**  
Built with **React**, **Plotly**, **FastAPI**, and **SQLite**.

---

## ✨ Features

- 📈 Visualize time series data (GDP, inflation, unemployment, etc.)
- 🌐 Compare countries or global regions across multiple indicators
- 🗺️ Interactive map with country-level data
- 🔮 Forecast trends using time series models (e.g. ARIMA, Prophet)
- 💾 Export filtered datasets as `.csv`

---

## 🛠️ Tech Stack

### Backend
- **Python** + **FastAPI**
- Data processing with **Pandas**
- Optional **SQLite** database for local persistence

### Frontend
- **React** + **Plotly.js**
- Responsive charts and interactive UI
- Map integration via **Leaflet.js** or **Mapbox**

---

## 🗂️ Project Structure

worldbank-economic-dashboard/
├── backend/
│ ├── app.py # FastAPI application
│ ├── requirements.txt # Python dependencies
│ └── data_loader.py # ETL scripts for data ingestion
├── frontend/
│ ├── src/ # React + Plotly dashboard UI
│ └── package.json # Frontend dependencies
├── database/
│ └── dataset.db # (Optional) Local SQLite DB
├── README.md
├── LICENSE
└── .gitignore
---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/worldbank-economic-dashboard.git
cd worldbank-economic-dashboard
2. Run the backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
3. Run the frontend (React)

cd frontend
npm install
npm start

🌍 Data Source
All data is retrieved from the World Bank Open Data API.

Make sure to cite appropriately if you use this data for academic or professional work.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

👨‍💻 Author
Developed by Vinícius Mangueira — Student of Data Science & Artificial Intelligence @ UFPB 🇧🇷

⭐️ Contributions
Pull requests are welcome! Feel free to open issues, submit suggestions, or collaborate on improvements.