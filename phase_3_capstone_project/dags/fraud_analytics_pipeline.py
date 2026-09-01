from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from datetime import datetime


def check_fraud_transactions(**context):

    result = context["ti"].xcom_pull(task_ids="fraud_count")

    count = result[0][0]

    if count > 0:
        return "send_email_alert"
    return None


with DAG(
    dag_id="fraud_analytics_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="""
            cd /opt/airflow/snowflake_etl

            dbt run \
                --project-dir /opt/airflow/snowflake_etl \
                --profiles-dir /home/airflow/.dbt
        """,
    )

    fraud_count = SQLExecuteQueryOperator(
        task_id="fraud_count",
        conn_id="snowflake_default",
        sql="""
            SELECT COUNT(*)
            FROM DBT_DB.DBT_DEV.fraud_alerts
            WHERE suspicious_transaction = TRUE;
        """,
    )

    check_fraud = BranchPythonOperator(
        task_id="check_fraud",
        python_callable=check_fraud_transactions,
    )

    send_email_alert = EmailOperator(
        task_id="send_email_alert",
        to="xxxxxx@gmail.com",
        subject="🚨 Fraud Alert",
        html_content="""
            <h3>Fraud Alert Triggered</h3>
            <p>Suspicious transactions have been detected.</p>
            <p>Please check the fraud_alerts table in Snowflake.</p>
        """,
        retries=3,
    )

    run_dbt >> fraud_count >> check_fraud >> send_email_alert
