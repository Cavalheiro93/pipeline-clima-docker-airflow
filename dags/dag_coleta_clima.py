from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Adiciona o caminho do src ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


# Importa a função de coleta do seu script
from coleta.coleta_api import coletar_dados_clima
from coleta.coleta_api import executar_coleta_multipla

# Define a DAG
with DAG(   
    dag_id="dag_coleta_clima",
    start_date=datetime(2024, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["clima", "api", "airflow"]
) as dag:

    tarefa_coleta = PythonOperator(
        task_id="coletar_dados_clima",
        python_callable=executar_coleta_multipla
    )