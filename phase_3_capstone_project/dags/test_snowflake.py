from airflow.sdk import dag, task
from datetime import datetime
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


@dag(
    dag_id="test_snowflake",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
)
def test_snowflake():

    @task
    def test_connection():
        hook = SnowflakeHook(snowflake_conn_id="snowflake_default")

        result = hook.get_first(
            "SELECT CURRENT_USER(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
        )

        print(f"Snowflake connection successful: {result}")

    test_connection()


test_snowflake()