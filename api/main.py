from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="API do Painel de Pobreza - ODS 1",
    description=(
        """
        API para consulta dos dados utilizados no Painel de
        priorização territorial de combate à pobreza.
        """
    ),
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def raiz():
    return {"mensagem": "API do Painel de Pobreza - ODS 1", "status": "online"}
