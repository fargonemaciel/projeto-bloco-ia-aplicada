# Project Charter

## 1. Identificação do Projeto

**Nome:** Painel de Priorização Territorial de Combate à Pobreza
**Responsável:** Fargone Maciel Flor
**Metodologia:** TDSP - Team Data Science Process
**ODS relacionado:** ODS 1 - Erradicação da Pobreza

## 2. Contexto e problema de negócio
Organizações sociais e gestores públicos precisam identificar quais Unidades da Federação devem receber análise prioritária no planejamento de ações de enfrentamento à pobreza. Entretanto, os dados oficiais nem sempre são apresentados de maneira simples, comparável e adequada à tomada de decisão, dificultando a identificação dos territórios com maior proporção de pessoas vivendo abaixo da linha internacional de pobreza.

A aplicação proposta será um dashboard interativo desenvolvido em Python com Streamlit, utilizando dados oficiais do Instituto Brasileiro de Geografia e Estatística (IBGE). O painel permitirá comparar as 27 Unidades da Federação, visualizar os indicadores disponíveis e identificar os territórios que necessitam de análise prioritária.

> Pergunta de negócio que orienta o projeto é: Quais unidades da federação apresentam as maiores proporções de população abaixo da linha internacional de pobreza e devem receber análise prioritária para o planejamento de ações sociais?

A aplicação possui caráter descritivo e atua como instrumento de apoio à decisão. O painel não determina automaticamente onde os recursos deverão ser aplicados, pois essa decisão também depende de outros fatores sociais, econômicos e institucionais.

## 3.Objetivo Geral
Desenvolver um dashboard interativo em Python com Streamlit que organize e apresente dados oficiais de pobreza das 27 Unidades da Federação, permita identificar territórios que necessitam de análise prioritária e utilize um modelo de linguagem local para automatizar a sumarização de notícias relacionadas ao ODS 1.

## 4. Objetivos Específicos
- Coletar dados oficiais disponibilizados pelo IBGE;
- Organizar os dados das 27 Unidades da Federação;
- Apresentar o período mais recente disponibilizado pela fonte oficial;
- Identificar as cinco Unidades da Federação com os maiores valores do indicador;
- Permitir a comparação e filtragem dos dados por Região;
- Coletar conteúdo relacionado à pobreza por meio de web scraping;
- Armazenar os dados coletados da web em arquivo CSV;
- Apresentar notícias, estatísticas e nuvem de palavras;
- Gerar resumos automáticos das notícias coletadas utilizando um modelo de linguagem local;
- Integrar Streamlit, FastAPI e o modelo de sumarização em um único fluxo de interação;
- Apresentar métricas, gráficos e insights derivados dos indicadores oficiais;
- Demonstrar o ciclo completo de Ciência de Dados, desde a coleta até a apresentação dos resultados;
- Relacionar os resultados ao ODS 1 e às dimensões Social e de Governança do ESG;
- Manter a decisão final sob responsabilidade humana, utilizando  aIA apenas como apoio à leitura;
- Utilizar cache para reduzir carregamentos repetidos;
- Utilizar estado de sessão para preservar dados durante as interações;
- Permitir upload de informações complementares em CSV;
- Integrar as informações complementares aos indicadores pela Sigla da UF;
- Permitir download do resultado consolidado em CSV;
- Disponibilizar o código por meio de repositório Git e publicar os componentes compatíveis com execução em nuvem.

## 5.1. Escopo
**Incluído no projeto:**
- Indicador 1.1.1 do ODS 1;
- Dados das 27 Unidades da Federação;
- Análise descritiva dos dados;
- Dados obtidos pela API de Dados Agregados do IBGE;
- Conteúdo complementar coletado da Agência Brasil;
- Web scraping executado separadamente com BeautifulSoup;
- Armazenamento em arquivo CSV;
- Ordenação das UFs pela proporção observada;
- Upload e download de arquivos CSV;
- Dashboard executivo com métricas, gráficos e insights territoriais;
- Modelo local de sumarização em português;
- Rota FastAPI para processamento de texto;
- Seleção de notícia e geração interativa de resumo no Streamlit;
- Exibição de tokens processados, truncamento e tempo de inferência;
- Apresentação do ciclo completo de Ciência de Dados;
- Contextualização da solução no ODS 1 e nas dimensões Social e de Governança do ESG;

