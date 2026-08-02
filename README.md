# Tech Challenge Fase 2

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white" />
  <img alt="Poetry" src="https://img.shields.io/badge/Poetry-2.x-60A5FA?logo=poetry&logoColor=white" />
  <img alt="Scikit-Learn" src="https://img.shields.io/badge/scikit--learn-1.7-FFB300?logo=scikit-learn&logoColor=white" />
  <img alt="MLflow" src="https://img.shields.io/badge/MLflow-3.x-0194E2?logo=mlflow&logoColor=white" />
  <img alt="DVC" src="https://img.shields.io/badge/DVC-3.x-13ADC7?logo=dvc&logoColor=white" />
  <img alt="Ruff" src="https://img.shields.io/badge/Ruff-0.12-FFB000?logo=ruff&logoColor=white" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker-supported-2496ED?logo=docker&logoColor=white" />
</p>

Sistema de classificação binária para estimar a propensão de compra em uma sessão de navegação de e-commerce. O projeto prioriza Engenharia de Machine Learning, reprodutibilidade e clareza operacional.

## Dataset e target

O projeto usa o [Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention), com 12.330 sessões. A coluna `Revenue` é o target binário: `1`/`True` indica que a sessão resultou em compra; `0`/`False` indica que não resultou.

O baseline é `LogisticRegression` com `max_iter=1000`. A decisão está detalhada em [doc/DATASET_DECISION.md](./doc/DATASET_DECISION.md).

## Abordagem de programação

O projeto combina programação orientada a objetos e programação funcional de
forma intencional.

Na programação orientada a objetos, o projeto utiliza:

- `dataclasses` imutáveis para configurações, como `AppConfig`, `DatasetConfig`
  e `ModelConfig`, em [config.py](./src/purchase_propensity/config.py);
- `ExportSummary` para representar o resultado da exportação do dataset, em
  [dataset_fetch.py](./src/purchase_propensity/dataset_fetch.py);
- componentes orientados a objetos do scikit-learn, como `Pipeline`,
  `ColumnTransformer` e `LogisticRegression`.

Na programação funcional, o projeto utiliza funções pequenas e focadas em uma
responsabilidade, sem estado global mutável. Exemplos incluem:

- carregamento e validação em [data.py](./src/purchase_propensity/data.py);
- construção do pré-processamento em [features.py](./src/purchase_propensity/features.py);
- avaliação em [evaluate.py](./src/purchase_propensity/evaluate.py);
- orquestração do treinamento em [train.py](./src/purchase_propensity/train.py).

Essa combinação permite usar objetos para representar configurações, resultados
e componentes do pipeline, enquanto as funções executam as transformações e as
etapas do fluxo. Classes de serviço sem estado persistente não foram
introduzidas para evitar complexidade desnecessária e manter o pipeline coeso e
testável.

## Requisitos

