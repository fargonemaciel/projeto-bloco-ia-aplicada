import requests

def carregar_dados():
    try:

        url_estados = (
            "https://servicodados.ibge.gov.br/"
            "api/v1/localidades/estados"
        )

        resposta_estados = requests.get(
            url_estados,
            params={"orderBy": "nome"},
            timeout=20
            )
        resposta_estados.raise_for_status()
        estados = resposta_estados.json()

        estados_por_id = {}
        for estado in estados:
            id_uf = int(estado["id"])
            estados_por_id[id_uf] = {
                "UF": estado["sigla"],
                "Unidade da Federação": estado["nome"],
                "Região": estado["regiao"]["nome"]
            }

        url_pobreza = (
            "https://servicodados.ibge.gov.br/"
        "api/v3/agregados/5817/periodos/-1/variaveis/9617"
        )

        resposta_pobreza = requests.get(
            url_pobreza,
            params={"localidades": "N3[all]"},
            timeout=20
        )
        resposta_pobreza.raise_for_status()
        pobreza = resposta_pobreza.json()

        series = pobreza[0]["resultados"][0]["series"]
        dados = []

        for serie in series:
            id_uf = int(serie["localidade"]["id"])
            periodo = list(serie["serie"].keys())[0]
            valor = list(serie["serie"].values())[0]
            linha = dict(estados_por_id[id_uf])
            linha["Período"] = int(periodo)
            linha["Proporção (%)"] = float(valor)
            dados.append(linha)

        return dados, "API do IBGE (ao vivo)"

    except Exception as erro:
        print(f"Erro ao carregar dados: {erro}")
        return [], "API do IBGE indisponível"

# if __name__ == "__main__":
#     dados, fonte = carregar_dados()
#     print(f"Fonte dos dados: {fonte}")
#     print("Dados carregados:")
#     for linha in dados:
#         print(linha)