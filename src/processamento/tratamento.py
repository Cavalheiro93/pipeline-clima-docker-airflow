import os
import pandas as pd
from dotenv import load_dotenv
import time

def tratar_dados_climaticos():
    # Carregar variáveis do .env    
    load_dotenv()
    # Pega as variáveis do .env
    BASE_URL = os.getenv("API_BASE_URL")
    PARAMETROS = os.getenv("PARAMETROS")

    # Caminho da pasta com os dados brutos
    CAMINHO_RAW = os.path.join("data", "raw")


    # Lista os arquivos .parquet dentro da pasta
    arquivos_parquet = [
        arquivo for arquivo in os.listdir(CAMINHO_RAW)
        if arquivo.endswith(".parquet")
    ]

    # Exibe os arquivos encontrados
    print("Arquivos encontrados na camada Bronze:")
    for nome in arquivos_parquet:
        print(f"🔹 {nome}")


    for arquivo in arquivos_parquet:
        # Caminho completo do arquivo
        caminho_arquivo = os.path.join(CAMINHO_RAW, arquivo)

        nome_cidade = arquivo.replace("_clima.parquet", "")

        # Leitura do .parquet
        df = pd.read_parquet(caminho_arquivo)    

        #TRANSFORMAÇÃO DOS DADOS    
        df['cidade'] = nome_cidade
        nome_coluna = PARAMETROS.split(",")[0]
        df.rename(columns={"valor": nome_coluna}, inplace=True)

        # Define o caminho de destino na camada processed
        CAMINHO_PROCESSED = "data/processed"
        os.makedirs(CAMINHO_PROCESSED, exist_ok=True)

        # Caminho de destino final
        caminho_salvar = os.path.join(CAMINHO_PROCESSED, arquivo)

        # Salva o DataFrame em formato .parquet
        df.to_parquet(caminho_salvar, index=False)
        print(f"✅ Arquivo transformado salvo: {caminho_salvar}")



if __name__ == "__main__":
    df_teste = tratar_dados_climaticos()


    

