from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
import random

# Task 1: envia a cidade usando XCom
def escolher_cidade(ti):
    cidade = Variable.get("cidade_alvo")
    ti.xcom_push(key="cidade_selecionada", value=cidade)

# Task 2: recebe a cidade via XCom
def exibir_cidade(ti):
    cidade = ti.xcom_pull(key="cidade_selecionada", task_ids="escolher_cidade")
    print(f"📍 Cidade recebida via XCom: {cidade}")

with DAG(
    dag_id="dag_xcom_exemplo",
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["xcom"]
) as dag:

    escolher = PythonOperator(
        task_id="escolher_cidade",
        python_callable=escolher_cidade
    )

    exibir = PythonOperator(
        task_id="exibir_cidade",
        python_callable=exibir_cidade
    )

    escolher >> exibir
