# src/processamento/consolidacao.py

"""
Módulo de Consolidação de Dados Climáticos

Este script contém funções responsáveis por:
✅ Unir os arquivos tratados da camada Processed (Silver)
✅ Consolidar os dados em um único DataFrame
✅ Salvar o resultado na camada Final (Gold), pronto para análises

Funções:
- consolidar_dados_clima(): Unifica os arquivos de múltiplas cidades
"""

import os
import pandas as pd
import glob
from datetime import datetime

def salvar_dados_clima(df_consolidado):
    # 1. Cria a pasta "data/final" se ela não existir
    os.makedirs("data/final", exist_ok=True)

    # 2. Salva o DataFrame consolidado em um arquivo .parquet
    CAMINHO_SAIDA = "data/final/dados_consolidados.parquet"

    # 3. Salva o DataFrame em um arquivo .parquet
    df_consolidado.to_parquet(CAMINHO_SAIDA, index=False)

    # 4. Exibe uma mensagem de sucesso
    print(f"✅ Arquivo salvo com sucesso em: {CAMINHO_SAIDA}")

def consolidar_dados_clima():
    # 1. Busca todos os arquivos .parquet da pasta processed
    caminhos_arquivos = glob.glob("data/processed/*.parquet")
    
    # 2. Lista para armazenar os DataFrames
    lista_df = []

    # 3. Itera e carrega cada arquivo
    for caminho in caminhos_arquivos:
        df = pd.read_parquet(caminho)
        lista_df.append(df)

    # 4. Concatena todos os DataFrames em um só
    df_consolidado = pd.concat(lista_df, ignore_index=True)

#   # 5. Converte a coluna "datetime" para o formato datetime
    df_consolidado["datetime"] = pd.to_datetime(df_consolidado["datetime"])

    # 6. Cria novas colunas com base no datetime
    df_consolidado["ano"] = df_consolidado["datetime"].dt.year
    df_consolidado["mes"] = df_consolidado["datetime"].dt.month
    df_consolidado["inicio_mes"] = df_consolidado["datetime"].dt.to_period("M").dt.to_timestamp()
    df_consolidado["data_ref"] = pd.to_datetime(datetime.now()).floor("min")

    # 7. Chama a função 'salvar_dados_clima' e Salva o DataFrame consolidado
    salvar_dados_clima(df_consolidado) 

    # 8. Retorna o DataFrame consolidado
    return df_consolidado


if __name__ == "__main__":
    df_teste = consolidar_dados_clima()
    print(df_teste)
