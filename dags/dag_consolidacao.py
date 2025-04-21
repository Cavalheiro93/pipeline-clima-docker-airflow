from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Garante que o Airflow encontre o módulo src/processamento
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from processamento.consolidacao import consolidar_dados_clima

# Definição da DAG
default_args = {
    'owner': 'Caio',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='dag_consolida_dados_climaticos',
    default_args=default_args,
    description='Consolida os dados climáticos processados',
    start_date=datetime(2024, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=['clima', 'consolidacao']
) as dag:
    
    task_transformar_dados = PythonOperator(
        task_id='consolidar_dados_climaticos',
        python_callable=consolidar_dados_clima,
    )