## 5.2.Não Escopo
- Análise municipal;
- Identificação das causas da pobreza;
- Previsão de valores futuros;
- Recomendação automática de políticas públicas;
- Substituição da análise humana por decisões geradas pela IA;
- Uso da notícia como substituta dos indicadores oficiais;
- Execução do modelo local no serviço gratuito utilizado para publicar a API.

## 6. Público-alvo
- Gestores de organizações sociais;
- Gestores públicos;
- Fundações e instituições sociais;
- Pesquisadores e estudantes interessados em indicadores de pobreza e desenvolvimento sustentável.

## 7. Stakeholders
- **Responsável pelo projeto:** Fargone Maciel Flor, responsável pelo planejamento, a coleta, a análise dos dados e o desenvolvimento da aplicação;
- **IBGE:** provedor externo dos dados oficiais utilizados no projeto;
- **Agência Brasil:** fonte pública do conteúdo complementar coletado por web scraping;
- **Gestores públicos:** utilizarão as informações como apoio ao planejamento de ações;
- **Analistas e técnicos dos órgãos e fundações:** são os que utilização o dashboard para consulta mais detalhada e de interpretação dos dados.

## 8. Indicadores de sucesso
- Obtenção dos dados das 27 Unidades da Federação;
- Disponibilização visual do período mais recente encontrato na fonte;
- Clareza na demonstração das cinco Unidades da Federação com maoiores valores de pobreza;
- Melhorar a experiência, com cache e estado de sessão, para evitar carregamentos repetidos;
- Parmitir complementação, através de upload de arquivos CSV, de informações adicionais sobre os dados;
- Aplicação versinada e preparada para publicação;

## 9. Principais Entregáveis
- Repositório Git organizado;
- Aplicação interativa em Streamlit;
- Código de acesso às APIs do IBGE;
- Código separado para web scraping;
- Project charter;
- Data Summary Report;
- Arquivo de dependências;
- Aplicação preparada para deploy;

## 10. Riscos
- Indisponibilidade da API do IBGE; (**Mitigação:** utilizar snapshot local dos dados oficiais como fallback)
- Mudança na estrutura do JSON; (**Mitigação:** separar o código de acesso aos dados, do código da aplicação)
- Valores ausentes ou indisponíveis; (**Mitigação:** verificar a limitação dos dados)
- Cobertura inferior às 27 UFs; (**Mitigação:** reavaliar fonte ou escopo do projeto)

## 11. Restrições e limitações
- A análise está limitada ao nível estadual;
- O indicador utilizado representa uma dimensão monetária da pobreza;
- O projeto não analisa todas as dimensões sociais relacionadas à pobreza;

## 12. Atualização do Projeto - TP3
Nesta etapa, a aplicação foi reorganizada em múltiplas páginas, separando a apresentação do projeto, os indicadores, 
as notícias e o planejamento para uso futuro da Inteligência Artificial.

### Funcionalidades incorporados
- Menu de navegação entre múltiplas páginas;
- API própria desenvolvida com FastAPI;
- Rotas para consulta de indicadores e notícias;
- Integração da página de notícias com a API;
- Ampliação da coleta realizada com BeautifulSoup;
- Extração do texto das notícias e da quantidade de palavras;
- Preparação da base textual para uso de LLM;

### Decições técnicas
O Selenium foi avaliado, mas não utilizado porque as fontes que usamos já disponibilizam os dados com HTML estático. Conforme
orientação do TP3, priorizamos o aprimoramento da coleta com BeautifulSoup, evitando a inclusão de automaçao de navegador.