- Python `>=3.11,<3.13` (Python 3.11 ou 3.12)
- [Poetry](https://python-poetry.org/), gerenciador suportado
- Docker, apenas para o fluxo em container

O Poetry é a interface de dependências do projeto. O `poetry.lock` deve ser usado para reproduzir as versões instaladas. A configuração da aplicação fica em `configs/base.yaml`; o `.env` é reservado para overrides opcionais da configuração do MLflow.

## Instalação e validação

```bash
make setup
make check
make lint
make test
```

`make setup` seleciona Python 3.12 ou 3.11, cria o ambiente virtual local `.venv` e instala as dependências usando o lock file. `make check` valida os metadados do projeto, `make lint` executa a análise estática com Ruff e `make test` executa os testes com pytest.

## Dados

Baixe o dataset oficial da UCI para o caminho configurado:

```bash
make fetch-data
```

O arquivo gerado é `data/external/online_shoppers_intention.csv`. O comando não substitui um arquivo existente. Para forçar a substituição:

```bash
poetry run python -m purchase_propensity.dataset_fetch --overwrite
```

O CSV bruto precisa existir antes de executar `make prepare`, `make dvc-repro` ou as etapas Docker. O arquivo é validado para conter as colunas esperadas e 12.330 linhas.

## Pipeline DVC

```bash
make prepare
make train
```

Ou reproduza as duas etapas declaradas em `dvc.yaml`:

```bash
make dvc-repro
```

As etapas são:

- `prepare`: lê o CSV bruto e cria `data/processed/train.csv` e `data/processed/test.csv`.
- `train`: treina o baseline, avalia no conjunto de teste e cria o modelo e as métricas.

O split é 80/20, usa `random_state=42` e estratificação pela coluna `Revenue`. O pré-processamento aplica imputação pela mediana e `StandardScaler` às colunas numéricas; aplica imputação pelo valor mais frequente e `OneHotEncoder(handle_unknown="ignore")` às colunas categóricas.

As métricas calculadas no conjunto de teste são `accuracy`, `precision`, `recall`, `f1` e `roc_auc`.

Artefatos gerados:

- `data/processed/train.csv`
- `data/processed/test.csv`
- `artifacts/model.joblib`
- `artifacts/metrics.json`

## MLflow

O treino registra as execuções localmente em SQLite, usando:

- Tracking URI: `sqlite:///mlruns/mlflow.db`
- Experimento: `tech-challenge-fase-2`
- Modelo registrado: `purchase-propensity-baseline`

O Registry é local e não corresponde a um servidor MLflow hospedado. O treino registra parâmetros, métricas, configuração, relatório de métricas e modelo.

O DVC é a fonte de reprodutibilidade do pipeline e controla os dados processados,
o modelo operacional e as métricas. O MLflow é a fonte de tracking e do Model Registry;
`mlruns/` é estado local não versionado pelo DVC e pode ser recriado ao executar
o treinamento.

As variáveis `MLFLOW_TRACKING_URI`, `MLFLOW_EXPERIMENT_NAME` e `MLFLOW_REGISTERED_MODEL_NAME` podem substituir os valores padrão. Consulte [.env.example](./.env.example) para os demais parâmetros documentados.

Para iniciar a UI local:

```bash
make mlflow-ui
```

Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Docker

```bash
make docker-build
make docker-prepare
make docker-train
```

Para reproduzir o pipeline DVC no container:

```bash
make docker-dvc-repro
```

Os alvos Docker montam o diretório do repositório no mesmo caminho absoluto dentro do container. Assim, `data/processed/`, `artifacts/` e `mlruns/` permanecem no host. A imagem utiliza Python 3.12 e instala as dependências com Poetry, sem usar a `.venv` do host.

O Docker não baixa o dataset automaticamente. Execute `make fetch-data` no host antes de `make docker-prepare` ou `make docker-dvc-repro`.

## Estrutura

```text
.
├── .env.example
├── Dockerfile
├── Makefile
├── README.md
├── configs/base.yaml
├── data/
├── doc/
├── dvc.yaml
├── dvc.lock
├── poetry.lock
├── src/purchase_propensity/
└── tests/
```

## Documentação complementar

- [AGENTS.md](./AGENTS.md): contrato de desenvolvimento do repositório.
- [doc/ARCHITECTURE.md](./doc/ARCHITECTURE.md): arquitetura e responsabilidades atuais.
- [doc/DATASET_DECISION.md](./doc/DATASET_DECISION.md): decisão do dataset e do baseline.
- [doc/CLEAN_CLONE_VALIDATION.md](./doc/CLEAN_CLONE_VALIDATION.md): evidência da validação em clone limpo.
- [doc/DELIVERY_STATUS.md](./doc/DELIVERY_STATUS.md): status atual dos requisitos e pendências.

## Evoluções futuras

Sugestões de evolução de infraestrutura, sem impacto nos requisitos obrigatórios
atuais, estão documentadas em [doc/FUTURE_EVOLUTIONS.md](./doc/FUTURE_EVOLUTIONS.md).
