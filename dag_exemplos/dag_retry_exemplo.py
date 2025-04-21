from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def tarefa_que_falha():
    raise ValueError("Erro proposital só pra testar o Retry 😅")

with DAG(
    dag_id="dag_retry_exemplo",
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["retry"]
) as dag:

    tarefa = PythonOperator(
        task_id="tarefa_falha",
        python_callable=tarefa_que_falha,
        retries=5,  # Tentar mais 3 vezes
        retry_delay=timedelta(seconds=10)  # Esperar 10s entre cada tentativa
    )
