from time import perf_counter
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from huggingface_hub import snapshot_download
import torch

MODELO_ID = "rhaymison/t5-portuguese-small-summarization"
LIMITE_TOKENS_ENTRADA = 512
PROMPT_RESUMO = "sumarize: {texto}"
ARQUIVOS_NECESSARIOS = [
    "config.json",
    "generation_config.json",
    "model.safetensors",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
]


def carregar_modelo_local():
    inicio = perf_counter()
    caminho_modelo = snapshot_download(
        repo_id=MODELO_ID, allow_patterns=ARQUIVOS_NECESSARIOS, local_files_only=True
    )

    tokenizador = AutoTokenizer.from_pretrained(caminho_modelo, local_files_only=True)

    modelo = AutoModelForSeq2SeqLM.from_pretrained(
        caminho_modelo, local_files_only=True
    )

    modelo.eval()
    tempo_carga = perf_counter() - inicio

    return tokenizador, modelo, tempo_carga


def gerar_resumo(texto, tokenizador, modelo):
    texto_limpo = texto.strip()
    if not texto_limpo:
        raise ValueError("O texto fornecido não pode estar vazio.")
    texto_preparado = PROMPT_RESUMO.format(texto=texto_limpo)
    tokens_completos = tokenizador(
        texto_preparado,
        add_special_tokens=True,
        truncation=False,
        return_attention_mask=False,
        verbose=False,
    )["input_ids"]
    entrada = tokenizador(
        texto_preparado,
        max_length=LIMITE_TOKENS_ENTRADA,
        truncation=True,
        return_tensors="pt",
    )
    quantidade_tokens_entrada = len(tokens_completos)
    quantidade_tokens_processados = entrada["input_ids"].shape[1]

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
        "modelo": MODELO_ID,
        "resumo": resumo,
        "tokens_entrada": quantidade_tokens_entrada,
        "tokens_processados": quantidade_tokens_processados,
        "texto_truncado": (quantidade_tokens_entrada > quantidade_tokens_processados),
        "tempo_inferencia_segundos": round(tempo_inferencia, 2),
    }
