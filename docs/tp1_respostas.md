# Projeto de Bloco: Inteligência Artificial Aplicada [26E3_5]
# Teste de Performance - TP1 [Obrigatório]

# Desenvolvimento de Soluções Sustentáveis com ESG e a Agenda 2030

# 1. Identificar o Problema de Negócio
## 1.1. Defina o problema de negócio que sua aplicação irá resolver.

Organizações sociais e gestores públicos precisam decidir quais Unidades da Federação devem receber análise prioritária no planejamento de ações de enfrentamento à pobreza. Entretanto, os dados oficiais estão apresentados de forma fria e sem maiores análises comparativas e respostas claras e diretas para uma rápida e estruturada tomada de decisão.

> Pergunta de negócio: Quais unidades da federação apresentam as maiores proporções de população abaixo da linha internacional de pobreza e devem receber análise prioritária para o planejamento de ações sociais?

## 1.2. Estabeleça as metas e os indicadores que determinarão o sucesso do projeto.
- **Meta principal:** Possibilitar que o usuário identifique as cinco Unidades da Federação com as maiores proporções abaixo da linha internacional de probreza, antes de qualquer filtro no painel.
- **Indicadores sugeridos:**

| Apresentação das 27 Unidades da Federação |
| Identificação das cinco Unidades da Federação com os maiores valores de pobreza |
| Utilização do período mais recente do dado como a visualização inicial do painel |

## 1.3. Escreva a qual ODS seu projeto atende e justifique sua resposta.
- O projeto está alinhado ao Objetivo **ODS 1 — Erradicação da Pobreza** que busca acabar com a pobreza em todas as suas formas e em todos os lugares.
- Mais especificamente, a aplicação contribui para a **Meta 1.1 - Indicador 1.1.1 - Proporção da população abaixo da linha internacional de pobreza**.
- Ao tornar os dados mais acessíveis em nível de informação de valor, o dashboard poderá auxiliar gestores e organizações sociais na identificação dos territórios que necessitam de análise prioritária e no planejamento de ações baseadas em evidências que permitam a otimização de recursos.

## 1.4. Estabeleça qual o público-alvo de sua aplicação.
- Gestores de organizações sociais que atuam no enfrentamento à pobreza;
- Gestores públicos responsáveis pelo planejamento de políticas e programas sociais;
- Fundações e instituições que financiam ou apoiam projetos sociais;

# 2. Organização do Projeto:
## 2.1. Estruture seu projeto utilizando os métodos CRISP-DM (Cross-Industry Standard Process for Data Mining) e TDSP (Team Data Science Process).

> Aplicação do método CRISP-DM na organização do trabalho

- **Entendimento do Negócio:** como já realizado acima, definimos o problema, a pergunta de negócio, o público alvo, estabelecemos os ODS que a problemática responde e os indicadores de sucesso;
- **Entendimento dos Dados:** será feito em seguida a identificação detalhada dos dados disponibilizados pela API do IBGE e sua avaliação;
- **Preparação dos Dados:** nesta fase vamos tratar as chamadas da API em JSON e tratá-las para o padrão tabular;
- **Modelagem:** tendo a clareza do nosso problema, essa fase será o momento de comparar as unidades da federação e ordená-las e quantificar de formas que nos permita visualizar a "fotografia" da estratificação;
- **Avaliação:** nesta fase verificamos os resultados em relação a metas e indicadores, que estabelecemos anteriormente;
- **Implantação:** para nosso trabalho, essa fase se materializa com a disponibilização de uma aplicação desenvolvida em streamlit, ainda de forma local.

## 2.2. Compreenda as diferentes fases do ciclo de vida do TDSP e como elas se aplicam ao seu projeto.

> Aplicação do ciclo de vida conforme o método TDSP

- **Business Understanding:** nesta fase, nosso projeto se aplica com a definição do problema de negócio, dos objetivos, dos indicadores e das fontes de dados, tendo como artefato o Project Charter, que desenvolveremos em seguida.
- **Data Acquisition and Understanding:** aqui há de forma mais clara o processo de consulta aos dados, juntamente com o seu endendimento, culminando na elaboração do Data Summary Report;
- **Modeling:** em uma fase desse método, temos a junção da modelagem e da avaliação, portanto, uma construção da análise descritiva que faremos para a comparação entre as unidades da federação;
- **Deployment:** vamos desenvolver e implantar a aplicação em streamlit, de forma local para o momento;
- **Customer Acceptance:** e por fim, no método TDSP, há essa etapa tão importante de verificação da aceitação do público alvo em relação ao objetivo inicial declarado no problema de negócio.

# 3. Organização de Diretórios e Artefatos Iniciais:

## 3.1. Crie uma organização de diretórios que reflita as diferentes fases do ciclo de vida do TDSP.
- **Business Understanding:** docs/project_charter.md;
- **Data Acquisition and Understanding:** o código que faremos para extração dos dados ficará na pasta src, e os dados salvos em data, dividos por raw, processed e sample, além do data_summary_report.md que ficará na pasta docs;
- **Modeling:** dentro de src que salvaremos os códigos desenvolvidos para modelagem e preparação para a aplicação em stramlit;
- **Deployment:** para deployment, teremos os arquivos app.py, requirements.txt e .gitignore na pasta raiz do projeto;
- **Customer Acceptance:** eventuais documentos de avaliação e aceitação da aplicação podem ser salvos na pasta docs. 

## 3.2. Desenvolva os artefatos iniciais do projeto, incluindo:
## 3.3. Project Charter: Documento que descreve o escopo, os objetivos e os stakeholders do projeto.
- Veja o arquivo em "Projeto de Bloco\painel_pobreza_ods1\docs\project_charter.md"

## 3.4. Data Summary Report: Relacione as fontes de dados que serão utilizadas, indicando o tipo de dados e o objetivo de uso. Este será o primeiro esboço do Data Summary Report.
- Veja o arquivo em "Projeto de Bloco\painel_pobreza_ods1\docs\data_summary_report.md"