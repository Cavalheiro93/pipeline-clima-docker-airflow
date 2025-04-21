from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

with DAG(
    dag_id="pipeline_completo_clima_v2",
    start_date=datetime(2025, 4, 1),
    schedule_interval="*/5 * * * *",  # ou None, se quiser só manual
    catchup=False,
    tags=["clima", "encadeado", "pipeline"]
) as dag:

    trigger_coleta = TriggerDagRunOperator(
        task_id="disparar_dag_coleta",
        trigger_dag_id="deprecated_pipeline_coleta_clima"
    )

    trigger_tratamento = TriggerDagRunOperator(
        task_id="disparar_dag_tratamento",
        trigger_dag_id="deprecated_tratamennto_dados_climaticos"
    )

    trigger_transformacao = TriggerDagRunOperator(
        task_id="disparar_dag_transformacao",
        trigger_dag_id="deprecated_dag_transformacao_dados_climaticos"
    )

    trigger_coleta >> trigger_tratamento >> trigger_transformacao
