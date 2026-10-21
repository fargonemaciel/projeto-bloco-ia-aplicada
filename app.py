import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from src.data_access import carregar_dados
from wordcloud import WordCloud


@st.cache_data(ttl=3600)
def carregar_noticias(caminho_arquivo):
    return pd.read_csv(caminho_arquivo)


@st.cache_data(ttl=3600)
def carregar_indicadores():
    return carregar_dados()


if "dados_complementares" not in st.session_state:
    st.session_state["dados_complementares"] = None

st.set_page_config(
    page_title="Painel da Pobreza - ODS 1", page_icon="💹", layout="wide"
)

coluna_imagem, coluna_titulo = st.columns([1, 5])
with coluna_imagem:
    caminho_imagem = Path(__file__).parent / "docs" / "ods-01.png"
    st.image(str(caminho_imagem), caption="ODS 1 - Erradicação da Pobreza", width=120)

with coluna_titulo:
    st.title("Painel de Priorização Territorial de Combate à Pobreza")
    st.write(
        """
    Aplicação desenvolvida para apoiar a comparação dos indicadores de pobreza das Unidades da Federação do Brasil.
    """
    )

st.divider()

coluna_problema, coluna_objetivos = st.columns([1, 1])
with coluna_problema:
    st.markdown("## Problema de negócio")
    st.write(
        """
        Organizações sociais e gestores públicos precisam identificar quais Unidades da Federação apresentam as maiores proporções de população abaixo da
        linha internacional de pobreza e necessitam de análise prioritária para alocação de recursos e políticas públicas.
        """
    )
with coluna_objetivos:
    st.markdown("## Objetivos do projeto")
    st.markdown(
        """
        - Coletar dados oficiais disponibilizados pelo IBGE;
        - Organizar os dados das 27 Unidades da Federação;
        - Apresentar os dados mais recentes disponíveis;
        - Identificar as cinco Unidades da Federação com os maiores valores do indicador;
        - Permitir a comparação e filtragem dos dados por Região;
        """
    )

st.divider()
st.write("")

st.markdown("## Dados de pobreza das Unidades da Federação do Brasil")

dados, fonte = carregar_indicadores()
st.caption(
    f"""
    Fonte: {fonte} - Indicador 1.1.1 - Proporção da população abaixo da linha internacional de pobreza, por Unidade da Federação (em %)
    """
)

