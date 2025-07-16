from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 28),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'banking_data_quality_dag',
    default_args=default_args,
    description='Run daily data quality and risk checks for banking dataset',
    schedule_interval=None,
    catchup=False
) as dag:

    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='python /opt/airflow/jobs/generate_data.py' 
    )

    data_quality_check = BashOperator(
        task_id='data_quality_check',
        bash_command='python /opt/airflow/jobs/data_quality_standards.py'
    )

    risk_based_check = BashOperator(
        task_id='risk_based_check',
        bash_command='python /opt/airflow/jobs/monitoring_audit.py'  
    )

    generate_data >> data_quality_check >> risk_based_check
