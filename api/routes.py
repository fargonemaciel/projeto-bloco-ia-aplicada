import pandas as pd

from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from src.data_access import carregar_dados
from api.models import ResumoResposta, TextoParaResumo

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


@router.post(
    "/processar_texto", response_model=ResumoResposta, tags=["Inteligência Artificial"]
)
def processar_texto(dados: TextoParaResumo, request: Request):
    tokenizador = getattr(request.app.state, "tokenizador_llm", None)
    modelo = getattr(request.app.state, "modelo_llm", None)
    funcao_resumo = getattr(request.app.state, "funcao_resumo", None)

    if tokenizador is None or modelo is None or funcao_resumo is None:
        raise HTTPException(
            status_code=503,
            detail="O modelo de linguagem local está indisponível Verifique se ele foi carregado corretamente.",
        )
    try:
        resultado = funcao_resumo(dados.texto, tokenizador, modelo)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro
    except Exception as erro:
        print(f"Erro durante a geração do resumo: {erro}")
        raise HTTPException(
            status_code=500,
            detail=("Ocorreu um erro interno durante a geração do resumo."),
        ) from erro

    return ResumoResposta(
        modelo=resultado["modelo"],
        resumo=resultado["resumo"],
        caracteres_entrada=len(dados.texto),
        tokens_entrada=resultado["tokens_entrada"],
        tokens_processados=resultado["tokens_processados"],
        texto_truncado=resultado["texto_truncado"],
        tempo_inferencia_segundos=resultado["tempo_inferencia_segundos"],
    )
