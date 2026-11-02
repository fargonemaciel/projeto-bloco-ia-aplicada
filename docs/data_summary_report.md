# Data Summary Report

## Objetivo do documento
Este documento apresenta o primeiro levantamento das fontes de dados que serão utilizadas no Painel de Priorização Territorial de Combate à Pobreza, indicando o tipo dos dados e o objetivo de uso de cada fonte.

## Fonte dos dados

| Fonte | Forma de acesso | Tipo de dado | Objetivo de uso |
|---|---|---|---|
| [SIDRA — Tabela 5817: Indicador 1.1.1](https://sidra.ibge.gov.br/tabela/5817) | API de Dados Agregados do IBGE | Semiestruturado — JSON | Obter a proporção da população abaixo da linha internacional de pobreza por Unidade da Federação e período |
| [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome) | API REST | Semiestruturado — JSON | Obter código, sigla, nome do estado e região geográfica |
| [Agência Brasil — Notícias sobre pobreza](https://agenciabrasil.ebc.com.br/tags/pobreza-0) | Extração de conteúdo web com BeautifulSoup | Semiestruturado — HTML | Obter notícias e textos relacionados à pobreza para contextualização dos indicadores e preparação para uso futuro com LLMs |
| `data/processed/noticias_pobreza.csv` | Arquivo local | Estruturado — CSV | Armazenar título, editoria, data, fonte, link, texto e quantidade de palavras das notícias coletadas |
| `data/sample/dados_complementares_exemplo.csv` | Arquivo local | Estruturado — CSV | Apresentar um exemplo de arquivo com informações complementares por UF |

## Informações utilizadas
A base principal dos dados é a [Tabela 5817 — SIDRA/IBGE](https://sidra.ibge.gov.br/tabela/5817), que apresenta a proporção da população abaixo da linha internacional de pobreza por Unidade da Federação e período.
- sigla da Unidade da Federação;
- nome da Unidade da Federação;
- região;
- período;
- proporção da população abaixo da linha internacional de pobreza.

A base de notícias é obtida da [Agência Brasil](https://agenciabrasil.ebc.com.br/tags/pobreza-0), que apresenta publicações relacionadas à pobreza.
- titulo;
- editoria;
- data de publicação;
- fonte;
- link;
- texto da notícia;
- quantidade de palavras;

Os dados complementares são armazenados em um arquivo CSV separado, que contém informações adicionais sobre os dados, como:
- sigla da UF;
- observação;
- fonte complementar.

**Estrutura esperada:** uf, estado, regiao, periodo, proporacao_pobreza

## Preparação dos dados
Os dados obtidos pelas APIs do IBGE são convertidos para uma estrutura tabular e organizados por Unidade da Federação. Durante a preparação, são selecionados as colunas necessárias, os valores do indicador são convertidos para o tipo numérico e os dados territoriais são associados aos indicadores por meio da sigla da UF.

As notícias são extraídas separadamente com BeautifulSoup e armazenadas em um arquivo CSV antes de serem utilizadas no painel. Além dos dados
exibidos na interface, o processo acessa cada notícia para coletar seu texto e calcular a quantidade de palavras, preparando uma base textual
para as funcionalidades com LLMs.

Os dados complementares enviados pelo usuário são associados aos indicadores pela sigla da UF.

## Verificações de qualidade
- Validade das respostas das fontes externas;
- Identificação do período mais recente disponível;
- Presença das 27 Unidades da Federação na base de dados;
- Identificação de valores ausentes ou duplicados;
- Conversão dos indicadores para valores numéricos;
- Verificação das colunas obrigatórias nos arquivos enviados pelo usuário;
- Verificação da presença de texto nas notícias coletadas;
- Contagem de palavras dos conteúdos extraídos;
- Verificação da disponibilidade do arquivo processado pela API.

## Limitações 
O indicador utilizado representa uma medida monetária da pobreza e não contempla todas as dimensões desse fenômeno social.

A análise possui abrangência estadual e não apresenta dados em nível municipal. As notícias têm caráter complementar e não substituem os indicadores oficiais do IBGE. Além disso a disponibilidade das informações depende do funcionamento das fontes externas utilizadas.

## Disponibilização pela API
Os dados processados são disponibilizados pela API FastAPI do projeto. A rota "/indicadores" fornece os indicadores de pobreza e aceita filtro
opcional por região. A rota "/noticias" fornece os dados coletados da Agência Brasil. A página de notícias do Streamlit consulta a API em vez de abrir 
diretamente o arquivo CSV.

## Preparação para LLM
A coluna "texto" poderá ser utilizada para geração de resumos, perguntas e respostas e identificação de termos recorrentes.

## Decisão sobre Selenium
O uso de Selenium foi avaliado e considerado desnecessário, pois os indicadores estão disponíveis por API criado no projeto e as notícias
puderam ser obtidas por HTML estático com BeautifulSoup.