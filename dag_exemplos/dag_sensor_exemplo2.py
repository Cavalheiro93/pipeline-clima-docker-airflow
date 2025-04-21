from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# Função que será executada depois do sensor
def processar_dados():
    print("✅ Arquivo encontrado. Podemos seguir o fluxo!")

# Função usada pelo PythonSensor
def todos_arquivos_presentes():
    base_path = "/opt/airflow/data/processed"
    arquivos_esperados = [
        "sao_paulo_clima.parquet",
        "salvador_clima.parquet",
        "rio_de_janeiro_clima.parquet",
        "sao_bernardo_clima.parquet"
    ]
    return all(os.path.exists(os.path.join(base_path, nome)) for nome in arquivos_esperados)

# BLOCO PRINCIPAL DA DAG
with DAG(
    dag_id="dag_sensor_todos_arquivos",
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["sensor", "python"]
) as dag:

    esperar_todos = PythonSensor(
        task_id="esperar_todos_os_arquivos",
        python_callable=todos_arquivos_presentes,
        poke_interval=10,
        timeout=300,
        mode="poke"
    )
    
    executar_proxima_etapa = PythonOperator(
        task_id="processar",
        python_callable=processar_dados
    )

    esperar_todos >> executar_proxima_etapa
