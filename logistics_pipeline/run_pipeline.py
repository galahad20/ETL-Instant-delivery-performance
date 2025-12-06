from extract import extract_data
from transform import transform_data
from load import load_to_postgres


def run():
    df_raw = extract_data()
    df_clean = transform_data(df_raw)
    load_to_postgres(df_clean)

if __name__ == "__main__" :
    run()
