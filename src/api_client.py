import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def buscar_noticias_api():
    resposta = requests.get(f"{API_BASE_URL}/noticias", timeout=15)

    resposta.raise_for_status()
    return resposta.json()
