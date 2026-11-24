import streamlit as st
import pandas as pd
import altair as alt

from pathlib import Path
from src.data_access import carregar_dados

RAIZ_PROJETO = Path(__file__).parent.parent
CAMINHO_IMAGEM_ODS = RAIZ_PROJETO / "assets" / "ods-01.png"
CAMINHO_NOTICIAS = RAIZ_PROJETO / "data" / "processed" / "noticias_pobreza.csv"


@st.cache_data(ttl=3600)
def carregar_indicadores():
    return carregar_dados()


@st.cache_data(ttl=3600)
def carregar_noticias():
    if not CAMINHO_NOTICIAS.exists():
        return pd.DataFrame()
    return pd.read_csv(CAMINHO_NOTICIAS)


dados_indicadores, fonte_indicadores = carregar_indicadores()
df_indicadores = pd.DataFrame(dados_indicadores)
df_noticias = carregar_noticias()

coluna_imagem, coluna_titulo = st.columns([1, 5])

with coluna_imagem:
    caminho_imagem = RAIZ_PROJETO / "docs" / "ods-01.png"
    st.image(str(caminho_imagem), caption="ODS 1 - Erradicação da Pobreza", width=120)

with coluna_titulo:
    st.title("Painel de Priorização Territorial de Combate à Pobreza - ODS 1")
    st.write(
        """
        Aplicação desenvolvida para apoiar a comparação dos indicadores de pobreza das Unidades da Federação
        do Brasil.
        """
    )

st.divider()

st.subheader("Visão geral do projeto")

if not df_indicadores.empty:
    periodo_referencia = int(df_indicadores["Período"].max())
    indicador_mais_alto = df_indicadores.sort_values(
        "Proporção (%)", ascending=False
    ).iloc[0]
    if not df_noticias.empty:
        textos_disponiveis = int(
            df_noticias["texto"].fillna("").str.strip().ne("").sum()
        )
    else:
        textos_disponiveis = 0
    coluna_ufs, coluna_periodo, coluna_prioridade, coluna_textos = st.columns(4)
    coluna_ufs.metric("Unidade da Federação", df_indicadores["UF"].nunique())
    coluna_periodo.metric("Período de referência", periodo_referencia)
    coluna_prioridade.metric(
        "Maior proporção",
        indicador_mais_alto["UF"],
        f"{indicador_mais_alto['Proporção (%)']:.1f}%",
    )
    coluna_textos.metric("Textos para análise por IA", textos_disponiveis)

    st.caption(f"Fonte dos indicadores: {fonte_indicadores}")

    st.divider()

    st.subheader("Principais resultados territoriais")

    cinco_maiores = (
        df_indicadores.sort_values("Proporção (%)", ascending=False)
        .head(5)
        .sort_values("Proporção (%)", ascending=True)
    )
    media_por_regiao = (
        df_indicadores.groupby("Região", as_index=False)["Proporção (%)"]
        .mean()
        .sort_values("Proporção (%)", ascending=False)
    )
    media_por_regiao["Proporção (%)"] = media_por_regiao["Proporção (%)"].round(2)

    coluna_ranking, coluna_regioes = st.columns(2)
    with coluna_ranking:
        st.markdown("#### Cinco maiores proporções por UF")
        grafico_ufs = (
            alt.Chart(cinco_maiores)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Proporção (%):Q",
                    title="Proporção (%)",
                ),
                y=alt.Y(
                    "UF:N",
                    title="UF",
                    sort="-x",
                ),
                tooltip=[
                    alt.Tooltip("UF:N", title="UF"),
                    alt.Tooltip(
                        "Unidade da Federação:N",
                        title="Estado",
                    ),
                    alt.Tooltip(
                        "Proporção (%):Q",
                        title="Proporção (%)",
                        format=".1f",
                    ),
                ],
            )
            .properties(height=260)
        )
        coluna_ranking.altair_chart(
            grafico_ufs,
            use_container_width=True,
        )
    with coluna_regioes:
        st.markdown("#### Média das proporções por região")
        grafico_regioes = (
            alt.Chart(media_por_regiao)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Região:N",
                    title="Região",
                    sort="-y",
                ),
                y=alt.Y(
                    "Proporção (%):Q",
                    title="Média da proporção (%)",
                ),
                tooltip=[
                    alt.Tooltip("Região:N", title="Região"),
                    alt.Tooltip(
                        "Proporção (%):Q",
                        title="Média simples (%)",
                        format=".2f",
                    ),
                ],
            )
            .properties(height=260)
        )

        coluna_regioes.altair_chart(
            grafico_regioes,
            use_container_width=True,
        )
    st.caption(
        """
        A média regional apresentada é uma média simples dos indicadores das Unidades da Federação
        de cada região. Ela não representa uma taxa regional oficial ponderada pela população.
        """
    )

    st.divider()

    st.subheader("Insights dos indicadores")

    uf_maior_proporcao = df_indicadores.loc[df_indicadores["Proporção (%)"].idxmax()]
    regiao_maior_media = media_por_regiao.iloc[0]
    contagem_regioes_top_cinco = cinco_maiores["Região"].value_counts()
    regiao_mais_presente_top_cinco = contagem_regioes_top_cinco.index[0]
    quantidade_ufs_regiao_top_cinco = int(contagem_regioes_top_cinco.iloc[0])
    media_simples_ufs = df_indicadores["Proporção (%)"].mean()

    st.markdown(
        f"""
        - **Maior valor estadual:**
        {uf_maior_proporcao["Unidade da Federação"]}
        ({uf_maior_proporcao["UF"]}) apresenta o maior valor do indicador,
        com **{uf_maior_proporcao["Proporção (%)"]:.1f}%**.

        - **Maior média simples regional:**
        A região **{regiao_maior_media["Região"]}** apresenta a maior média
        simples entre suas Unidades da Federação, com
        **{regiao_maior_media["Proporção (%)"]:.2f}%**.

        - **Presença entre os cinco maiores valores:**
        A região **{regiao_mais_presente_top_cinco}** possui
        **{quantidade_ufs_regiao_top_cinco} UF(s)** entre os cinco maiores
        valores observados.

        - **Referência comparativa:**
        A média simples dos indicadores das 27 Unidades da Federação é de
        **{media_simples_ufs:.2f}%**.
        """
    )

    st.info(
        """
        Esses resultados apoiam a identificação de territórios que merecem análise prioritária,
        mas não determinam automaticamente a destinação de recursos. A decisão também deve considerar população,
        evolução histórica, infraestrutura, capacidade institucional e outros indicadores sociais.
        """
    )

    st.divider()

    st.subheader("Ciclo de Ciência de Dados aplicado ao projeto")

    coluna_coleta, coluna_preparacao, coluna_analise, coluna_ia, coluna_apresentacao = (
        st.columns(5)
    )
    with coluna_coleta:
        st.markdown("### 1. Coleta")
        st.write(
            """
            APIs do IBGE para indicadores oficiais e web scraping da Agência Brasil para obtenção de notícias sobre pobreza.
            """
        )
    with coluna_preparacao:
        st.markdown("### 2. Preparação")
        st.write(
            """
            Conversão dos dados para estruturas tabulares, tratamento dos tipos,
            verificação das colunas e armazenamento em arquivos CSV.
            """
        )

    with coluna_analise:
        st.markdown("### 3. Análise")
        st.write(
            """
            Comparação territorial, filtros por região, ranking de UFs,
            estatísticas descritivas e identificação dos maiores valores.
            """
        )

    with coluna_ia:
        st.markdown("### 4. Inteligência Artificial")
        st.write(
            """
            Modelo de linguagem executado localmente para produzir resumos automáticos
            dos textos coletados por web scraping.
            """
        )

    with coluna_apresentacao:
        st.markdown("### 5. Apresentação")
        st.write(
            """
            Dashboard interativo com métricas, gráficos, notícias, resumos e informações
            de apoio à análise territorial.
            """
        )

    st.success(
        """
        O projeto integra dados quantitativos oficiais e dados textuais complementares.
        Os indicadores do IBGE sustentam a comparação territorial, enquanto a IA auxilia na
        síntese das notícias, facilitando o acesso ao contexto relacionado à pobreza.
        """
    )

    st.subheader("Contribuição para ODS e ESG")
    st.markdown(
        """
        O projeto está alinhado ao **ODS 1 - Erradicação da Pobreza** ao organizar indicadores que apoiam a identificação
        de territórios com maior necessidade de análise.

        No contexto de **ESG, a aplicação contribui principalmente para a dimensão **social**, pois facilita o acompanhamento
        de desigualdades e indicadores relacionados às condições de vida da população.

        A solução também se relaciona à dimensão de **Governança**, porque utiliza fontes identificadas, mantém rastreabilidade
        dos dados e apresenta limitações metodológicas para apoiar decisões mais transparentes.
        """
    )

