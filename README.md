# ETL-Instant-delivery-performance
Personal ETL project using python + deliver into dashboard using Metabase 

📦 Instant Delivery Operations Analytics

End-to-End Data Engineering & BI Project

Proyek ini merupakan implementasi lengkap pipeline Data Engineering dan Business Intelligence untuk menganalisis performa pengantaran layanan Instant Delivery. Mulai dari data ingestion, cleaning, transformation, data modeling, loading ke PostgreSQL (Docker), hingga visualisasi menggunakan Metabase.

Dashboard akhir digunakan sebagai alat analisis operasional untuk mengidentifikasi performa SLA, waktu pengantaran, faktor cuaca, area, dan jarak.

🗂️ Project Structure
.
├── data/
│   └── amazon_delivery.csv
├── ingest.py
├── transform.py
├── load.py
├── docker-compose.yml
├── README.md  ← (this file)

🚀 1. Objective

Membangun pipeline lengkap untuk:

Membersihkan dan menyiapkan dataset pengiriman instant delivery.

Melakukan rekayasa fitur (area_clean, weather_group, distance_bucket, on_time_flag).

Menghitung metrik operasional seperti:

Total Orders

On-Time Delivery Rate

Delivery Time & Pickup Delay

SLA Performance by Category, Area, Distance, Weather

Menyimpan data ke PostgreSQL melalui Docker.

Menyajikan dashboard operasional menggunakan Metabase.

⚙️ 2. Tech Stack
Komponen	Teknologi
Data Storage	PostgreSQL (Dockerized)
Data Processing	Python (Pandas, NumPy)
Orchestration (optional)	Airflow-ready pipeline structure
BI Dashboard	Metabase
Environment	Docker, venv (Python)
🛠️ 3. Pipeline Overview
3.1 Ingestion (ingest.py)

File CSV dimuat ke Python menggunakan Pandas.

df = pd.read_csv("data/amazon_delivery.csv")

3.2 Transformation (transform.py)

Berikut ringkasan fitur yang ditambahkan:

✔ Clean Area Field → area_clean
Urban → Urban  
Metropolitan → Metropolitan  
Sub Urban → Non-Urban  

✔ Weather Normalization → weather_group

Clear, Sunny → Good

Cloudy, Rainy → Bad

✔ Distance Calculation → distance_km

Haversine formula digunakan untuk menghitung jarak antara store & drop location.

✔ Distance Bucketing → distance_bucket
Range	Bucket
0–5 km	Near
5–10 km	Mid-range
10–20 km	Far
>20 km	Very Far
✔ SLA Flag → on_time_flag
on_time → 1  
late → 0  

3.3 Loading (load.py)

Data hasil transformasi di-batch insert ke PostgreSQL dengan execute_batch.

INSERT INTO deliveries (...) VALUES (%s, %s, ...)

Docker PostgreSQL Setup (docker-compose.yml)
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: galahad
      POSTGRES_PASSWORD: 12345
      POSTGRES_DB: logistics_db
    ports:
      - "5433:5432"

🧱 4. Database Modeling

Tabel utama: deliveries

Column	Type	Description
order_id	text	Unique ID
agent_age	int	Courier age
store_latitude	float	Store location
drop_latitude	float	Customer location
order_datetime	timestamp	Order created
pickup_datetime	timestamp	Courier pickup
pickup_delay	int	Minutes
delivery_time	int	Minutes
sla_status	text	on_time / late
category	text	Product category
area_clean	text	Urban / Non-Urban / Metropolitan
weather_group	text	Good / Bad
distance_km	float	Calculated distance
distance_bucket	text	Near / Mid-range / Far / Very Far
on_time_flag	int	1 / 0
📊 5. Dashboard (Metabase)

Dashboard terdiri dari:

5.1 KPI Cards

Total Orders

On-Time Delivery Rate

Average Delivery Time

Average Pickup Delay

5.2 Visualizations
🔵 Daily Orders Trend

Menampilkan jumlah pesanan harian berdasarkan tanggal pesanan.

🟢 Pie Chart – On-Time vs Late Delivery Rate

Ilustrasi proporsi SLA secara keseluruhan.

📍 SLA Performance by Area

Memperlihatkan distribusi on-time & late berdasarkan lokasi pengantaran.

⛅ SLA Performance by Weather

Menilai dampak kondisi cuaca terhadap SLA.

📦 SLA Performance by Category

Top 5 & Top 10 kategori berdasarkan total pesanan + breakdown on_time/late.

🚚 Delivery Time Performance by Distance Bucket

Menunjukkan hubungan jarak dengan peluang keterlambatan.

📍 Delivery Time by Area

Rata-rata waktu antar berdasarkan area.

📝 6. How to Run the Project
1️⃣ Clone repository
git clone https://github.com/galahad/instant-delivery-analytics.git
cd instant-delivery-analytics

2️⃣ Start PostgreSQL
docker-compose up -d

3️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate

4️⃣ Install requirements
pip install -r requirements.txt

5️⃣ Run ingestion → transform → load
python ingest.py
python transform.py
python load.py

6️⃣ Open Metabase

Connect PostgreSQL

Sync & scan tables

Build dashboard

🧠 7. Key Insights (Executive Summary)

Tingkat on-time delivery sekitar 65%, menunjukkan terdapat ruang besar untuk perbaikan.

Area Metropolitan memiliki volume tertinggi tetapi juga tingkat keterlambatan yang signifikan.

Kondisi cuaca buruk menyebabkan penurunan SLA yang jelas.

Jarak Far dan Very Far meningkatkan waktu pengantaran & risiko keterlambatan.

Kategori Grocery memiliki volume pesanan tertinggi dan SLA 100% (tanpa keterlambatan).

📌 8. Improvement Ideas (Next Steps)

Tambahkan dbt untuk modular data modeling.

Tambahkan Airflow untuk scheduling pipeline otomatis.

Implementasikan alerts pada Metabase untuk SLA rendah.

Buat model prediksi late delivery menggunakan machine learning.

👤 Author

Galahad
Data Engineering & Analytics Enthusiast
