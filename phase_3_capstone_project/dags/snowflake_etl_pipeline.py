from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime
from airflow.decorators import task


with DAG(
    dag_id="q2_snowflake_etl",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
) as dag:

    transform_coffee_sales = SQLExecuteQueryOperator(
        task_id="transform_coffee_sales",
        conn_id="snowflake_default",
        sql="""
            CREATE OR REPLACE TABLE DBT_DB.DBT_DEV.total_coffee_sales AS

            WITH source AS (

                SELECT
                    date AS transaction_date,
                    datetime AS transaction_datetime,
                    cash_type AS payment_type,
                    card AS card_identifier,
                    money AS amount,
                    coffee_name AS coffee_name
                FROM DBT_DB.DBT_DEV_RAW.coffee_sales

            ),

            transformed AS (

                SELECT
                    transaction_date,
                    payment_type,
                    coffee_name,
                    COUNT(*) AS transaction_count,
                    SUM(amount) AS total_sales,
                    AVG(amount) AS average_transaction_amount
                FROM source
                GROUP BY
                    transaction_date,
                    payment_type,
                    coffee_name

            )

            SELECT *
            FROM transformed;
        """,
    )

    row_count_report = SQLExecuteQueryOperator(
        task_id="row_count_report",
        conn_id="snowflake_default",
        sql="""
            SELECT COUNT(*) AS row_count
            FROM DBT_DB.DBT_DEV.total_coffee_sales;
        """,
    )

    @task
    def print_row_count(**context):
        result = context["ti"].xcom_pull(task_ids="row_count_report")
        print(f"Row count: {result}")

    transform_coffee_sales >> row_count_report >> print_row_count()