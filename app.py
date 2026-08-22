import streamlit as st

from pathlib import Path
from src.data_access import carregar_dados

st.set_page_config(
    page_title="Painel da Pobreza - ODS 1",
    page_icon="💹",
    layout="wide"
)

coluna_imagem, coluna_titulo = st.columns([1, 5])
with coluna_imagem:
    caminho_imagem = Path(__file__).parent / "docs" / "ods-01.png"
    st.image(
        str(caminho_imagem),
        caption="ODS 1 - Erradicação da Pobreza",
        width=120
    )

with coluna_titulo:
    st.title("Painel de Priorização Territorial de Combate à Pobreza")
    st.write(
    """
    Aplicação desenvolvida para apoioar a compração dos indicadores de pobreza das Unidade da Federação do Brasil.
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

dados, fonte = carregar_dados()
st.caption(
    f"""
    Fonte: {fonte} - Indicador 1.1.1 - Proporção da população abaixo da linha internacional de pobreza, por Unidade da Federação (em %)
    """
)

if dados:
    cinco_maiores = sorted(
        dados,
        key=lambda linha: linha["Proporção (%)"],
        reverse=True,
    )[:5]

    st.subheader("Cinco estados com maior proporção de pobreza")
    st.dataframe(
        cinco_maiores,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("Não foi possível carregar os dados da API do IBGE")

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