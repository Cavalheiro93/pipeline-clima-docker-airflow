from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Garante que o Airflow encontre o módulo src/processamento
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from processamento.tratamento import tratar_dados_climaticos


# Define a DAG
with DAG(   
    dag_id="dag_trata_dados_climaticos",
    start_date=datetime(2024, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["clima", "api", "airflow"]
) as dag:

    tarefa_coleta = PythonOperator(
        task_id="tratar_dados_clima",
        python_callable=tratar_dados_climaticos
    )