from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

# Função que será executada depois do sensor
def processar_dados():
    print("✅ Arquivo encontrado. Podemos seguir o fluxo!")

with DAG(
    dag_id="dag_sensor_exemplo",
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["sensor", "exemplo"]
) as dag:

    esperar_sao_paulo = FileSensor(
        task_id="esperar_sao_paulo",
        filepath="/opt/airflow/data/processed/sao_paulo_clima.parquet",
        poke_interval=10,
        timeout=300
    )

    esperar_salvador = FileSensor(
        task_id="esperar_salvador",
        filepath="/opt/airflow/data/processed/salvador_clima.parquet",
        poke_interval=10,
        timeout=300
    )

    esperar_rio = FileSensor(
        task_id="esperar_rio",
        filepath="/opt/airflow/data/processed/rio_de_janeiro_clima.parquet",
        poke_interval=10,
        timeout=300
    )

    esperar_sao_bernardo = FileSensor(
        task_id="esperar_sao_bernardo",
        filepath="/opt/airflow/data/processed/sao_bernardo_clima.parquet",
        poke_interval=10,
        timeout=300
    )

    executar_proxima_etapa = PythonOperator(
        task_id="processar",
        python_callable=processar_dados
    )

    [esperar_sao_paulo, esperar_salvador, esperar_rio, esperar_sao_bernardo] >> executar_proxima_etapa
