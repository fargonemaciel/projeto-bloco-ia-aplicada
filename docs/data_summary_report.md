# Data Summary Report

## Objetivo do documento
Este documento apresenta as fontes, a preparação, a qualidade e o uso dos dados integrados ao Painel de Priorização Territorial de Combate à Pobreza, abrangendo indicadores oficiais, notícias coletadas por web scraping e os dados utilizados pelo modelo local de sumarização.

## Fonte dos dados

| Fonte | Forma de acesso | Tipo de dado | Objetivo de uso |
|---|---|---|---|
| [SIDRA — Tabela 5817: Indicador 1.1.1](https://sidra.ibge.gov.br/tabela/5817) | API de Dados Agregados do IBGE | Semiestruturado — JSON | Obter a proporção da população abaixo da linha internacional de pobreza por Unidade da Federação e período |
| [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome) | API REST | Semiestruturado — JSON | Obter código, sigla, nome do estado e região geográfica |
| `data/processed/indicadores_pobreza.csv` | Snapshot local gerado a partir das APIs do IBGE | Estruturado — CSV | Manter os indicadores disponíveis quando as APIs do IBGE estiverem temporariamente inacessíveis |
| [Agência Brasil — Notícias sobre pobreza](https://agenciabrasil.ebc.com.br/tags/pobreza-0) | Extração de conteúdo web com BeautifulSoup | Semiestruturado — HTML | Obter notícias e textos relacionados à pobreza para contextualização dos indicadores e sumarização automática com o modelo local |
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

Quando a consulta ao vivo das APIs do IBGE não está disponível, a aplicação utiliza um snapshot local gerado previamente a partir das mesmas
fontes oficiais. A origem utilizada é identificada na interface.

As notícias são extraídas separadamente com BeautifulSoup e armazenadas em um arquivo CSV antes de serem utilizadas no painel. Além dos dados
exibidos na interface, o processo acessa cada notícia para coletar seu texto e calcular a quantidade de palavras, preparando uma base textual
para as funcionalidades com LLMs.

Os dados complementares enviados pelo usuário são associados aos indicadores pela sigla da UF.

## Dados e resultados derivados
A partir dos dados processados, a aplicação produz:

- total de Unidades da Federação disponíveis;
- período de referência;
- identificação da UF com maior valor do indicador;
- ranking das cinco maiores proporções;
- médias simples dos indicadores estaduais agrupados por região;
- contagem de notícias e textos disponíveis;
- resumos automáticos das notícias selecionadas;
- quantidade de tokens recebidos e processados;
- indicação de truncamento;
- tempo de inferência do modelo local.

Os cálculos territoriais são realizados com pandas e não pela LLM. O modelo de linguagem é utilizado exclusivamente para sumarizar os textos coletados.

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

## Integração no ciclo de Ciência de Dados
Os indicadores do IBGE são utilizados para cálculos, filtros, rankings, métricas e gráficos territoriais. As notícias coletadas da Agência Brasil formam a bse textual utilizada pelo modelo de linguagem.

O fluxo de dados é composto por:
1. coleta por APIs e web scraping;
2. armazenamento dos dados processados em CSV;
3. validação e transformação com Pandas;
4. análise descritiva dos indicadores;
5. sumarização dos textos com o modelo local;
6. disponibilização dos dados e da IA pela API FastAPI;
7. apresentação dos resultados no dashboard Streamlit.

Os indicadores oficiais e os textos jornalísticos permanecem separados. As notícias complementam o contexto, mas não substituem os dados do IBGE.

## Limitações 
O indicador utilizado representa uma medida monetária da pobreza e não contempla todas as dimensões desse fenômeno social.

A análise possui abrangência estadual e não apresenta dados em nível municipal. As notícias têm caráter complementar e não substituem os indicadores oficiais do IBGE. Além disso a disponibilidade das informações depende do funcionamento das fontes externas utilizadas.

O snapshot de contingência pode não refletir uma atualização publicada pelo IBGE após sua última geração. Por isso, sua atualização deve ser realizada de forma controlada por meio do script de coleta.

O modelo de linguagem pode omitir informações, apresentar falhas de escrita ou produzir respostas imprecisas. Por isso, a interface mantém a referência para o conteúdo original e informa quando o texto foi truncado.

As médias apresentadas por região são médias simples dos indicadores das Unidades da Federação. Elas não correspondem a taxas regionais oficiais ponderadas pela população.

## Disponibilização pela API
Os dados processados são disponibilizados pela API FastAPI do projeto. A rota "/indicadores" fornece os indicadores de pobreza e aceita filtro
opcional por região. A rota "/noticias" fornece os dados coletados da Agência Brasil. A página de notícias do Streamlit consulta a API em vez de abrir 
diretamente o arquivo CSV.

A rota `POST /processar_texto` recebe o texto de uma notícia e retorna o resumo gerado pelo modelo local, juntamente com informações sobre tokens, truncamento, tempo de inferência e modelo utilizado.

## Uso da base textual pela LLM

A coluna `texto` é utilizada como entrada para o modelo local de sumarização. O conteúdo selecionado no Streamlit é enviado à rota `POST /processar_texto` da API FastAPI.

O modelo processa até 512 tokens. Quando o texto ultrapassa esse limite, a resposta informa que houve truncamento. O resumo gerado não altera o arquivo original e deve ser conferido com a notícia de origem.

## Decisão sobre Selenium
O uso de Selenium foi avaliado e considerado desnecessário, pois os indicadores estão disponíveis por API criado no projeto e as notícias
puderam ser obtidas por HTML estático com BeautifulSoup.