import pandas as pd
import numpy as np

# ambil SLA threshold yang sudah kamu pakai
SLA_THRESHOLD_MINUTES = 140  # sesuaikan bila mau

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform pipeline untuk Instant Delivery dashboard.
    - Normalize datetime fields
    - Drop rows with missing critical datetimes
    - Hitung distance_km (haversine)
    - Hitung pickup_delay, sla_status
    - Clean area -> area_clean (Metropolitan / Urban / Non-Urban)
    - Group weather -> weather_group (Good / Bad)
    - Create distance_bucket (quantile-based, q=4)
    - Create on_time_flag (0/1)
    Returns transformed DataFrame (ready to load).
    """
    # Work on a safe copy to avoid SettingWithCopyWarning
    df = df.copy()

    # --- 1. Datetime parsing (tolerant)
    if "Order_Date" in df.columns and "Order_Time" in df.columns:
        df.loc[:, "order_datetime"] = pd.to_datetime(
            df["Order_Date"].astype(str) + " " + df["Order_Time"].astype(str),
            errors="coerce"
        )
    else:
        df.loc[:, "order_datetime"] = pd.NaT

    if "Order_Date" in df.columns and "Pickup_Time" in df.columns:
        df.loc[:, "pickup_datetime"] = pd.to_datetime(
            df["Order_Date"].astype(str) + " " + df["Pickup_Time"].astype(str),
            errors="coerce"
        )
    else:
        df.loc[:, "pickup_datetime"] = pd.NaT

    # drop rows missing critical datetimes (and make sure it's a copy)
    before = len(df)
    df = df.dropna(subset=["order_datetime", "pickup_datetime"]).copy()
    after = len(df)
    print(f"Dropped rows missing critical datetimes: {before - after}")

    # --- 2. Distance (haversine)
    def haversine_series(lat1, lon1, lat2, lon2):
        # expects series or array-like (degrees). Handles NaN gracefully.
        lat1_r, lon1_r, lat2_r, lon2_r = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2_r - lat1_r
        dlon = lon2_r - lon1_r
        a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2.0) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371.0  # Earth radius in km
        return c * r

    # Guard against non-numeric lat/lon (use .loc to avoid warnings)
    for col in ["Store_Latitude", "Store_Longitude", "Drop_Latitude", "Drop_Longitude"]:
        if col in df.columns:
            df.loc[:, col] = pd.to_numeric(df[col], errors="coerce")

    df.loc[:, "distance_km"] = haversine_series(
        df.get("Store_Latitude"),
        df.get("Store_Longitude"),
        df.get("Drop_Latitude"),
        df.get("Drop_Longitude"),
    )

    # --- 3. pickup_delay (minutes)
    df.loc[:, "pickup_delay"] = (
        (df["pickup_datetime"] - df["order_datetime"]).dt.total_seconds() / 60.0
    )
    # Fix negative pickup delays (invalid data)
    df["pickup_delay"] = df["pickup_delay"].clip(lower=0)

    # --- 4. sla_status (based on Delivery_Time column)
    if "Delivery_Time" in df.columns:
        df.loc[:, "Delivery_Time"] = pd.to_numeric(df["Delivery_Time"], errors="coerce")
        df.loc[:, "sla_status"] = df["Delivery_Time"].apply(
            lambda x: "late" if pd.notnull(x) and x > SLA_THRESHOLD_MINUTES else "on_time"
        )
    else:
        df.loc[:, "Delivery_Time"] = pd.NA
        df.loc[:, "sla_status"] = pd.NA

    # --- 5. Clean area -> area_clean (robust: case-insensitive column detection)
    area_col = next((c for c in df.columns if c.lower() == "area"), None)
    if area_col:
        # normalize strings, replace en-dash with hyphen, strip whitespace, title-case
        df.loc[:, area_col] = df[area_col].astype(str).str.replace("–", "-", regex=False).str.strip().str.title()
        area_mapping = {
            "Semi-Urban": "Non-Urban",
            "Other": "Non-Urban",
            "Metropolitian": "Metropolitan",  # dataset typo safety
            "Metropolitan": "Metropolitan",
            "Urban": "Urban",
        }
        df.loc[:, "area_clean"] = df[area_col].replace(area_mapping)
    else:
        df.loc[:, "area_clean"] = pd.NA

    # --- 6. Weather grouping -> weather_group (robust)
    weather_col = next((c for c in df.columns if c.lower() == "weather"), None)
    if weather_col:
        df.loc[:, weather_col] = df[weather_col].astype(str).str.strip().str.title()
        good_weather = {"Sunny", "Cloudy"}  # as decided
        df.loc[:, "weather_group"] = df[weather_col].apply(lambda x: "Good" if x in good_weather else "Bad")
    else:
        df.loc[:, "weather_group"] = pd.NA

    # --- 7. Distance bucket (quantile-based)
    labels = ["Near", "Mid-range", "Far", "Very Far"]
    mask = df["distance_km"].notna()
    if mask.any():
        try:
            temp = pd.qcut(df.loc[mask, "distance_km"], q=4, labels=labels, duplicates="drop")
            # assign only for indices that have a bucket (preserve NaN for others)
            df.loc[mask, "distance_bucket"] = temp.astype(object)
        except Exception:
            # fallback to manual binning
            max_val = df["distance_km"].max()
            bins = [0, 5, 10, 15, max_val if pd.notnull(max_val) else 9999]
            df.loc[:, "distance_bucket"] = pd.cut(df["distance_km"], bins=bins, labels=labels, include_lowest=True)
    else:
        df.loc[:, "distance_bucket"] = pd.NA

    # --- 8. helper flags
    df.loc[:, "on_time_flag"] = df["sla_status"].apply(lambda s: 1 if s == "on_time" else 0)

    # Optional: cast some columns to desirable types for DB
    df.loc[:, "distance_km"] = pd.to_numeric(df["distance_km"], errors="coerce")
    # use nullable Int64 for SQL-friendly nullable integer
    df.loc[:, "on_time_flag"] = df["on_time_flag"].astype("Int64")

    # Print sample for quick debugging
    sample_cols = [
        "order_datetime", "pickup_datetime", "pickup_delay", "Delivery_Time", "sla_status",
        "area_clean", "weather_group", "distance_km", "distance_bucket", "on_time_flag"
    ]
    avail = [c for c in sample_cols if c in df.columns]
    print("Sample transformed data:")
    print(df.loc[:, avail].head())

    return df
