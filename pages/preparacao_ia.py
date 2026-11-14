from pathlib import Path

import pandas as pd
import streamlit as st
import requests
from src.api_client import processar_texto_api

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

CAMINHO_NOTICIAS = RAIZ_PROJETO / "data" / "processed" / "noticias_pobreza.csv"


@st.cache_data(ttl=3600)
def carregar_base_textual():
    return pd.read_csv(CAMINHO_NOTICIAS)


st.title("Resumo de notícias com Inteligência Artificial")
st.write(
    """
    Selecione uma notícia sobre pobreza e gere um resumo utilizando
    um modelo de lingaugem executado localmente pela API FastAPI.
    """
)

st.info(
    """
    O resumo é produzido automaticamente por Inteligência Artificial.
    Confira sempre o conteúdo original antes de utilizar as informações.
    """
)

if not CAMINHO_NOTICIAS.exists():
    st.warning("A base textual de notícias ainda não foi encontrada.")
    st.stop()
st.divider()

df_noticias = carregar_base_textual()

if "texto" not in df_noticias.columns:
    st.warning("A coluna 'texto' não foi encontrada na base textual de notícias.")
    st.stop()

textos_validos = df_noticias[df_noticias["texto"].fillna("").str.strip() != ""].copy()
textos_validos = textos_validos.reset_index(drop=True)

total_palavras = int(df_noticias["quantidade_palavras"].fillna(0).sum())

st.subheader("Situação da base textual")

coluna_noticias, coluna_textos, coluna_palavras = st.columns(3)

coluna_noticias.metric("Notícias coletadas", len(df_noticias))
coluna_textos.metric("Textos disponíveis", len(textos_validos))
coluna_palavras.metric("Palavras coletadas", total_palavras)

if textos_validos.empty:
    st.warning("Não há textos válidos disponíveis na base textual de notícias.")
    st.stop()

st.divider()

st.subheader("Selecionar notícia")

indice_noticia = st.selectbox(
    "Notícia",
    options=textos_validos.index,
    format_func=lambda indice: textos_validos.loc[indice, "titulo"],
)

noticia_selecionada = textos_validos.loc[indice_noticia]

st.caption(
    f"Fonte: {noticia_selecionada['fonte']} | "
    f"Data: {noticia_selecionada['data_publicacao']}"
)

with st.expander("Visualizar texto original"):
    st.write(noticia_selecionada["texto"])

if "resultado_resumo" not in st.session_state:
    st.session_state.resultado_resumo = None

if "indice_noticia_resumida" not in st.session_state:
    st.session_state.indice_noticia_resumida = None

if st.button(
    "Gerar resumo com IA",
    type="primary",
):
    st.session_state.resultado_resumo = None
    st.session_state.indice_noticia_resumida = None

    with st.spinner("Gerando resumo no modelo local..."):
        try:
            resultado = processar_texto_api(noticia_selecionada["texto"])

        except requests.exceptions.HTTPError as erro:
            resposta = erro.response
            status = resposta.status_code if resposta else None

            if status == 503:
                st.warning(
                    """
                    O modelo local está indisponível. Para utilizar
                    esta funcionalidade, execute a API local com o
                    modelo previamente baixado.
                    """
                )
            else:
                detalhe = (
                    resposta.json().get("detail") if resposta is not None else str(erro)
                )

                st.error(f"A API não conseguiu processar o texto: {detalhe}")

        except requests.exceptions.ConnectionError:
            st.error(
                """
                Não foi possível conectar à API. Verifique se o
                FastAPI está sendo executado em
                http://127.0.0.1:8000.
                """
            )

        except requests.exceptions.Timeout:
            st.error("A API ultrapassou o tempo limite de processamento.")

        except requests.exceptions.RequestException as erro:
            st.error(f"Erro de comunicação com a API: {erro}")

        else:
            st.session_state.resultado_resumo = resultado
            st.session_state.indice_noticia_resumida = indice_noticia

resultado = st.session_state.resultado_resumo

if resultado is not None and st.session_state.indice_noticia_resumida == indice_noticia:
    st.divider()
    st.subheader("Resumo gerado")

    st.write(resultado["resumo"])

    coluna_caracteres, coluna_tokens, coluna_tempo = st.columns(3)

    coluna_caracteres.metric(
        "Caracteres recebidos",
        resultado["caracteres_entrada"],
    )

    coluna_tokens.metric(
        "Tokens processados",
        resultado["tokens_processados"],
    )

    coluna_tempo.metric(
        "Tempo de inferência",
        f"{resultado['tempo_inferencia_segundos']:.2f} s",
    )

    if resultado["texto_truncado"]:
        st.warning(
            """
            O texto ultrapassou o limite do modelo. O resumo foi
            produzido com os primeiros 512 tokens.
            """
        )

    st.caption(f"Modelo: {resultado['modelo']} | Execução: {resultado['execucao']}")

    link_noticia = noticia_selecionada.get("link", "")

    if link_noticia:
        st.link_button(
            "Acessar notícia original",
            link_noticia,
        )

st.divider()

st.subheader("Possíveis evoluções")

st.markdown(
    """
    - comparação de resumos de diferentes notícias;
    - perguntas e respostas baseadas na base textual;
    - identificação de temas recorrentes;
    - geração assistida de relatórios descritivos.
    """
)
