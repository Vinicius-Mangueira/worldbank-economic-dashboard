# World Bank Economic Dashboard

An **interactive** and **responsive** data visualization dashboard for exploring key macroeconomic indicators from the World Bank Open Data API. The dashboard allows researchers, policymakers, students, and data enthusiasts to visualize time series trends, compare countries and regions, and export data for further analysis.

---

## 🚀 Features

* **Time Series Visualization**: Explore indicators such as GDP, inflation, unemployment, and more.
* **Comparative Analysis**: Compare multiple countries or regions side-by-side.
* **Interactive Mapping**: View country-level data on a dynamic, zoomable world map.
* **Forecasting**: Preview short-term forecasts powered by ARIMA or Facebook Prophet models.
* **Data Export**: Download filtered datasets in CSV format for offline analysis.
* **Responsive Design**: Accessible on desktop, tablet, and mobile devices.

---

## 🔧 Tech Stack

**Backend**

* **FastAPI**: High-performance API framework for Python.
* **Pandas**: Data ingestion and preprocessing.
* **SQLite** (optional): Local persistence of cleaned datasets.
* **ARIMA & Prophet**: Time series forecasting libraries.

**Frontend**

* **React**: Component-based UI library.
* **Plotly.js**: Interactive charting library.
* **Leaflet.js**: Map rendering with tile layers.
* **Tailwind CSS**: Utility-first styling framework.

---

## 📂 Project Structure

```
worldbank-economic-dashboard/
├── backend/
│   ├── app.py             # FastAPI application entrypoint
│   ├── data_loader.py     # ETL scripts: fetch & clean World Bank data
│   ├── models/            # Forecasting model definitions
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable React components (charts, maps, filters)
│   │   ├── pages/         # Page views (Dashboard, Comparison, Forecast)
│   │   └── App.jsx        # Main application component
│   └── package.json       # Frontend dependencies
├── database/
│   └── dataset.db         # (Optional) Preloaded SQLite database
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📥 Installation & Setup

### Prerequisites

* **Python 3.8+**
* **Node.js 14+ & npm**
* **Git**

### 1. Clone the repository

```bash
git clone https://github.com/Vinicius-Mangueira/worldbank-economic-dashboard.git
cd worldbank-economic-dashboard
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate       # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

1. **Configure Environment**: Copy `.env.example` to `.env` and set any API keys (if required).
2. **Data Ingestion**: Run the data loader to fetch and store indicators:

   ```bash
   python data_loader.py
   ```
3. **Start the API Server**:

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run start
```

The dashboard will be available at `http://localhost:3000` and the API at `http://localhost:8000`.

---

## 💡 Usage

1. **Navigate** to the Dashboard page to see global trends.
2. **Filter** by indicator (e.g., `GDP`), time range, and countries.
3. **Compare** multiple selections side-by-side in the Comparison view.
4. **Switch** to Forecast view to generate short-term projections.
5. **Export** any filtered dataset using the `Download CSV` button.

---

## 🗺️ Data Sources

* **World Bank Open Data API**: [https://data.worldbank.org](https://data.worldbank.org)
* All data is fetched in real time via REST API endpoints.
* See `data_loader.py` for details on endpoints and data cleaning steps.



## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests for:

1. Bug reports or feature requests.
2. Improvements to data processing or visualization.
3. Documentation enhancements.

Steps to contribute:

1. **Fork** the repo.
2. **Create** a feature branch (`git checkout -b feature/YourFeature`).
3. **Commit** your changes (`git commit -m 'Add your feature'`).
4. **Push** to your fork (`git push origin feature/YourFeature`).
5. **Open** a Pull Request.

Please adhere to the existing code style and include clear descriptions.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

**Vinícius Mangueira**
Data Science & AI Student @ UFPB
Email: [viniciusmangueira04@gmail.com](mailto:viniciusmangueira04@gmail.com)

Feel free to reach out for questions or collaboration!

LinkedIn: [https://www.linkedin.com/in/vinicius-mangueira-0b8285224/](https://www.linkedin.com/in/vinicius-mangueira-0b8285224/)
