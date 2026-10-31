import streamlit as st

from pathlib import Path

RAIZ_PROJETO = Path(__file__).parent.parent

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
