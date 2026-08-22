# Project Charter

## Identificação do Projeto

**Nome:** Painel de Priorização Territorial de Combate à Pobreza
**Responsável:** Fargone Maciel Flor
**Metodologia:** TDSP - The Data Science Project

## Contexto e problema
Organizações sociais e gestores públicos precisam identificar quais Unidades da Federação necessitam de análise prioritária no planejamento de ações de enfrentamento à pobreza. Entretanto, os dados oficiais nem sempre são apresentados de maneira simples, comparável e adequado à tomada de decisão.

> Pergunta de negócio: Quais unidades da federação apresentam as maiores proporções de população abaixo da linha internacional de pobreza e devem receber análise prioritária para o planejamento de ações sociais?

## Objetivo Geral
Desenvolver um dashboard interativo em Python com Streamlit que permita comparar as 27 Unidades da Federação e identificar os territórios com os maiores valores do indicador 1.1.1 do ODS 1.

## Objetivos Específicos
- Coletar dados oficiais disponibilizados pelo IBGE;
- Organizar os dados das 27 Unidades da Federação;
- Apresentar os dados mais recentes disponíveis;
- Identificar as cinco Unidades da Federação com os maiores valores do indicador;
- Permitir a comparação e filtragem dos dados por Região;

## Escopo
**Incluído no projeto:**
- Indicador 1.1.1 do ODS 1;
- Dados das 27 Unidades da Federação;
- Análise descritiva dos dados;
- Comparação e ordenação dos dados;
- Aplicação interativa em Streamlit.

## Não Escopo
- Aplicação publicada em núvem;
- Análise municipal;
- Identificação das causas da pobreza;
- Previsão de valores futuros.

## Público-alvo
- Gestores de organizações sociais;
- Gestores públicos;
- Fundações e instituições sociais;

## Stakeholders
- **Responsável pelo projeto:** Fargone Maciel Flor, responsável pelo planejamento, a coleta, a análise dos dados e o desenvolvimento da aplicação;
- **IBGE:** provedor externo dos dados oficiais utilizados no projeto;
- **Gestores públicos:** utilizarão as informações como apoio ao planejamento de ações;
- **Analistas e técnicos dos órgãos e fundações:** são os que utilização o dashboard para consulta mais detalhada e de interpretação dos dados.

## Indicadores de sucesso
- Obtenção dos dados das 27 Unidades da Federação;
- Disponibilização visual do período mais recente encontrato na fonte;
- Clareza na demonstração das cinco Unidades da Federação com maoiores valores de pobreza;

## Principais Entregáveis
- Diretórios organizados;
- Este project charter;
- Data Summary Report;
- Amostra dos dados;
- Códigos de acesso e de aplicação da solução;

## Riscos
- Indisponibilidade da API na consulta inicial; (**Mitigação:** utilizar amostra local como fallback)
- Mudança na estrutura do JSON; (**Mitigação:** separar o código de acesso aos dados, do código da aplicação)
- Valores ausentes ou indisponíveis; (**Mitigação:** verificar a limitação dos dados)
- Cobertura inferior às 27 UFs; (**Mitigação:** reavaliar fonte ou escopo do projeto)

