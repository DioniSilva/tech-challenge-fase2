# Arquitetura

## Visão geral

O projeto implementa um pipeline de classificação binária para estimar a
propensão de compra em sessões de navegação de e-commerce.

O fluxo principal é:

```text
dataset UCI
    -> validação dos dados
    -> prepare
    -> train
    -> avaliação
    -> artifacts/model.joblib e artifacts/metrics.json
    -> tracking e Registry local no MLflow
```

## Organização do código

```text
src/purchase_propensity/
├── config.py
├── data.py
├── dataset_fetch.py
├── evaluate.py
├── features.py
├── mlflow_tracking.py
├── prepare.py
└── train.py
```

Responsabilidades principais:

- `config.py`: carrega e valida a configuração YAML e seus overrides de MLflow.
- `dataset_fetch.py`: obtém e exporta o dataset oficial da UCI.
- `data.py`: carrega, valida e separa features e target.
- `features.py`: constrói o preprocessing numérico e categórico.
- `prepare.py`: gera os splits estratificados de treino e teste.
- `train.py`: orquestra treinamento, avaliação e persistência dos artefatos.
- `evaluate.py`: calcula as métricas de classificação.
- `mlflow_tracking.py`: registra parâmetros, métricas, artefatos e modelo.

## Configuração

`configs/base.yaml` é a fonte principal para dataset, split, modelo, caminhos e
MLflow. O arquivo `.env` é opcional e pode sobrescrever somente:

- `MLFLOW_TRACKING_URI`;
- `MLFLOW_EXPERIMENT_NAME`;
- `MLFLOW_REGISTERED_MODEL_NAME`.

Os objetos de configuração são representados por dataclasses imutáveis. As
etapas do pipeline são executadas por funções pequenas e coesas. Essa
combinação aplica POO à configuração, aos resultados e aos componentes do
Scikit-Learn, e programação funcional para transformações e orquestração.

## DVC e MLflow

O DVC é a fonte de reprodutibilidade do pipeline. Ele declara:

```text
data/external/online_shoppers_intention.csv
    -> data/processed/train.csv
    -> data/processed/test.csv
    -> artifacts/model.joblib
    -> artifacts/metrics.json
```

O MLflow é a fonte de tracking e do Model Registry. O banco SQLite e os diretórios em
`mlruns/` são estado local, ignorado pelo Git e não versionado pelo DVC. Eles
podem ser recriados ao executar o treinamento.

O repositório não possui DVC remote configurado. Por isso, o dataset bruto é
adquirido com `make fetch-data` durante a reprodução. A validação desse fluxo
está registrada em [CLEAN_CLONE_VALIDATION.md](./CLEAN_CLONE_VALIDATION.md).

## Docker

O `Dockerfile` instala o mesmo ambiente Poetry usado pelo projeto e o
`Makefile` monta o repositório do host no container. Assim, os artefatos
gerados permanecem no host.

O Docker não adquire o dataset automaticamente. A aquisição deve ocorrer no
host antes de `make docker-prepare` ou `make docker-dvc-repro`.

## Entrypoints

O `Makefile` é a interface operacional canônica. Os principais comandos são:

- `make setup`: instala o ambiente;
- `make fetch-data`: adquire o dataset;
- `make prepare`: gera os splits;
- `make train`: treina e registra o modelo;
- `make dvc-repro`: reproduz o pipeline;
- `make docker-build`: constrói a imagem;
- `make docker-dvc-repro`: reproduz o pipeline em container.

## Saídas geradas

Os diretórios abaixo são saídas locais e ignoradas pelo Git:

- `data/processed/`;
- `artifacts/`;
- `mlruns/`;
- caches de ferramentas e ambiente virtual.
