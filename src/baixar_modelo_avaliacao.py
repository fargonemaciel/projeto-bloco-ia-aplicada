from time import perf_counter
from huggingface_hub import snapshot_download

# MODELO = "rhaymison/t5-portuguese-small-summarization"
MODELO = "recogna-nlp/ptt5-base-summ-xlsum"

# ARQUIVOS_NECESSARIOS = ["*,json", "*.safetensors", "*,model", "*.txt", "tokenizer*"]
ARQUIVOS_NECESSARIOS = [
    "config.json",
    "model.safetensors",
    "special_tokens_map.json",
    "spiece.model",
    "tokenizer_config.json",
]


def baixar_modelo():
    print(f"Baixando o modelo {MODELO}...")

    inicio = perf_counter()
    # pasta_modelo = snapshot_download(repo_id=MODELO)
    caminho_modelo = snapshot_download(
        repo_id=MODELO, allow_patterns=ARQUIVOS_NECESSARIOS
    )

    tempo_total = perf_counter() - inicio

    print(f"Modelo disponível em: {caminho_modelo}")
    print(f"Tempo do download ou verificação: {tempo_total:.2f} segundos")
    return caminho_modelo


if __name__ == "__main__":
    baixar_modelo()
