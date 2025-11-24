from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="logistique_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="* * * * *",  # every minute
    catchup=False,
):
    
    # Run analytics script
    run_analytics = BashOperator(
        task_id="calculate_stats",
        bash_command="py /mnt/c/Users/anass/Desktop/Briefs/B7_Systeme-Predictif-Intelligent-de-Gestion-Logistique/analytics.py"
    )

    run_analytics
