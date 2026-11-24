# Integração Local com Modelo de Linguagem

## Objetivo
O projeto passou a utilizar um modelo de linguagem executado localmente para gerar resumos das notícias sobre pobreza coletadas da Agência Brasil.
O usuário seleciona uma notícia no Streamlit, e o texto é enviado à API FastAPI para processamento.

## Ambiente utilizado
| Recurso | Configuração |
|---|---|
| Sistema | Windows 11 |
| Processador | Intel Core i7-1355U |
| CPUs lógicas | 12 |
| Memória RAM | 15,7 GB |
| GPU CUDA | Não disponível |
| Python | 3.14.6 |
| Execução | CPU local |

## Criação do ambiente virtual
Foi criado um ambiente virtual separado para as dependências locais da LLM. No Git Bash do Windows, foram utilizados os seguintes comandos:

```bash
python -m venv "/c/Python Projects/venvs/painel_pobreza_tp4"

source "/c/Python Projects/venvs/painel_pobreza_tp4/Scripts/activate"

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

python -m pip install -r requirements-llm.txt

python -m pip check
```

## Bibliotecas principais:
- PyTorch 2.15.0+cpu;
- Transformers 5.22.2;
- SentencePiece 0.2.3;
- Hugging Face Hub 2.4.0.

## Modelos avaliados
| Critério | T5 português pequeno | PTT5 base XL-Sum |
|---|---:|---:|
| Identificador | `rhaymison/t5-portuguese-small-summarization` | `recogna-nlp/ptt5-base-summ-xlsum` |
| Parâmetros aproximados | 60 milhões | 200 milhões |
| Tamanho dos pesos | 242 MB | 892 MB |
| Carregamento observado | 4,54 s | 5,43 s |
| Inferência observada | 11,12 s | 7,77 s |
| Resultado | Preservou os fatos principais | Introduziu informações incorretas |

No teste realizado, o primeiro modelo preservou o percentual de 32,3% e o período de 2026. O segundo informou incorretamente o ano de 2024 e mencionou Néstor Kirchner, informação ausente da notícia.

## Modelo escolhido
Foi selecionado `rhaymison/t5-portuguese-small-summarization` considerando:
- **Desempenho:** maior fidelidade dos fatos no teste realizado;
- **Custo computacional:** possui menos parâmetros e pesos menores;
- **Acessibilidade:** está disponível no Hugging Face e funciona em CPU.

O modelo apresentou falhas de acentuação em algumas palavras, mas essa limitação foi considerada menos grave do que a criação de informações incorretas.

## Engenharia de prompt
O modelo recebe a instrução definida em `src/resumidor_llm.py`:

```python
PROMPT_RESUMO = "sumarize: {texto}"
```

## Configuração local:
As dependências de IA foram separadas em requirements-llm.txt, evitando instalar PyTorch e Transformers nos serviços publicados no Render durante o TP3.

Download ou verificação do modelo:

```bash
python -m src.baixar_modelo
```

O modelo é armazenado no cache da Hugging Face e não é enviado ao GitHub.

Durante a configuração, foi necessário atualizar o Protobuf para versão 7.36.1 devido à compatibilidade com o SentencePiece.

## Integração com FastAPI
O modelo é carregado uma única vez durante o `lifespan` da API e armazenado em `app.state`.

O fluxo implementado é:
1. o Streamlit seleciona o texto da notícia;
2. `src/api_client.py` envia o texto à API;
3. o Pydantic valida a entrada;
4. `src/resumidor_llm.py` gera o resumo;
5. o Response Model valida a resposta;
6. o resultado é apresentado no Streamlit.

Execução local:

```bash
uvicorn api.main:app
```

Em outro terminal:

```bash
streamlit run app.py
```

Documentação da API:

http://127.0.0.1:8000/docs

## Rota de processamento

A rota implementada foi:

`POST /processar_texto`

Entrada:

```json
{
  "texto": "Texto da notícia que será resumida."
}
```

A resposta contém:

- tipo de análise;
- modelo utilizado;
- resumo;
- quantidade de caracteres e tokens;
- indicação de truncamento;
- tempo de inferência;
- confirmação de execução local.

## Tratamento de erros

| Código | Situação |
|---:|---|
| 200 | Resumo gerado |
| 422 | Texto inválido |
| 500 | Erro inesperado na inferência |
| 503 | Modelo local indisponível |

Os retornos 422, 500 e 503 foram simulados e testados.

## Consolidação da solução no TP5
Entre as opções propostas no TP5, foi escolhida a automação de sumarização de textos com LLM.

A escolha aproveita diretamente os dados textuais coletados por web scraping. O usuário seleciona uma notícia no dashboard, solicita o proecssamento e recebe um resumo gerado localmente, acompanhado das informações técnicas da inferência e do link para a fonte original.

A solução não implementa memória conversacional nem agente autônomo, pois essas funcionalidades não são necessárias para o problema definido. A sumarização mantém o escopo objetivo, reduz custo computacional e utiliza diretamente a base textual construída durante todo o projeto.

## Limitações

- o modelo processa no máximo 512 tokens;
- textos maiores são truncados;
- o resumo pode omitir informações;
- foram observadas falhas de acentuação;
- o conteúdo original deve ser conferido;
- a funcionalidade não substitui análise humana.

A interface informa quando houve truncamento e disponibiliza o link da notícia original.

## Decisões técnicas

Os padrões de download separado, cache local, `local_files_only=True`, `lifespan`, `app.state`, Response Models e tratamento com `HTTPException` foram baseados no conteúdo das aulas.

A comparação entre modelos, a sumarização das notícias e a separação das dependências locais foram adaptações realizadas para este projeto.
