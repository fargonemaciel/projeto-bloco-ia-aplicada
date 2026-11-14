from pathlib import Path
from time import perf_counter
import pandas as pd
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import snapshot_download

CAMINHO_NOTICIAS = (
    Path(__file__).resolve().parents[1] / "data" / "processed" / "noticias_pobreza.csv"
)

# MODELO = "rhaymison/t5-portuguese-small-summarization"
MODELO = "recogna-nlp/ptt5-base-summ-xlsum"

ARQUIVOS_NECESSARIOS = [
    "config.json",
    "model.safetensors",
    "special_tokens_map.json",
    "spiece.model",
    "tokenizer_config.json",
]

LIMITE_TOKENS_ENTRADA = 512


def carregar_primeira_noticia():
    df_noticias = pd.read_csv(CAMINHO_NOTICIAS)

    noticias_com_texto = df_noticias.dropna(subset=["texto"]).copy()

    noticias_com_texto = noticias_com_texto[
        noticias_com_texto["texto"].str.strip() != ""
    ]

    if noticias_com_texto.empty:
        raise ValueError("Nenhuma notícias com texto foi encontrada.")

    return noticias_com_texto.iloc[0]


def carregar_modelo():
    inicio = perf_counter()
    caminho_modelo = snapshot_download(
        repo_id=MODELO, allow_patterns=ARQUIVOS_NECESSARIOS, local_files_only=True
    )
    print(f"Modelo disponível em: {caminho_modelo}")
    tokenizador = AutoTokenizer.from_pretrained(caminho_modelo, local_files_only=True)
    modelo = AutoModelForSeq2SeqLM.from_pretrained(
        caminho_modelo, local_files_only=True
    )
    modelo.eval()
    tempo_carga = perf_counter() - inicio
    return tokenizador, modelo, tempo_carga


def gerar_resumo(texto, tokenizador, modelo):
    # texto_preparado = f"sumarize: {texto}"
    texto_preparado = texto
    tokens_sem_corte = tokenizador.encode(
        texto_preparado, add_special_tokens=True, truncation=False
    )
    entrada = tokenizador(
        texto_preparado,
        max_length=LIMITE_TOKENS_ENTRADA,
        truncation=True,
        return_tensors="pt",
    )
    quantidade_tokens_original = len(tokens_sem_corte)
    quantidade_tokens_utilizados = entrada["input_ids"].shape[1]

    inicio = perf_counter()

    with torch.inference_mode():
        saida = modelo.generate(
            **entrada,
            max_new_tokens=120,
            min_new_tokens=30,
            num_beams=4,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    tempo_inferencia = perf_counter() - inicio
    resumo = tokenizador.decode(saida[0], skip_special_tokens=True)
    return {
        "resumo": resumo,
        "quantidade_tokens_original": quantidade_tokens_original,
        "quantidade_tokens_utilizados": quantidade_tokens_utilizados,
        "texto_truncado": (quantidade_tokens_original > quantidade_tokens_utilizados),
        "tempo_inferencia": tempo_inferencia,
    }


if __name__ == "__main__":
    noticia = carregar_primeira_noticia()
    texto = noticia["texto"]

    print("Título:", noticia["titulo"])
    print("Quantidade de caracteres:", len(texto))
    print("Quantidade aproximada de palavras:", len(texto.split()))
    # print("Trecho inicial:")
    # print(texto[:500])

    tokenizador, modelo, tempo_carga = carregar_modelo()
    print(f"Modelo carregado em: {tempo_carga:.2f} segundos")
    resultado = gerar_resumo(texto, tokenizador, modelo)
    print("Resumo:", resultado["resumo"])
    print("Tokens do texto completo:", resultado["quantidade_tokens_original"])
    print("Tokens enviados ao modelo:", resultado["quantidade_tokens_utilizados"])
    print("Texto truncado:", resultado["texto_truncado"])
    print(f"Tempo de inferência: {resultado['tempo_inferencia']:.2f} segundos")
