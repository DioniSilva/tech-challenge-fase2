# Status da Entrega

## Entregáveis

- Repositório GitHub
- Vídeo de até 5 minutos no formato STAR

## Status atual dos requisitos

| Requisito | Status | Evidência |
|---|---|---|
| Classificação binária de propensão de compra | Atendido | `README.md`, `DATASET_DECISION.md` |
| Modelo clássico com Scikit-Learn | Atendido | `src/purchase_propensity/train.py` |
| Engenharia de Machine Learning | Atendido | pipeline DVC, Docker e MLflow |
| clean code, convenções de nomenclatura, anotações de tipo, docstrings e lint | Atendido | `src/`, `tests/`, `pyproject.toml`, `make lint` |
| Dependências separadas entre produção e desenvolvimento | Atendido | `pyproject.toml`, `poetry.lock` |
| Instalação reproduzível | Atendido | `README.md`, `poetry.lock`, `CLEAN_CLONE_VALIDATION.md` |
| Pipeline DVC | Atendido | `dvc.yaml`, `dvc.lock` |
| Docker funcional | Atendido | `Dockerfile`, `CLEAN_CLONE_VALIDATION.md` |
| Rastreamento e registro de modelos no MLflow | Atendido | `src/purchase_propensity/mlflow_tracking.py` |
| Histórico de commits compreensível | Atendido | histórico Git linear em `main` |
| Vídeo STAR | Pendente | entrega externa ao repositório |

## Critérios de avaliação

- Clean code e estrutura: `20%`
- Reprodutibilidade: `20%`
- Docker: `15%`
- DVC + Pipeline: `15%`
- Modelagem clássica: `10%`
- MLflow + Registry: `20%`

## Validação atual

- `make check`, `make lint` e `make test` passaram com `20 passed`.
- `make dvc-repro` passou localmente.
- `make docker-build` e `make docker-dvc-repro` passaram.
- clone limpo validado em [CLEAN_CLONE_VALIDATION.md](./CLEAN_CLONE_VALIDATION.md).

## Próximo passo

Preparar o roteiro e as evidências do vídeo STAR.
