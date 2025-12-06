import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

# Optional: centralize DB config here
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,       # sesuaikan jika perlu
    "user": "galahad",
    "password": "12345",
    "dbname": "logistics_db",
}

def load_to_postgres(df: pd.DataFrame, batch_size: int = 1000):
    """
    Load DataFrame ke tabel `deliveries`.
    Pastikan transformasi sudah dijalankan sehingga kolom baru tersedia.
    """

    # Convert NaN / NaT -> None (Postgres friendly)
    df = df.where(pd.notnull(df), None)

    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        insert_query = """
        INSERT INTO deliveries (
            order_id,
            agent_age,
            agent_rating,
            store_latitude,
            store_longitude,
            drop_latitude,
            drop_longitude,
            order_datetime,
            pickup_datetime,
            pickup_delay,
            delivery_time,
            sla_status,
            category,
            area,
            area_clean,
            vehicle,
            weather,
            weather_group,
            traffic,
            distance_km,
            distance_bucket,
            on_time_flag
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        # Build rows in same order as insert_query fields above
        rows = []
        for _, row in df.iterrows():
            tup = (
                row.get("Order_ID"),
                row.get("Agent_Age"),
                row.get("Agent_Rating"),
                row.get("Store_Latitude"),
                row.get("Store_Longitude"),
                row.get("Drop_Latitude"),
                row.get("Drop_Longitude"),
                row.get("order_datetime"),
                row.get("pickup_datetime"),
                row.get("pickup_delay"),
                row.get("Delivery_Time"),
                row.get("sla_status"),
                row.get("Category"),
                row.get("Area"),
                row.get("area_clean"),
                row.get("Vehicle"),
                row.get("Weather"),
                row.get("weather_group"),
                row.get("Traffic"),
                row.get("distance_km"),
                row.get("distance_bucket"),
                row.get("on_time_flag"),
            )
            rows.append(tup)

        # Sanity check: placeholders vs tuple length
        if rows:
            print("Insert query placeholders:", insert_query.count("%s"))
            print("First tuple length:", len(rows[0]))

        # Execute in batches for performance
        if rows:
            execute_batch(cur, insert_query, rows, page_size=batch_size)
            conn.commit()
            print(f"Inserted {len(rows)} rows into deliveries table.")
        else:
            print("No rows to insert.")

    except Exception as e:
        # rollback if error and re-raise
        if conn:
            conn.rollback()
        print("Error while loading to Postgres:", str(e))
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# If run directly for quick manual test (not recommended for production)
if __name__ == "__main__":
    import sys
    try:
        df = pd.read_csv("data/amazon_delivery.csv")
    except FileNotFoundError:
        print("data/amazon_delivery.csv not found. Place dataset at data/amazon_delivery.csv or call load_to_postgres() directly.")
        sys.exit(1)

    # Example: if you already transformed, load transformed df instead.
    print("Read CSV rows:", len(df))
    print("Please call load_to_postgres(df_transformed) from your run_pipeline or interactive session.")
