# Tech Challenge Fase 2

Repositório do Tech Challenge da Fase 2 da pós-tech FIAP.

## Objetivo

Construir um sistema preditivo para estimar a **propensão de compra** de um usuário com base em seu **comportamento de navegação** em um contexto de e-commerce.

O foco principal deste projeto é **Engenharia de Machine Learning**:

- organização de código;
- reprodutibilidade;
- empacotamento do ambiente;
- containerização;
- versionamento de dados;
- rastreamento de experimentos;
- documentação de entrega.

## Fonte oficial

A fonte de verdade do projeto é:

- `learning/postech-FIAP/raw/fase-02/01-final_project.pdf`

Se houver conflito entre este repositório, notas antigas e o PDF oficial, o PDF prevalece.

## O que este projeto deve entregar

### Obrigatório

- Repositório GitHub com implementação reproduzível.
- Vídeo de até 5 minutos no formato STAR.

### Opcional

- Deploy em nuvem.

## Escopo técnico esperado

- Problema de **classificação binária**.
- Modelo clássico com **Scikit-Learn**.
- Gerenciamento de dependências com `Poetry` ou `uv`.
- Pipeline reproduzível com `DVC`.
- Tracking e registry com `MLflow`.
- Execução reproduzível com `Docker`.

## Fora de escopo por padrão

Este projeto **não** deve ser conduzido como:

- sistema de recomendação;
- projeto centrado em `PyTorch`;
- projeto centrado em redes neurais;
- experimento excessivamente orientado a pesquisa.

Qualquer desvio nessa direção deve ser uma decisão explícita, não o caminho padrão.

## Estrutura atual

```text
.
├── AGENTS.md
├── README.md
├── Makefile
├── pyproject.toml
├── .env.example
├── .gitignore
├── .dockerignore
├── doc/
├── raw/
├── src/
├── tests/
├── data/
├── configs/
└── scripts/
```

## Estado atual

- Fonte oficial do desafio validada.
- `AGENTS.md` criado para orientar desenvolvimento agentico.
- Documentação-base do projeto consolidada.
- Dataset principal definido: **Online Shoppers Purchasing Intention Dataset**.
- Target definido: **`Revenue`**.
- Baseline inicial definido: **`LogisticRegression`**.
- Estrutura do projeto aplicada com `Makefile` + `Poetry`.
- Pipeline reproduzível com `DVC` implementado.
- Tracking local com `MLflow` e Model Registry implementados.
- Execução em `Docker` implementada e validada.

## Documentação do projeto

- Guia para agentes: [AGENTS.md](./AGENTS.md)
- Especificação inicial do projeto: [doc/PROJECT_SPEC.md](./doc/PROJECT_SPEC.md)
- Decisão de dataset e baseline: [doc/DATASET_DECISION.md](./doc/DATASET_DECISION.md)
- Spec da estrutura mínima: [doc/MINIMAL_PROJECT_STRUCTURE_SPEC.md](./doc/MINIMAL_PROJECT_STRUCTURE_SPEC.md)
- Rastreabilidade dos requisitos de entrega: [doc/DELIVERY_REQUIREMENTS_TRACEABILITY.md](./doc/DELIVERY_REQUIREMENTS_TRACEABILITY.md)

## Como inicializar

Pré-requisito:

- `poetry` instalado na máquina
- `python3.11` ou `python3.12` disponível no shell

Fluxo mínimo:

```bash
make venv
make setup
make test
make fetch-data
make dvc-repro
```

Comandos disponíveis:

- `make help`: lista os alvos principais
- `make venv`: cria o ambiente virtual local `.venv` com `Poetry`, tentando `python3.12` e depois `python3.11`
- `make setup`: inicializa o ambiente e instala dependências com `Poetry`
- `make check`: valida o `pyproject.toml`
- `make test`: executa os testes
- `make fetch-data`: baixa o dataset oficial da UCI para `data/external/`
- `make prepare`: gera os conjuntos processados de treino e teste
- `make train`: treina o baseline a partir dos dados processados
- `make dvc-repro`: reproduz o pipeline definido no `dvc.yaml`
- `make mlflow-ui`: sobe a UI local do `MLflow`
- `make docker-build`: gera a imagem Docker local
- `make docker-prepare`: executa a etapa de preparação em container
- `make docker-train`: executa o treino em container
- `make docker-dvc-repro`: executa o pipeline completo em container

## Observação sobre dados

O repositório já está preparado para o dataset escolhido.

Aquisição recomendada a partir da UCI:

```bash
make fetch-data
```

Isso salva o CSV oficial em:

- `data/external/online_shoppers_intention.csv`

Se o arquivo já existir e você quiser substituir, use:

```bash
poetry run python -m purchase_propensity.dataset_fetch --overwrite
```

## Pipeline com DVC

Fluxo mínimo esperado para a entrega:

```bash
make fetch-data
make dvc-repro
make mlflow-ui
```

Saídas principais do pipeline:

- `data/processed/train.csv`
- `data/processed/test.csv`
- `artifacts/model.joblib`
- `artifacts/metrics.json`

O `dvc.yaml` materializa o fluxo mínimo aderente ao PDF:

- `prepare`: valida o dataset bruto e gera os splits processados
- `train`: treina o baseline e salva métricas + modelo

## Tracking com MLflow

O treino agora registra automaticamente:

- parâmetros do dataset, split e modelo
- métricas do baseline
- arquivos de configuração e métricas
- o modelo no Tracking
- uma versão registrada no Model Registry local

Configuração padrão:

- Tracking URI: `sqlite:///mlruns/mlflow.db`
- Experimento: `tech-challenge-fase-2`
- Modelo registrado: `purchase-propensity-baseline`

Para inspecionar localmente a UI:

```bash
make mlflow-ui
```

## Execucao com Docker

Build da imagem local:

```bash
make docker-build
```

Executar os passos principais em container:

```bash
make docker-prepare
make docker-train
make docker-dvc-repro
```

Observacoes:

- os alvos Docker montam o repositorio no mesmo caminho absoluto do host
- os arquivos gerados em `data/processed/`, `artifacts/` e `mlruns/` ficam persistidos no host
- a imagem usa `Poetry` sem depender da `.venv` local do host
- o dataset bruto precisa existir no repositorio antes de rodar `docker-prepare` ou `docker-dvc-repro`

## Próximos passos recomendados

1. Refinar a documentação final da entrega com evidências objetivas dos fluxos local e Docker.
2. Validar o projeto a partir de clone limpo para consolidar a reprodutibilidade exigida pela pós.
3. Preparar o roteiro do vídeo STAR com base em `DVC`, `MLflow`, `Docker` e métricas do baseline.
4. Revisar Clean Code e docstrings nos módulos principais.
5. Organizar o histórico de commits final para a entrega.

## Critério de sucesso

Este repositório estará bem encaminhado quando conseguir provar, por meio dos próprios artefatos:

- problema claramente definido;
- dataset e target documentados;
- ambiente instalável do zero;
- pipeline reproduzível;
- experimentos rastreados;
- modelo registrado;
- execução reproduzível em Docker;
- README suficiente para reprodução da entrega.
