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
| [Agência Brasil - Notícias sobre pobreza] | Extração de conteúdo web com BeautifulSoup | Estruturado — HTML | Obter notícias relacionadas à pobreza para complementar a contextualização dos indicadores |
| `data/processed/noticias_pobreza.csv` | Arquivo local | Estruturado — CSV | Armazenar os dados coletados da web em arquivo CSV |
| `data/sample/dados_complementares_example.csv` | Arquivo local | Estruturado — CSV | Apresentar exemplo de arquivo CSV com dados complementares |


## Informações utilizadas
A base principal dos dados é a [Tabela 5817 — SIDRA/IBGE](https://sidra.ibge.gov.br/tabela/5817), que apresenta a proporção da população abaixo da linha internacional de pobreza por Unidade da Federação e período.
- sigla da Unidade da Federação;
- nome da Unidade da Federação;
- região;
- período;
- proporção da população abaixo da linha internacional de pobreza.

A base de notícias é a [Agência Brasil](https://www.ag.gov.br/pt-br/home/noticias/pobreza), que apresenta notícias relacionadas à pobreza.
- titulo;
- editoria;
- data de publicação;
- fonte;
- link.

Os dados complementares são armazenados em um arquivo CSV separado, que contém informações adicionais sobre os dados, como:
- sigla da UF;
- observação;
- fonte complementar.

**Estrutura esperada:** uf, estado, regiao, periodo, proporacao_pobreza

## Preparação dos dados
Os dados obtidos pelas APIs do IBGE são convertidos para uma estrutura tabular e organizados por Unidade da Federação. Durante a preparação, são selecionados as colunas necessárias, os valores do indicador são convertidos para o tipo numérico e os dados territoriais são associados aos indicadores por meio da sigla da UF.

As notícias são extraídas separadamente com BeautifulSoup e armazenadas em um arquivo CSV antes de serem utilizadas no painel.

Os dados complementares enviados pelo usuário são associados aos indicadores pela sigla da UF.

## Verificações de qualidade
- Validade das respostas das fontes externas;
- Identificação do período mais recente disponível;
- Presença das 27 Unidades da Federação na base de dados;
- Identificação de valores ausentes ou duplicados;
- Conversão dos indicadores para valores numéricos;
- Verificação das colunas obrigatórias nos arquivos enviados pelo usuário;

## Limitações 
O indicador utilizado representa uma medida monetária da pobreza e não contempla todas as dimensões desse fenômeno social.

A análise possui abrangência estadual e não apresenta dados em nível municipal. As notícias têm caráter complementar e não substituem os indicadores oficiais do IBGE. Além disso a disponibilidade das informações depende do funcionamento das fontes externas utilizadas.