A API foi organizada separadamente da interface. Ela fornece os dados, enquanto a aplicação Streamlit é responsável pela navegação, interação e apresentação das informações.

### Preparação para Inteligência Artificial

O caso de uso prioritário planejado para a próxima etapa é a geração de resumos fundamentadas nas notícias coletadas.
As respostas deversão utilizar apenas o conteúdo fornecido, preservar a referência da fonte, informar quando os dados
forem insuficientes.
Nesta etapa foram preparados os dados e o formato inicial do prompt.

## 13. Atualização do Projeto - TP4
Nesta etapa, a aplicação passou a utilizar um modelo de linguagem executado localmente para gerar resumos das notícias coletadas sobre pobreza.

### Funcionalidades incorporadas
- Modelo de sumarização em português obtido da Hugging Face;
- Execução local com Transformers e PyTorch;
- Rota `POST /processar_texto` no FastAPI;
- Validação da entrada e da resposta com Pydantic;
- Tratamento de erros 422, 500 e 503;
- Integração da funcionalidade com interface Streamlit;
- Exibição do resumo, tempo de inferência, tokens processados e indicação de truncamento.

### Decisão técnica
O modelo `rhaymison/t5-portuguese-small-summarization` foi selecionado após comparação com outro modelo de sumarização em português. A escolha considerou fidelidade dos fatos resumidos, com custo computacional aceitável e possibilidade de execuação local com CPU.

A funcionalidade possui caráter de apoio à leitura. Os resumos automáticos devem ser conferidos com o texto original e não substituem análise humana ou decisão sobre políticas públicas.

## 14. Atualização do Projeto - TP5

Nesta etapa final, foi escolhida a automação de sumarização de textos com LLM. A funcionalidade utiliza os textos das notícias coletadas por web scraping e transforma conteúdos extensos em resumos que apoiam a contextualização dos indicadores oficiais.

### Ciclo de Ciência de Dados

O projeto apresenta o seguinte ciclo:
1. coleta dos indicadores pelas APIs do IBGE;
2. coleta das notícias da Agência Brasil com BeautifulSoup;
3. armazenamento dos dados processados em arquivos CSV;
4. tratameto, validação e organização dos dados com Pandas;
5. análise territorial com métricas, filtros, rankings e gráficos;
6. sumarização dos textos com umm modelo de linguagem local;
7. apresentação dos resultados em dashboard interativo com Streamlit.

### Engenharia de prompt

O modelo escolhido utiliza o prefixo de tarefa: `sumarize: {texto}`

A instrução foi mantida curta porque o modelo T5 foi treinado especificamente para interpretar esse prefixo como uma tarefa de sumarização. Prompts conversacionais longos poderiam consumir o limite de entrada e reduzir a quantidade de texto efetivamente processada.

Além da instrução, o fluxo realiza limpeza da entrada, limitação de tokens, truncamento controlado e configuração dos parâmetros de geração.

### Contribuição para o problema de negócio

Os dados do IBGE sustentam a identificação dos territórios com maiores valores do indicador. As notícias e seus resumos fornecem contexto textual complementar, tornando a leitura dos conteúdos mais rápida.

A IA não calcula os indicadores e não define prioridades automaticamente. A aplicação oferece evidências organizadas para apoiar a interpretação de gestores, pesquisadores e organizações sociais.

### Relação com ODS e ESG

A solução está alinhada aos ODS 1 - Erradicação da Pobreza. No contexto ESG, contribui principalmente com a dimensão Social, ao facilitar o acompanhamento de desigualdades, e com a dimensão de Governança, ao identificar fontes, limitações e critérios utilizados no processamento das informações.

### Resultado final

A aplicação integra coleta, processamento, análise, inteligência artificial e apresentação. O dashboard mantém separadas as funções dos indicadores oficiais, dos textos jornalísticos e do modelo de lingaugem, preservando a rastreabilidade das informações e a responsabilidade humana pela decisão.