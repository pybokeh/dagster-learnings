from pipelines.my_pipeline import main_pipeline
from schedules.my_schedule import fetch_csv_from_url
from dagster import repository

@repository
def my_repo():
    return {
        "pipelines": {
            "main_pipeline": lambda: main_pipeline
        },
        "schedules": {
            "fetch_csv_from_url": lambda: fetch_csv_from_url
        }
    }