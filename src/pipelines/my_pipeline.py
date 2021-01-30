from dagster import pipeline
from solids.my_solids import fetch_csv, transform_name

@pipeline
def main_pipeline():
    df = fetch_csv()
    transform_name(df)
