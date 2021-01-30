from dagster import schedule 

@schedule(
    cron_schedule="*/5 * * * 1-5",
    pipeline_name="main_pipeline",
    execution_timezone="US/Eastern"
)
def fetch_csv_from_url(_):
    return {}