import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

URL_BUSCA = "https://agenciabrasil.ebc.com.br/tags/pobreza-0"

CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/155.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def coletar_texto_noticia(url):
    resposta_noticia = requests.get(url, headers=CABECALHOS, timeout=30)
    resposta_noticia.raise_for_status()
    pagina_noticia = BeautifulSoup(resposta_noticia.text, "html.parser")
    elemento_conteudo = pagina_noticia.select_one("div.conteudo-noticia")
    if elemento_conteudo is None:
        return ""
    paragrafos = elemento_conteudo.select("p")
    texto = " ".join(paragrafo.get_text(strip=True) for paragrafo in paragrafos)
    return texto


resposta = requests.get(URL_BUSCA, headers=CABECALHOS, timeout=30)
print("Status da requisição:", resposta.status_code)

resposta.raise_for_status()

pagina = BeautifulSoup(resposta.text, "html.parser")

bloco_noticias = pagina.select("div.ultima-noticia")

print("Quantidade de notícias encontradas:", len(bloco_noticias))

if not bloco_noticias:
    raise ValueError("Nenhuma notícia encontrada")

noticias_coletadas = []

for bloco in bloco_noticias:
    elemento_titulo = bloco.select_one("a.titulo-noticia")
    elemento_editoria = bloco.select_one("a.editoria")
    elemento_data = bloco.select_one("span.data")

    if elemento_titulo is None or elemento_editoria is None or elemento_data is None:
        continue

    link_relativo = elemento_titulo.get("href")
    if not link_relativo:
        continue

    link_noticia = urljoin(URL_BUSCA, link_relativo)
    try:
        texto_noticia = coletar_texto_noticia(link_noticia)
    except requests.RequestException as erro:
        print(f"Erro ao coletar o conteúdo da notícia: {erro}")
        texto_noticia = ""
    time.sleep(1)

    noticia = {
        "titulo": elemento_titulo.get_text(strip=True),
        "editoria": elemento_editoria.get_text(strip=True),
        "data_publicacao": elemento_data.get_text(strip=True),
        "fonte": "Agencia Brasil",
        "link": link_noticia,
        "texto": texto_noticia,
        "quantidade_palavras": len(texto_noticia.split()),
    }

    noticias_coletadas.append(noticia)

print("Quantidade de notícias coletadas:", len(noticias_coletadas))
print("Três primeiras notícias coletadas:")
for noticia in noticias_coletadas[:3]:
    print(
        {
            "titulo": noticia["titulo"],
            "quantidade_palavras": noticia["quantidade_palavras"],
            "link": noticia["link"],
        }
    )

if not noticias_coletadas:
    raise ValueError("Nenhuma notícia encontrada")

df_noticias = pd.DataFrame(noticias_coletadas)
pasta_dados = Path("data") / "processed"
pasta_dados.mkdir(parents=True, exist_ok=True)

caminho_arquivo = pasta_dados / "noticias_pobreza.csv"

df_noticias.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")
print(f"Arquivo de notícias salvo em {caminho_arquivo}")
print("Arquivo CSV gerado com sucesso")
print("Forma do arquivo:", df_noticias.shape)
