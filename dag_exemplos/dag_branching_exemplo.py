from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

# Função que decide o caminho com base na cidade
def decidir_caminho():
    cidade = "sao_paulo"  # você pode tornar isso dinâmico futuramente
    if cidade == "sao_paulo":
        return "tratar_sao_paulo"
    else:
        return "tratar_outras_cidades"

# Simulações de tratamento
def tratamento_sao_paulo():
    print("🔵 Tratando dados de São Paulo com lógica especial...")

def tratamento_outras():
    print("🟢 Tratando dados de outras cidades normalmente...")

with DAG(
    dag_id='dag_branching_exemplo',
    start_date=datetime(2025, 4, 1),
    schedule_interval=None,
    catchup=False,
    tags=["teste", "branching"],
) as dag:

    inicio = EmptyOperator(task_id="inicio")

    escolha_caminho = BranchPythonOperator(
        task_id="branch_cidade",
        python_callable=decidir_caminho
    )

    tratar_sao_paulo = PythonOperator(
        task_id="tratar_sao_paulo",
        python_callable=tratamento_sao_paulo
    )

    tratar_outras_cidades = PythonOperator(
        task_id="tratar_outras_cidades",
        python_callable=tratamento_outras
    )

    fim = EmptyOperator(
        task_id="fim",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    # Encadeamento
    inicio >> escolha_caminho
    escolha_caminho >> tratar_sao_paulo >> fim
    escolha_caminho >> tratar_outras_cidades >> fim
