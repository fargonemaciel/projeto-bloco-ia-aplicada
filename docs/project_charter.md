# Project Charter

## 1. Identificação do Projeto

**Nome:** Painel de Priorização Territorial de Combate à Pobreza
**Responsável:** Fargone Maciel Flor
**Metodologia:** TDSP - The Data Science Project
**ODS relacionado:** ODS 1 - Erradicação da Pobreza

## 2. Contexto e problema de negócio
Organizações sociais e gestores públicos precisam identificar quais Unidades da Federação devem receber análise prioritária no planejamento de ações de enfrentamento à pobreza. Entretanto, os dados oficiais nem sempre são apresentados de maneira simples, comparável e adequada à tomada de decisão, dificultando a identificação dos territórios com maior proporção de pessoas vivendo abaixo da linha internacional de pobreza.

A aplicação proposta será um dashboard interativo desenvolvido em Python com Streamlit, utilizando dados oficiais do Instituto Brasileiro de Geografia e Estatística (IBGE). O painel permitirá comparar as 27 Unidades da Federação, visualizar os indicadores disponíveis e identificar os territórios que necessitam de análise prioritária.

> Pergunta de negócio que orienta o projeto é: Quais unidades da federação apresentam as maiores proporções de população abaixo da linha internacional de pobreza e devem receber análise prioritária para o planejamento de ações sociais?

A aplicação possui caráter descritivo e atua como instrumento de apoio à decisão. O painel não determina automaticamente onde os recursos deverão ser aplicados, pois essa decisão também depende de outros fatores sociais, econômicos e institucionais.

## 3.Objetivo Geral
Desenvolver um dashboard interativo em Python com Streamlit que organize e apresente dados oficiais de pobreza das 27 Unidades da Federação, permitindo comparar os territórios e identificar aqueles que necessitam de análise prioritária.

## 4. Objetivos Específicos
- Coletar dados oficiais disponibilizados pelo IBGE;
- Organizar os dados das 27 Unidades da Federação;
- Apresentar o período mais recente disponibilizado pela fonte oficial;
- Identificar as cinco Unidades da Federação com os maiores valores do indicador;
- Permitir a comparação e filtragem dos dados por Região;
- Coletar conteúdo relacionado à pobreza por meio de web scraping;
- Armazenar os dados coletados da web em arquivo CSV;
- Apresentar notícias, estatísticas e nuvem de palavras;
- Utilizar cache para reduzir carregamentos repetidos;
- Utilizar estado de sessão para preservar dados durante as interações;
- Permitir upload de informações complementares em CSV;
- Integrar as informações complementares aos indicadores pela Sigla da UF;
- Permitir download do resultado consolidado em CSV;
- Disponibilizar a aplicação por meio de repositório Git e prepará-la para deploy.

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

## 5.2.Não Escopo
- Análise municipal;
- Identificação das causas da pobreza;
- Previsão de valores futuros;

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
- Indisponibilidade da API na consulta inicial; (**Mitigação:** utilizar amostra local como fallback)
- Mudança na estrutura do JSON; (**Mitigação:** separar o código de acesso aos dados, do código da aplicação)
- Valores ausentes ou indisponíveis; (**Mitigação:** verificar a limitação dos dados)
- Cobertura inferior às 27 UFs; (**Mitigação:** reavaliar fonte ou escopo do projeto)

## 11. Restrições e limitações
- A análise está limitada ao nível estadual;
- O indicador utilizado representa uma dimensão monetária da pobreza;
- O projeto não analisa todas as dimensões sociais relacionadas à pobreza;