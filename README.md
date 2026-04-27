# 📦 Instant Delivery Operations Analytics

End-to-End Data Engineering & Business Intelligence Project

---

<img width="801" height="491" alt="Screenshot 2025-12-06 at 09 46 22" src="https://github.com/user-attachments/assets/cd5e4d20-3b8b-428a-8cd3-0e05b0c3a50b" />



## 📌 Background

Instant delivery services face significant operational challenges in maintaining Service Level Agreement (SLA), especially due to factors such as delivery distance, weather conditions, and geographic areas.

Delays in delivery can directly impact customer satisfaction and operational efficiency. Therefore, understanding the key drivers behind late deliveries is essential for optimizing logistics performance.

This project aims to build an end-to-end data pipeline to analyze delivery performance and uncover actionable insights.

---

## 🎯 Objectives

- Build a complete ETL pipeline (Extract, Transform, Load)
- Perform data cleaning and feature engineering
- Store processed data in a PostgreSQL database (Dockerized)
- Develop an interactive dashboard using Metabase
- Analyze operational performance and identify key delay factors

---

## 🛠️ Tech Stack

| Component        | Technology              |
|-----------------|------------------------|
| Data Processing | Python (Pandas, NumPy) |
| Database        | PostgreSQL (Docker)    |
| BI Dashboard    | Metabase               |
| Environment     | Docker, Virtual Env    |

---

## 🗂️ Project Structure

```bash
project/
├── data/
│   └── amazon_delivery.csv
├── ingest.py
├── transform.py
├── load.py
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Data Pipeline Overview

### 1. Extract (Ingestion)
```python
df = pd.read_csv("data/amazon_delivery.csv")
```

### 2. Transform (Feature Engineering)
- Area Cleaning → area_clean
- Weather Grouping → weather_group
- Distance Calculation → distance_km
- Distance Bucketing → distance_bucket
- SLA Classification → on_time_flag

### 3. Load
- Data is inserted into PostgreSQL using batch processing

---

## 🧱 Data Modeling

**Main Table: deliveries**

| Column            | Description |
|------------------|------------|
| order_id         | Unique identifier |
| agent_age        | Courier age |
| delivery_time    | Delivery duration (minutes) |
| sla_status       | on_time / late |
| area_clean       | Area classification |
| weather_group    | Weather category |
| distance_km      | Calculated distance |
| distance_bucket  | Distance grouping |
| on_time_flag     | Binary SLA indicator |

---

## 📊 Dashboard (Metabase)

### KPI Metrics
- Total Orders
- On-Time Delivery Rate
- Average Delivery Time
- Average Pickup Delay

### Visualizations
- Daily Orders Trend
- On-Time vs Late Delivery Rate
- SLA Performance by Area
- SLA Impact by Weather
- SLA Performance by Category
- Delivery Performance by Distance

---

## 🚀 How to Run

```bash
git clone https://github.com/galahad/instant-delivery-analytics.git
cd instant-delivery-analytics

docker-compose up -d

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python ingest.py
python transform.py
python load.py
```

---

## 📈 Key Insights

- On-time delivery rate is approximately 65%
- Metropolitan areas have higher delay rates
- Bad weather reduces SLA performance
- Longer distances increase delay probability
- Grocery category has best performance

---

## ⚠️ Challenges & Learnings

### Challenges
- Handling inconsistent categorical values
- Designing meaningful feature engineering
- Efficient data loading into PostgreSQL

### Learnings
- Data cleaning is critical
- Feature engineering impacts insights
- Pipeline design is key in data engineering

---

## 🔮 Future Improvements

- Integrate dbt
- Use Apache Airflow for scheduling
- Add alerting system
- Build ML model for prediction

---

## 👤 Author

Dimas Abian  
Data Engineering & Analytics Enthusiast
