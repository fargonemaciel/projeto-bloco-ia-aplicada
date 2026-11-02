import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests

from wordcloud import WordCloud
from src.api_client import buscar_noticias_api
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

CAMINHO_NOTICIAS = RAIZ_PROJETO / "data" / "processed" / "noticias_pobreza.csv"


@st.cache_data(ttl=3600)
def carregar_noticias():
    resposta_api = buscar_noticias_api()

    return pd.DataFrame(resposta_api["noticias"])


@st.cache_data(ttl=3600)
def carregar_noticias_csv():
    return pd.read_csv(CAMINHO_NOTICIAS)


st.header("Notícias relacionadas à pobreza")

st.write(
    """
Publicações coletadas da Agência Brasil para complementar a análise
dos indicadores oficiais.
    """
)


erro_api = None
origem_dados = "API FastAPI do projeto"

try:
    df_noticias = carregar_noticias()
except requests.RequestException as erro:
    erro_api = erro
    if CAMINHO_NOTICIAS.exists():
        df_noticias = carregar_noticias_csv()
        origem_dados = "Arquivo CSV local de contingência"
    else:
        df_noticias = None

if df_noticias is not None:
    if erro_api is not None:
        st.warning(
            """A API está temporariamente indisponível. Os dados foram carregados do arquivo CSV de contingência."""
        )
    st.caption(f"Origem dos dados: {origem_dados}")

    coluna_total, coluna_editorias = st.columns(2)
    coluna_total.metric("Publicações coletadas", len(df_noticias))
    coluna_editorias.metric("Editorias encontradas", df_noticias["editoria"].nunique())

    editorias_disponiveis = sorted(df_noticias["editoria"].unique().tolist())

    editoria_selecionada = st.selectbox(
        "Filtrar notícias por editoria", options=["Todas"] + editorias_disponiveis
    )

    if editoria_selecionada == "Todas":
        noticias_filtradas = df_noticias.copy()
    else:
        noticias_filtradas = df_noticias[
            df_noticias["editoria"] == editoria_selecionada
        ].copy()

    st.dataframe(
        noticias_filtradas[["titulo", "editoria", "data_publicacao", "fonte", "link"]],
        hide_index=True,
    )

    st.subheader("Palavras-chave mais frequentes")
    titulos_noticias = noticias_filtradas["titulo"].dropna().astype(str)

    texto_noticias = " ".join(titulos_noticias)

    palavras_excluidas = {
        "a",
        "ao",
        "aos",
        "as",
        "com",
        "como",
        "da",
        "das",
        "de",
        "do",
        "dos",
        "e",
        "em",
        "entre",
        "é",
        "mais",
        "na",
        "nas",
        "no",
        "nos",
        "o",
        "os",
        "para",
        "por",
        "que",
        "se",
        "um",
        "uma",
    }

    if texto_noticias.strip():
        nuvem_palavras = WordCloud(
            width=1200,
            height=500,
            background_color="white",
            stopwords=palavras_excluidas,
            collocations=False,
        ).generate(texto_noticias)

        figura, eixo = plt.subplots(figsize=(12, 5))
        eixo.imshow(nuvem_palavras, interpolation="bilinear")
        eixo.axis("off")
        st.pyplot(figura)
        plt.close(figura)

    else:
        st.info("""Não existem títulos disponíveis para gerar a nuvem de palavras""")

else:
    st.error("Não foi possível carregar as notícias da API.")

    st.caption(f"Detalhes técnicos: {erro_api}")
