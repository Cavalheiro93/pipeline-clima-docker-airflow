from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time

def tarefa_longa():
    time.sleep(180)  # Tempo de execução maior que o SLA
    print("Tarefa em andamento!")
    time.sleep(180)  # Tempo de execução maior que o SLA
    print("Tarefa concluida!")

with DAG(
    dag_id="dag_sla_exemplo",
    start_date=datetime(2025, 4, 1),
    schedule_interval="* * * * *",  # Executa a cada minuto (ideal para teste)
    catchup=False,
    default_args={
        "email_on_failure": True,
        "email_on_retry": True,
        "email": ["caio.cavalheiro@hotmail.com"],  # Mesmo que não envie de fato, precisa estar configurado para logar SLA Miss
    },
    tags=["sla", "teste"]
) as dag:

    tarefa = PythonOperator(
        task_id="tarefa_com_sla",
        python_callable=tarefa_longa,
        sla=timedelta(seconds=5)  # SLA bem curto para forçar o atraso
    )
