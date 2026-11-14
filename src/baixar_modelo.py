from time import perf_counter

from huggingface_hub import snapshot_download

from src.resumidor_llm import ARQUIVOS_NECESSARIOS, MODELO_ID


def baixar_modelo():
    print(f"Preparando o modelo local: {MODELO_ID}")

    inicio = perf_counter()

    caminho_modelo = snapshot_download(
        repo_id=MODELO_ID,
        allow_patterns=ARQUIVOS_NECESSARIOS,
    )

    tempo = perf_counter() - inicio

    print(f"Modelo disponível em: {caminho_modelo}")
    print(f"Tempo do download ou verificação: {tempo:.2f} segundos")

    return caminho_modelo


if __name__ == "__main__":
    baixar_modelo()
