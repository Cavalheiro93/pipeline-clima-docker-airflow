from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Garante que o Airflow encontre o módulo src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Importa as funções
from coleta.coleta_api import executar_coleta_multipla
from processamento.tratamento import tratar_dados_climaticos
from processamento.consolidacao import transformar_dados_clima

# Definição da DAG
default_args = {
    'owner': 'Caio',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='pipeline_completo_clima',
    default_args=default_args,
    description='Pipeline completo: coleta, tratamento e consolidação',
    schedule_interval='*/5 * * * *',  # Roda a cada 5 minutos
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=['clima', 'pipeline', 'encadeado']
) as dag:
    
    coletar_dados = PythonOperator(
        task_id='coletar_dados',
        python_callable=executar_coleta_multipla
    )

    tratar_dados = PythonOperator(
        task_id='tratar_dados',
        python_callable=tratar_dados_climaticos
    )

    consolidar_dados = PythonOperator(
        task_id='consolidar_dados',
        python_callable=transformar_dados_clima
    )

    # Encadeamento das tasks
    coletar_dados >> tratar_dados >> consolidar_dados