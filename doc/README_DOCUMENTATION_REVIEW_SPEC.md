# Spec: Revisao da Documentacao do Projeto

## Objetivo

Tornar a documentacao suficiente para que uma pessoa consiga instalar,
reproduzir e inspecionar o projeto sem depender de conhecimento previo do
repositorio.

## Escopo

- Revisar o `README.md`.
- Revisar documentos complementares quando houver conflito ou informacao
  desatualizada.
- Nao alterar o escopo tecnico, o modelo ou a estrutura de execucao do projeto.
- Nao modificar o `README.md` para registrar o backlog de prioridades; esse
  registro permanece em `doc/DELIVERY_REQUIREMENTS_TRACEABILITY.md`.

## Requisitos funcionais da documentacao

### Instalação

- Informar Python suportado: `>=3.11,<3.13`.
- Informar Poetry como gerenciador atualmente suportado.
- Explicar que `make setup` cria/configura o ambiente e instala as
  dependencias usando o lock file.
- Documentar `make check` e `make test`.

### Dados

- Identificar o Online Shoppers Purchasing Intention Dataset.
- Informar que o dataset possui 12.330 sessoes.
- Definir `Revenue` como target binario e explicar o significado de `1/True`.
- Documentar `make fetch-data`, o caminho do CSV e o uso de `--overwrite`.
- Explicar que o arquivo bruto precisa existir antes do `dvc repro` e das
  etapas Docker.

### Pipeline

- Documentar as etapas `prepare` e `train` do DVC.
- Informar split 80/20, `random_state=42` e estratificacao por `Revenue`.
- Descrever imputacao, padronizacao e one-hot encoding.
- Descrever o baseline `LogisticRegression` e `max_iter=1000`.
- Listar as metricas geradas no conjunto de teste.
- Listar os artefatos gerados e seus caminhos.

### MLflow

- Documentar Tracking local em SQLite.
- Informar experimento e nome do modelo registrado.
- Documentar parametros de ambiente suportados, quando aplicavel.
- Explicar como iniciar a UI e informar `http://127.0.0.1:5000`.
- Deixar claro que o Registry descrito e local, nao um servidor hospedado.

### Docker

- Documentar build e execucao local.
- Explicar bind mount e persistencia dos artefatos.
- Explicar que Docker nao baixa o dataset automaticamente.
- Evitar alegacoes de validacao sem comando ou evidencia correspondente.

### Estrutura e linguagem

- Atualizar a arvore para refletir os arquivos relevantes presentes no repo.
- Manter links relativos validos.
- Corrigir acentuacao e inconsistencias de nomenclatura.
- Usar Makefile como interface canonica, salvo quando um comando direto for
  necessario para explicar uma operacao especifica.

## Requisitos de qualidade

- Os comandos documentados devem corresponder ao `Makefile`, `Dockerfile`,
  `dvc.yaml`, `pyproject.toml` e `configs/base.yaml`.
- A documentacao nao deve prometer remote DVC, deploy ou suporte a `uv` se
  esses recursos nao estiverem configurados.
- A revisao deve preservar informacoes corretas que ja existam.

## Validacao

- Verificar links e caminhos mencionados.
- Executar, quando disponivel, `make check` e `make test`.
- Validar que os comandos principais do README existem no `Makefile`.
- Revisar o diff para garantir que apenas documentacao e a spec sejam
  alteradas nesta etapa.

## Entregaveis

- `doc/README_DOCUMENTATION_REVIEW_SPEC.md`.
- README revisado.
- Documentos complementares ajustados apenas quando necessario.
- Relatorio final com alteracoes, validacoes executadas e pendencias.
