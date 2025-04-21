import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json

# Carregar variáveis do .env
load_dotenv()

# Pega as variáveis do .env
BASE_URL = os.getenv("API_BASE_URL")
PARAMETROS = os.getenv("PARAMETROS")

caminho_base = os.path.dirname(__file__)
caminho_json = os.path.join(caminho_base, "cidades", "cidades.json")

with open(caminho_json, "r") as f:
    cidades = json.load(f)

def coletar_dados_clima(LAT, LON, CIDADE):
    # Monta a URL completa
    url = f"{BASE_URL}?latitude={LAT}&longitude={LON}&hourly={PARAMETROS}"

    print(f"📡 Requisição para: {url}")
    resposta = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        dados = resposta.json()

        # Extrai os dados da resposta
        timestamps = dados['hourly']['time']
        valores = dados['hourly'][PARAMETROS.split(",")[0]]

        df = pd.DataFrame({
            "datetime": timestamps,
            "valor": valores
        })

        # Salva o resultado em Parquet
        caminho_arquivo = f"data/raw/{CIDADE}_clima.parquet"
        df.to_parquet(caminho_arquivo, index=False)
        print(f"✅ Arquivo salvo em: {caminho_arquivo}")

    else:
        print("❌ Erro na requisição:", resposta.status_code)


def executar_coleta_multipla():
    for nome_cidade, coordenadas in cidades.items():
        lat = coordenadas["lat"]
        lon = coordenadas["lon"]
        coletar_dados_clima(lat, lon, nome_cidade)


# Executa se rodar direto (não como módulo)
if __name__ == "__main__":
    executar_coleta_multipla()
