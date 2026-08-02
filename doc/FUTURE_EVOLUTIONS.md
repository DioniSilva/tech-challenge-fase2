# Evoluções Futuras

Este documento reúne sugestões de evolução de infraestrutura. Elas não fazem
parte dos requisitos obrigatórios atuais e não alteram o status da entrega.

## Estado atual

- O DVC utiliza a configuração local do repositório e não possui remote
  configurado.
- O MLflow utiliza SQLite e arquivos locais em `mlruns/`.
- O pipeline atual é reproduzível com aquisição do dataset via `make fetch-data`.
- As evoluções abaixo podem ser implementadas posteriormente, conforme a
  necessidade de compartilhamento, colaboração ou operação contínua.

## DVC remoto

Um DVC remote permitiria armazenar e recuperar datasets e artefatos fora da
máquina local. Opções possíveis incluem:

- Amazon S3;
- Google Drive;
- Azure Blob Storage;
- MinIO;
- servidor SSH.

Uma configuração futura poderia seguir este fluxo:

```bash
dvc remote add -d storage <url-do-remote>
dvc push
```

Em outro ambiente, os dados e artefatos poderiam ser recuperados com:

```bash
dvc pull
```

As credenciais do storage devem ser configuradas por mecanismos seguros e não
devem ser commitadas no repositório.

## MLflow remoto

O tracking local poderia ser substituído por uma arquitetura compartilhada
composta por:

- MLflow Tracking Server;
- backend relacional, como PostgreSQL ou MySQL;
- artifact store, como S3, MinIO ou Azure Blob Storage;
- Model Registry compartilhado.

A aplicação já permite configurar o tracking por variáveis de ambiente:

```env
MLFLOW_TRACKING_URI=<tracking-uri-remoto>
MLFLOW_EXPERIMENT_NAME=tech-challenge-fase-2
MLFLOW_REGISTERED_MODEL_NAME=purchase-propensity-baseline
```

Em uma implantação remota, também seriam necessários autenticação, controle
de acesso, gerenciamento de secrets e políticas de retenção dos artefatos.

## Critério para adoção

Essas evoluções devem ser consideradas quando houver necessidade de:

- compartilhar dados e artefatos entre ambientes;
- permitir colaboração entre várias pessoas;
- manter histórico de experimentos em uma infraestrutura centralizada;
- executar treinamento em CI/CD ou infraestrutura de produção.

Até que essas necessidades existam, a configuração local permanece adequada ao
escopo do Tech Challenge e reduz a complexidade operacional.