if dados:
    df_indicadores = pd.DataFrame(dados)
    regioes_disponiveis = sorted(df_indicadores["Região"].dropna().unique().tolist())

    st.sidebar.header("Filtros dos indicadores")

    regiao_selecionada = st.sidebar.selectbox(
        "Selecione uma região", options=["Todos"] + regioes_disponiveis
    )

    if regiao_selecionada == "Todos":
        indicadores_filtrados = df_indicadores.copy()
    else:
        indicadores_filtrados = df_indicadores[
            df_indicadores["Região"] == regiao_selecionada
        ]

    indicadores_ordenados = indicadores_filtrados.sort_values(
        by="Proporção (%)", ascending=False
    )

    cinco_maiores = indicadores_ordenados.head(5)

    periodos_encontrados = (
        indicadores_ordenados["Período"].dropna().astype(int).unique().tolist()
    )

    if len(periodos_encontrados) == 1:
        periodo_exibido = periodos_encontrados[0]
    else:
        periodo_exibido = "Mais de um período"

    maior_proporcao = indicadores_ordenados.iloc[0]

    coluna_ufs, coluna_periodo, coluna_maior = st.columns(3)
    coluna_ufs.metric("Unidades da Federação", len(indicadores_filtrados))
    coluna_periodo.metric("Período de referência", periodo_exibido)
    coluna_maior.metric("Maior proporção", f"{maior_proporcao['Proporção (%)']:.2f}%")

    st.subheader("Unidades da Federação com maiores proporçõies de pobreza")
    st.write(f"Resultado considerando o filtro de região: **{regiao_selecionada}**.")

    tabela_cinco_maiores = cinco_maiores[
        ["UF", "Unidade da Federação", "Região", "Período", "Proporção (%)"]
    ]

    st.dataframe(tabela_cinco_maiores, hide_index=True)

    st.subheader("Dados complementares por UF")

    st.write("""Envie um arquivo CSV para acrescentar observações e 
    fontes complementares para os indicadores oficiais de pobreza.""")

    with st.form("formulario_upload"):
        arquivo_enviado = st.file_uploader("Selecione um arquivo CSV", type=["csv"])
        confirmar_upload = st.form_submit_button("Carregar dados complementares")

    if confirmar_upload:
        if arquivo_enviado is None:
            st.warning("Selecione um arquivo CSV antes de confirmar.")
        else:
            try:
                dados_enviados = pd.read_csv(arquivo_enviado)
                colunas_obrigatorias = {"UF", "Observação", "Fonte complementar"}
                colunas_ausentes = colunas_obrigatorias - set(dados_enviados.columns)

                if colunas_ausentes:
                    st.error(
                        "O arquivo não contém todas as colunas obrigatórias:"
                        f"{sorted(colunas_ausentes)}"
                    )
                else:
                    st.session_state["dados_complementares"] = dados_enviados.copy()
                    st.success("Dados complementares carregados com sucesso.")

            except (UnicodeDecodeError, pd.errors.ParserError):
                st.error("O arquivo não é um arquivo CSV válido.")

    if st.session_state["dados_complementares"] is not None:
        st.write("Dados mantidos na sessão atual:")
        st.dataframe(st.session_state["dados_complementares"], hide_index=True)
        dados_complementares = st.session_state["dados_complementares"].copy()

        dados_complementares["UF"] = (
            dados_complementares["UF"].astype(str).str.strip().str.upper()
        )

        ufs_validas = set(df_indicadores["UF"].astype(str).str.strip().str.upper())

        ufs_informadas = set(dados_complementares["UF"])

        ufs_invalidas = sorted(ufs_informadas - ufs_validas)
        if ufs_invalidas:
            st.error(f"O arquivo contém siglas de UF inválidas: {ufs_invalidas}")
        elif dados_complementares["UF"].duplicated().any():
            st.error(
                "O arquivo contém UFs duplicadas. Mantenha apenas uma linha por UF."
            )
        else:
            dados_consolidados = indicadores_filtrados.merge(
                dados_complementares, on="UF", how="left", validate="one_to_one"
            )

            st.subheader("Indicadores com dados complementares")
            st.write(
                """A tabela mantém os indicadores oficiais do IBGE e acrescenta as informações
                enviadas pelo usuário."""
            )
            st.dataframe(dados_consolidados, hide_index=True)

            arquivo_download = dados_consolidados.to_csv(index=False).encode(
                "utf-8-sig"
            )

            st.download_button(
                label="Baixar dados consolidados em CSV",
                data=arquivo_download,
                file_name="indicadores_pobreza_complementados.csv",
                mime="text/csv",
            )

else:
    st.error("Não foi possível carregar os dados da API do IBGE")


st.divider()

st.markdown("## Links úteis")
st.markdown(
    """
    - [ODS 1 — Nações Unidas Brasil](https://brasil.un.org/pt-br/sdgs/1)
    - [Tabela 5817 — SIDRA/IBGE](https://sidra.ibge.gov.br/tabela/5817)
    - [API de Dados Agregados do IBGE](https://servicodados.ibge.gov.br/api/docs/agregados)
    - [Conecta Brasil](https://conectabrasil.org/ods)
    - [Observatório do Terceiro Setor](https://observatorio3setor.org.br/ods/ods-01/)
    """
)

st.divider()
st.info(
    """
    Esta é a versão inicial do painel de priorização territorial de combate à pobreza. A aplicação será aprimorada com novas funcionalidades
    nas próximas etapas do projeto
    """
)

st.divider()

st.header("Notícias relacionadas à pobreza")

st.write(
    """
Publicações coletadas da Agência Brasil para complementar a análise
dos indicadores oficiais.
    """
)

caminho_noticias = (
    Path(__file__).parent / "data" / "processed" / "noticias_pobreza.csv"
)

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
