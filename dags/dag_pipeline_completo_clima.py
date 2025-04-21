"""
Pipeline Completo de Coleta, Tratamento e Consolidação de Dados Climáticos

Esta DAG integra todo o fluxo de ETL:
1. Agendamento da DAG
1. Dispara a DAG de coleta (`dag_coleta_clima`)
2. Aguarda todos os arquivos da pasta `raw/` estarem disponíveis
3. Dispara a DAG de tratamento (`dag_trata_dados_climaticos`)
4. Aguarda todos os arquivos na pasta `processed/`
5. Dispara a DAG de consolidação (`dag_consolida_dados_climaticos`)

Autor: Caio Cavalheiro
Data de Criação: 20/04/2025
"""

from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.python import PythonSensor
from datetime import datetime, timedelta
import os

# 🔍 Verifica se todos os arquivos .parquet estão na pasta RAW
def verificar_arquivos_raw():
    caminho = "/opt/airflow/data/raw"
    arquivos_esperados = {
        "sao_paulo_clima.parquet",
        "salvador_clima.parquet",
        "rio_de_janeiro_clima.parquet",
        "sao_bernardo_clima.parquet"
    }
    return arquivos_esperados.issubset(set(os.listdir(caminho)))

# 🔍 Verifica se todos os arquivos .parquet estão na pasta PROCESSED
def verificar_arquivos_processed():
    caminho = "/opt/airflow/data/processed"
    arquivos_esperados = {
        "sao_paulo_clima.parquet",
        "salvador_clima.parquet",
        "rio_de_janeiro_clima.parquet",
        "sao_bernardo_clima.parquet"
    }
    return arquivos_esperados.issubset(set(os.listdir(caminho)))



# ⚙️ Configurações adicionais: Retry e controle de falhas
default_args = {
    "retries": 3,                                # Tenta executar até 3 vezes em caso de falha
    "retry_delay": timedelta(minutes=2),         # Intervalo de 2 minutos entre as tentativas
    "email_on_failure": False,                   # Não envia e-mail em falhas
    "email_on_retry": False                      # Não envia e-mail em retries
}


#1. 🎯 Definição da DAG principal
with DAG(
    default_args=default_args,
    dag_id="pipeline_completo_clima",
    start_date=datetime(2025, 4, 1),
    schedule_interval="*/5 * * * *",  # Executa a cada 5 minutos
    catchup=False,
    tags=["clima", "encadeado", "pipeline"]
) as dag:

    #2. 🚀 Dispara a DAG de coleta
    trigger_coleta = TriggerDagRunOperator(
        task_id="disparar_dag_coleta",
        sla=timedelta(minutes=5),
        trigger_dag_id="dag_coleta_clima"
    )

    #3. 🕵️ Sensor: aguarda todos os arquivos na pasta RAW
    aguardar_raw = PythonSensor(
        task_id="aguardar_todos_arquivos_raw",
        python_callable=verificar_arquivos_raw,
        poke_interval=10,
        timeout=300,
        mode="poke"
    )

    #4. 🚀 Dispara a DAG de tratamento
    trigger_tratamento = TriggerDagRunOperator(
        task_id="disparar_dag_tratamento",
        sla=timedelta(minutes=5),
        trigger_dag_id="dag_trata_dados_climaticos"
    )

    #5. 🕵️ Sensor: aguarda todos os arquivos na pasta PROCESSED
    aguardar_processed = PythonSensor(
        task_id="aguardar_todos_arquivos_processed",
        python_callable=verificar_arquivos_processed,
        poke_interval=10,
        timeout=300,
        mode="poke"
    )

    #6. 🚀 Dispara a DAG de consolidação
    trigger_consolidacao = TriggerDagRunOperator(
        task_id="disparar_dag_consolidacao",
        sla=timedelta(minutes=5),
        trigger_dag_id="dag_consolida_dados_climaticos"
    )

    #7. ➕ Encadeamento do pipeline
    trigger_coleta >> aguardar_raw >> trigger_tratamento >> aguardar_processed >> trigger_consolidacao