else:
    st.warning("Os dados dos indicadores não estão disponíveis para a visão geral.")


st.divider()

coluna_problema, coluna_objetivos = st.columns(2)

with coluna_problema:
    st.subheader("Problema de negócio")
    st.write(
        """
        Organizações sociais e gestores públicos precisam identificar quais Unidades da Federação
        apresentam as maiores proporções de população abaixo da linha internacional de probreza e necessitam de análise prioritária
        para alocação de recursos e políticas públicas.
        """
    )

with coluna_objetivos:
    st.subheader("Objetivos do projeto")
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

st.subheader("Como utilizar a aplicação")
st.markdown(
    """
    Utilize o menu lateral para acessar:

    - **Painel da pobreza:** indicadores oficiais, filtros, ranking,
    upload e download de dados;
    - **Notícias:** conteúdo coletado da web e análise das palavras mais
    frequentes;
    """
)

st.divider()

st.subheader("Fontes e referências")
st.markdown(
    """
    - [ODS 1 — Nações Unidas Brasil](https://brasil.un.org/pt-br/sdgs/1)
    - [Tabela 5817 — SIDRA/IBGE](https://sidra.ibge.gov.br/tabela/5817)
    - [API de Dados Agregados do IBGE](https://servicodados.ibge.gov.br/api/docs/agregados)
    - [Conecta Brasil](https://conectabrasil.org/ods)
    - [Observatório do Terceiro Setor](https://observatorio3setor.org.br/ods/ods-01/)
    """
)

st.info(
    """
    O projeto está sendo desenvolvido incrementalmente e nesta etapa, a aplicação está integrada a uma API própria
    e preparada para funcionalidades futuras de inteligências artificial.
    """
)

st.divider()

st.subheader("Explore a aplicação")

coluna_indicadores, coluna_noticias, coluna_ia = st.columns(3)

with coluna_indicadores:
    st.page_link(
        "pages/indicadores.py",
        label="Consultar indicadores",
        icon="📊",
        use_container_width=True,
    )

with coluna_noticias:
    st.page_link(
        "pages/noticias.py",
        label="Explorar notícias",
        icon="📰",
        use_container_width=True,
    )

with coluna_ia:
    st.page_link(
        "pages/preparacao_ia.py",
        label="Gerar resumo com IA",
        icon="🤖",
        use_container_width=True,
    )
