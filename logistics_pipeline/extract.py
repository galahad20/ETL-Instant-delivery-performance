import pandas as pd
from pathlib import Path

def extract_data():
    data_path = Path("data/amazon_delivery.csv")
    df = pd.read_csv(data_path)
    print("Loaded rows:", len(df))
    
    return df

if __name__ == "__main__":
    extract_data()
