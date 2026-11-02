from pathlib import Path
from src.data_access import carregar_dados

import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parent.parent

CAMINHO_SAIDA = RAIZ_PROJETO / "data" / "processed" / "indicadores_pobreza.csv"


def main():
    dados, fonte = carregar_dados()

    if not dados:
        raise RuntimeError("Não foi possível obter os indicadores do IBGE.")
    if fonte != "API do IBGE (ao vivo)":
        raise RuntimeError(
            "O snapshot só pode ser atualizado com dados obtidos ao vivo"
        )

    df_indicadores = pd.DataFrame(dados)

    colunas = ["UF", "Unidade da Federação", "Região", "Período", "Proporção (%)"]

    df_indicadores = df_indicadores[colunas]

    CAMINHO_SAIDA.parent.mkdir(parents=True, exist_ok=True)

    df_indicadores.to_csv(CAMINHO_SAIDA, index=False, encoding="utf-8-sig")

    print("Fonte:", fonte)
    print("Registros:", len(df_indicadores))
    print("Períodos:", sorted(df_indicadores["Período"].unique()))
    print("Arquivo de saída:", CAMINHO_SAIDA)


if __name__ == "__main__":
    main()
