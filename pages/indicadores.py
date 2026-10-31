import streamlit as st
import pandas as pd

from src.data_access import carregar_dados


@st.cache_data(ttl=3600)
def carregar_indicadores():
    return carregar_dados()


if "dados_complementares" not in st.session_state:
    st.session_state["dados_complementares"] = None

st.title("Indicadores de pobreza")
st.write(
    """
    Consulte, filtre e complemente os indicadores oficiais de pobreza
    das Unidades da Federação do Brasil.
    """
)

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
