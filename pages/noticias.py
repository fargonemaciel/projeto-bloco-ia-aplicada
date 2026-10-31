import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent


@st.cache_data(ttl=3600)
def carregar_noticias(caminho_arquivo):
    return pd.read_csv(caminho_arquivo)


st.header("Notícias relacionadas à pobreza")

st.write(
    """
Publicações coletadas da Agência Brasil para complementar a análise
dos indicadores oficiais.
    """
)

caminho_noticias = RAIZ_PROJETO / "data" / "processed" / "noticias_pobreza.csv"

if caminho_noticias.exists():
    df_noticias = carregar_noticias(caminho_noticias)

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
    st.warning("O arquivo de notícias não foi encontrado.")
