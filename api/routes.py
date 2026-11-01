import pandas as pd

from pathlib import Path
from fastapi import APIRouter, HTTPException
from src.data_access import carregar_dados

router = APIRouter()

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

CAMINHO_NOTICIAS = RAIZ_PROJETO / "data" / "processed" / "noticias_pobreza.csv"


@router.get("/noticias", tags=["Notícias"])
def listar_noticias():
    if not CAMINHO_NOTICIAS.exists():
        raise HTTPException(
            status_code=404, detail="Arquivo de notícias não encontrado."
        )
    df_noticias = pd.read_csv(CAMINHO_NOTICIAS)
    df_noticias = df_noticias.fillna("")

    return {
        "total": len(df_noticias),
        "noticias": df_noticias.to_dict(orient="records"),
    }


@router.get("/indicadores", tags=["Indicadores"])
def listar_indicadores(regiao: str | None = None):
    dados, fonte = carregar_dados()

    if not dados:
        raise HTTPException(
            status_code=503, detail="Não foi possível carregar os dados de indicadores."
        )
    if regiao and regiao.strip():
        regiao_normalizada = regiao.strip().casefold()
        indicadores_filtrados = [
            indicador
            for indicador in dados
            if str(indicador.get("Região", "")).casefold() == regiao_normalizada
        ]

        if not indicadores_filtrados:
            raise HTTPException(
                status_code=404,
                detail=f"Não foram encontrados indicadores para a região '{regiao}'.",
            )

        regiao_aplicada = regiao.strip()
    else:
        indicadores_filtrados = dados
        regiao_aplicada = "Todas"

    return {
        "total": len(indicadores_filtrados),
        "regiao": regiao_aplicada,
        "fonte": fonte,
        "indicadores": indicadores_filtrados,
    }
