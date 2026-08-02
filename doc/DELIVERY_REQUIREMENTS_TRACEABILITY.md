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

- `Atendido com melhorias contínuas`

Evidências:

- Estrutura base presente em `src/`, `tests/`, `data/`, `configs/` e `doc/`
- `type hints` aplicados às funções públicas dos módulos principais
- docstrings adicionadas às funções públicas de produção
- Ruff configurado no `pyproject.toml` e disponível via `make lint`
- naming conventions e responsabilidades separadas por módulo
- testes de caminhos de erro adicionados aos testes de dados e treino

Pendências:

- avaliar regras adicionais de tipagem estática caso o projeto evolua
- revisar funções maiores sob a ótica do critério de Clean Code da pós

### Etapa 2 - Ambiente e Dependências

Requisitos principais:

- `pyproject.toml` com dependências organizadas
- lock file commitado
- `.env.example`
- projeto instalável do zero

Status atual:

- `Atendido`

Evidências:

- `pyproject.toml` presente
- `.env.example` presente
- fluxo de setup documentado no `README.md`
- `poetry.lock` presente
- `make check` validado sem warnings

Pendências menores:

- registrar explicitamente a validação em clone limpo na documentação final

### Etapa 3 - Containerização e Versionamento

Requisitos principais:

- dataset versionado com `DVC`
- `dvc.yaml` com pipeline claro
- `Dockerfile` funcional

Status atual:

- `Atendido`

Evidências:

- `dvc.yaml` implementado com `prepare -> train`
- dataset bruto rastreado por `DVC`
- DVC definido como fonte de reprodutibilidade; MLflow tratado como tracking e Registry local não versionado
- `Dockerfile` funcional criado
- execução em container validada com `docker build`, `docker-prepare`, `docker-train` e `docker-dvc-repro`

### Etapa 4 - Modelagem, Registry e Entrega

Requisitos principais:

- treinar modelo simples com `Scikit-Learn`
- logar parâmetros, métricas e modelo no `MLflow`
- registrar o melhor modelo no registry
- finalizar `README.md`
- gravar o vídeo STAR

Status atual:

- `Atendido com pendência de entrega final`

Evidências:

- baseline com `LogisticRegression`
- carregamento de dados, pré-processamento, treino e avaliação já implementados
- testes automatizados cobrindo dados, features e treino
- `MLflow` integrado com tracking local
- modelo registrado no `MLflow Model Registry`
- fluxo fechado com dataset real
- `README.md` atualizado com DVC, MLflow e Docker

Pendências:

- preparar roteiro e evidências do vídeo STAR

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
- `DVC`
- `MLflow`
- `Model Registry`
- `Dockerfile`
- execução ponta a ponta com dataset real

Ainda não atende como entrega final:

- evidência do vídeo STAR
- validação documentada a partir de clone limpo

## Validação executada em 2026-07-28

Comandos validados com sucesso:

- `make check`
- `make test`
- `make train`
- `make dvc-repro`
- `make docker-build`
- `make docker-dvc-repro`

Evidências objetivas desta validação:

- `make test` passou com `9 passed`
- `make train` gerou métricas e registrou nova versão do modelo `purchase-propensity-baseline` no `MLflow`
- o experimento `tech-challenge-fase-2` está presente no tracking local
- `make dvc-repro` confirmou pipeline íntegro com estágios em cache
- `make docker-build` validou a imagem local
- `make docker-dvc-repro` confirmou o fluxo reproduzível também em container

Conclusão prática:

- tudo o que foi implementado até agora atende ao escopo técnico já construído no repositório
- o que ainda falta para a entrega final não é implementação central do pipeline, e sim evidência complementar de entrega: vídeo STAR e validação formal em clone limpo

## Validação após a revisão técnica

Validações executadas após as melhorias de configuração, validação de dados,
refatoração do treinamento e organização estrutural:

- `make check` passou.
- `make lint` passou com as regras Ruff configuradas.
- `make test` passou com `20 passed`.
- `make prepare` gerou os splits processados.
- `make train` gerou métricas e registrou a versão `7` do modelo no MLflow local.
- `make dvc-repro` confirmou que os estágios estão atualizados.
- `git diff --check` passou.

O clone limpo e a validação Docker permanecem como evidências de entrega a
serem executadas na etapa específica de reprodutibilidade.

## Ordem recomendada de implementação

1. Consolidar a documentação final da reprodução local e Docker
2. Registrar uma validação em clone limpo como evidência de reprodutibilidade
3. Preparar o roteiro do vídeo STAR com base nos artefatos do repo
4. Revisar Clean Code e docstrings onde ainda houver lacunas

## Prioridade de conclusão da entrega

Esta ordem representa o backlog final de entrega. Cada etapa deve produzir ou atualizar evidências no repositório:

1. Revisão da documentação do projeto (`README.md` e documentação complementar)
2. Reprodutibilidade e clone limpo
3. Revisão técnica do código
4. Roteiro do vídeo STAR
