import streamlit as st

st.set_page_config(
    page_title="Painel da Pobreza - ODS 1", page_icon="💹", layout="wide"
)

pagina_inicio = st.Page("pages/inicio.py", title="Início", icon="🏠", default=True)

pagina_ia = st.Page("pages/preparacao_ia.py", title="Resumo com IA", icon="🤖")

pagina_indicadores = st.Page("pages/indicadores.py", title="Indicadores", icon="📊")

pagina_noticias = st.Page("pages/noticias.py", title="Notícias", icon="📰")

paginas = {
    "Projeto": [pagina_inicio, pagina_ia],
    "Análises": [pagina_indicadores, pagina_noticias],
}

navegacao = st.navigation(paginas)
navegacao.run()
