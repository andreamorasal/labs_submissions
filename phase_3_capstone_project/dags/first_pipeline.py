from airflow.sdk import dag, task
from datetime import datetime
import time


@dag(
    dag_id="first_pipeline",
    schedule="0 8 * * *",
    start_date=datetime(2026, 9, 1),
    catchup=False,
)
def first_pipeline():

    @task
    def pipeline_started():
        print("Data Pipeline Started")

    @task
    def wait_10_seconds():
        time.sleep(10)

    @task
    def pipeline_completed():
        print("Data Pipeline Completed")

    started = pipeline_started()
    wait = wait_10_seconds()
    completed = pipeline_completed()

    started >> wait >> completed


first_pipeline()