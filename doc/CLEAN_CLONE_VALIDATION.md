# Validacao de Clone Limpo

## Identificacao

- Repositorio: `DioniSilva/tech-challenge-fase2`
- Branch: `main`
- Commit validado: `a90d43f`
- Data: `2026-08-02`
- Ambiente: macOS, Python 3.12, Poetry e Docker

## Procedimento

A validacao foi executada em um diretorio temporario independente, criado a
partir do repositorio publicado no GitHub. O clone nao reutilizou `.venv`,
cache DVC, artefatos, banco MLflow ou dados do workspace original.

```bash
git clone git@github.com:DioniSilva/tech-challenge-fase2.git
make setup
make check
make lint
make test
make fetch-data
make dvc-repro
make docker-build
make docker-dvc-repro
```

## Resultados

- O clone inicial estava limpo e apontava para o commit `a90d43f`.
- `make setup` criou um ambiente Poetry novo e instalou as dependencias pelo
  `poetry.lock`.
- `make check` passou.
- `make lint` passou.
- `make test` passou com `20 passed`.
- `make fetch-data` baixou e validou 12.330 registros e 18 colunas.
- `make dvc-repro` executou `prepare` e `train` sem depender do cache DVC do
  workspace original.
- O treino gerou os artefatos e registrou a versao `1` do modelo no MLflow
  local do clone.
- `make docker-build` construiu a imagem `tech-challenge-fase-2:local`.
- `make docker-dvc-repro` executou o pipeline dentro do container.
- O clone permaneceu limpo apos a validacao; dados e artefatos gerados sao
  ignorados pelo Git.

## Metricas observadas

As metricas do treino no clone foram:

- Accuracy: `0.8811841038118411`
- Precision: `0.7431693989071039`
- Recall: `0.35602094240837695`
- F1: `0.4814159292035398`
- ROC AUC: `0.8877134186170373`

## Limitacao conhecida

O repositorio nao possui um DVC remote configurado. Por isso, o dataset bruto
e adquirido da UCI com `make fetch-data` durante a reproducao. O DVC controla o
dataset por meio do arquivo `.dvc`, mas o armazenamento remoto do cache ainda
nao faz parte da entrega.

O estado local `mlruns/` tambem nao e versionado pelo DVC. Ele e recriado pela
execucao do treinamento e serve como tracking e Registry local.
