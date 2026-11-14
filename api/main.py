from fastapi import FastAPI
from api.routes import router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.tokenizador_llm = None
    app.state.modelo_llm = None
    app.state.funcao_resumo = None
    app.state.tempo_carga_llm = None
    app.state.erro_llm = None

    try:
        from src.resumidor_llm import carregar_modelo_local, gerar_resumo

        tokenizador, modelo, tempo_carga = carregar_modelo_local()
        app.state.tokenizador_llm = tokenizador
        app.state.modelo_llm = modelo
        app.state.funcao_resumo = gerar_resumo
        app.state.tempo_carga_llm = tempo_carga

        print("Modelo carregado localmente com sucesso em", tempo_carga, "segundos.")
    except Exception as erro:
        app.state.erro_llm = str(erro)
        print("Modelo LLM indisponível:", str(erro))

    yield
    app.state.tokenizador_llm = None
    app.state.modelo_llm = None
    app.state.funcao_resumo = None


app = FastAPI(
    title="API do Painel de Pobreza - ODS 1",
    description=(
        """
        API para consulta dos dados utilizados no Painel de
        priorização territorial de combate à pobreza.
        """
    ),
    version="1.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
async def raiz():
    return {"mensagem": "API do Painel de Pobreza - ODS 1", "status": "online"}
