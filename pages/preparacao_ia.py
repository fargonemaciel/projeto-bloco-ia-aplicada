from pathlib import Path

import pandas as pd
import streamlit as st

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

CAMINHO_NOTICIAS = RAIZ_PROJETO / "data" / "processed" / "noticias_pobreza.csv"


@st.cache_data(ttl=3600)
def carregar_base_textual():
    return pd.read_csv(CAMINHO_NOTICIAS)


st.title("Preparação para Inteligência Artificial")
st.write(
    """
    Esta etapa apresenta nossa coleta de dados para utilização futura com 
    os modelos de liguagem (LLM).
    """
)

st.info(
    """
    Nenhuma LLM está sendo executada, apenas a coleta de dados e a preparação do dataset para uso futuro.
    """
)

st.divider()

st.subheader("Situação da base textual")

if CAMINHO_NOTICIAS.exists():
    df_noticias = carregar_base_textual()

    textos_validos = df_noticias[df_noticias["texto"].fillna("").str.strip() != ""]

    total_palavras = int(df_noticias["quantidade_palavras"].fillna(0).sum())

    coluna_noticias, coluna_textos, coluna_palavras = st.columns(3)

    coluna_noticias.metric("Notícias coletadas", len(df_noticias))
    coluna_textos.metric("Textos disponíveis", len(textos_validos))
    coluna_palavras.metric("Palavras coletadas", total_palavras)

else:
    st.warning("A base textual de notícias ainda não foi encontrada.")

st.divider()

st.subheader("Caso de uso prioritário")

st.markdown(
    """
    **Resumo fundamentado de notícias sobre pobreza**

    A funcionalidade receberá o texto de uma notícia e
    produzirá uma síntese objetiva, destacando:

    - tema principal;
    - dados e números relevantes;
    - localidade ou população mencionada;
    - relação com o ODS 1;
    - limitações do conteúdo;
    - fonte utilizada.
    """
)

st.subheader("Possíveis evoluções")

st.markdown(
    """
    - Perguntas e respostas baseadas nas notícias coletadas;
    - identificação de temas recorrentes;
    - apoio à elaboração de relatórios descritivos.
    """
)

st.divider()

st.subheader("Estrutura planejada do prompt")
st.code(
    """
Papel:
Você é um assistente de análise social especializado no ODS 1.

Contexto:
A aplicação apresenta indicadores oficiais de pobreza e notícias
coletadas de fontes identificadas.

Tarefa:
Produza um resumo objetivo da notícia fornecida.

Dados:
{texto_da_noticia}

Formato esperado:
- Síntese
- Dados principais
- Relação com o ODS 1
- Limitações
- Fonte

Regras:
- Utilize somente as informações presentes no texto.
- Não invente números, locais ou conclusões.
- Informe quando o texto não trouxer dados suficientes.
- Preserve a referência da fonte original.
    """,
    language="text",
)
