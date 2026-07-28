# Rastreabilidade dos Requisitos de Entrega

## Fonte de verdade

Este documento consolida os requisitos do desafio a partir de:

- `learning/postech-FIAP/raw/fase-02/01-final_project.pdf`

Se houver conflito entre este documento e qualquer outro artefato do repositório, o PDF oficial prevalece.

## Entregáveis obrigatórios da pós

- Repositório GitHub
- Vídeo de até 5 minutos no formato STAR

## Escopo técnico obrigatório

- Problema de classificação com foco em propensão de compra em e-commerce
- Modelo clássico com `Scikit-Learn`
- Projeto com foco em Engenharia de Machine Learning
- Dependências gerenciadas por `Poetry` ou `uv`
- `Dockerfile` funcional
- Pipeline reprodutível com `DVC` e `dvc.yaml`
- Experimentos rastreados com `MLflow`
- Registro do melhor modelo no `MLflow Model Registry`
- Estrutura limpa, `type hints`, código legível e histórico de commits organizado

## Etapas oficiais do desafio

### Etapa 1 - Clean Code e Estrutura

Requisitos principais:

- Estrutura de pastas organizada
- Naming consistente
- `type hints`
- Docstrings nas funções principais
- Lint opcional recomendado

Status atual:

- `Parcialmente atendido`

Evidências:

- Estrutura base presente em `src/`, `tests/`, `data/`, `configs/`, `scripts/` e `doc/`
- `type hints` já aparecem nos módulos principais
- Ainda faltam docstrings e uma revisão objetiva de Clean Code contra o critério do PDF

### Etapa 2 - Ambiente e Dependências

Requisitos principais:

- `pyproject.toml` com dependências organizadas
- lock file commitado
- `.env.example`
- projeto instalável do zero

Status atual:

- `Parcialmente atendido`

Evidências:

- `pyproject.toml` presente
- `.env.example` presente
- fluxo de setup documentado no `README.md`

Pendências:

- confirmar e manter o lock file commitado como parte obrigatória da entrega
- validar o fluxo completo de instalação a partir de clone limpo como evidência de entrega

### Etapa 3 - Containerização e Versionamento

Requisitos principais:

- dataset versionado com `DVC`
- `dvc.yaml` com pipeline claro
- `Dockerfile` funcional

Status atual:

- `Não atendido`

Pendências:

- adicionar `dvc.yaml`
- definir estágios mínimos do pipeline, preferencialmente `preprocess -> train`
- adicionar `Dockerfile`
- documentar execução via Docker

### Etapa 4 - Modelagem, Registry e Entrega

Requisitos principais:

- treinar modelo simples com `Scikit-Learn`
- logar parâmetros, métricas e modelo no `MLflow`
- registrar o melhor modelo no registry
- finalizar `README.md`
- gravar o vídeo STAR

Status atual:

- `Parcialmente atendido`

Evidências:

- baseline com `LogisticRegression`
- carregamento de dados, pré-processamento, treino e avaliação já implementados
- testes automatizados cobrindo dados, features e treino

Pendências:

- integrar `MLflow`
- registrar modelo no registry
- fechar o fluxo com dataset real
- completar o `README.md` com DVC, MLflow e Docker
- preparar roteiro e evidências para o vídeo STAR

## Critérios de avaliação da pós

- Clean code e estrutura: `20%`
- Reprodutibilidade: `20%`
- Docker: `15%`
- DVC + Pipeline: `15%`
- Modelagem clássica: `10%`
- MLflow + Registry: `20%`

## Estado consolidado do repositório hoje

Atende hoje:

- enquadramento correto do problema
- escolha de dataset aderente ao PDF
- baseline clássico com `Scikit-Learn`
- estrutura mínima do projeto
- testes automatizados básicos

Ainda não atende como entrega final:

- `DVC`
- `MLflow`
- `Model Registry`
- `Dockerfile`
- execução ponta a ponta com dataset real
- evidência do vídeo STAR

## Ordem recomendada de implementação

1. Colocar o dataset real em `data/external/online_shoppers_intention.csv`
2. Fechar o fluxo mínimo de preparação e treino para o dataset real
3. Adicionar `DVC` com pipeline reprodutível
4. Integrar `MLflow` com logging de parâmetros, métricas e modelo
5. Adicionar `Dockerfile` e documentar execução
6. Fechar o `README.md` final com instruções completas de reprodução
7. Preparar o roteiro do vídeo STAR com base nos artefatos do repo
