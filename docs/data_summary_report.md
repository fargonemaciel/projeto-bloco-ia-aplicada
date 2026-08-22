# Data Summary Report

## Objetivo do documento
Este documento apresenta o primeiro levantamento das fontes de dados que serão utilizadas no Painel de Priorização Territorial de Combate à Pobreza, indicando o tipo dos dados e o objetivo de uso de cada fonte.

## Fonte dos dados
## Fontes de dados

| Fonte | Forma de acesso | Tipo de dado | Objetivo de uso |
|---|---|---|---|
| [SIDRA — Tabela 5817: Indicador 1.1.1](https://sidra.ibge.gov.br/tabela/5817) | API de Dados Agregados do IBGE | Semiestruturado — JSON | Obter a proporção da população abaixo da linha internacional de pobreza por Unidade da Federação e período |
| [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome) | API REST | Semiestruturado — JSON | Obter código, sigla, nome do estado e região geográfica |
| `data/sample/amostra_pobreza.csv` | Arquivo local | Estruturado — CSV | Apresentar uma amostra dos dados na aplicação demo e servir como alternativa temporária quando a API estiver indisponível |

## Informações esperadas
- Código da Unidade da Federação;
- Sigla da Unidade da Federação;
- Nome do Estado;
- Região;
- Períodos;
- Proporção da população abaixo da linha internacional de pobreza;
- Unidade de medida do indicador;

**Estrutura esperada:** uf, estado, regiao, periodo, proporacao_pobreza

## Transformação prevista
Os dados consumidos via API em formato JSON serão transformados em lista de dicionários. E durante a preparação dos dados, escolheremos as colunas pretendidas, além de converção dos valores para o tipos corretos, com a devida organização por UFs.

## Verificações iniciais de qualidade
- Confirmação de resposta válida de API;
- Verificação de qual o período mais recente disponível;
- Verificação da existência de registros duplicados;
- Identificação de valores ausentes ou indisponíveis;
- Conversão dos valores para tipo numéricos;
- Checagem da presença das 27 Unidades da Federação na base dados.

## Limitações iniciais
O indicador representa uma medida monetária da pobreza e não contempla todas as dimensões possíveis sobre o referido fenômeno social. Além disso, a primeira versão neste TP só terá abrangência estadual, não descendo o nível até município.