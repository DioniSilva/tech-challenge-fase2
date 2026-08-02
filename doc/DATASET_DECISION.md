# Decisão de Dataset e Baseline

## Resumo da decisão

Data da decisão: `2026-07-23`

- Dataset selecionado: `Online Shoppers Purchasing Intention Dataset`
- Baseline selecionado: `LogisticRegression`
- Coluna target: `Revenue`
- Tipo de problema: classificação binária

## Motivos da decisão

Este dataset é a opção mais adequada e pragmática para o Tech Challenge porque atende
ao escopo oficial com pouca ambiguidade.

Ele foi selecionado porque:

- representa um contexto de navegação em e-commerce;
- possui um target binário nativo (`Revenue`);
- evita transformar o projeto inicialmente em um problema de engenharia do
  alvo;
- permite chegar rapidamente a evidências reproduzíveis de ML Engineering.

## Datasets não selecionados

### RetailRocket

- Tem forte aderência a recomendação e eventos de interação.
- Não é o melhor encaixe para a classificação de propensão de compra deste
  projeto.
- Poderia direcionar o projeto para arquitetura de recomendação.

### Instacart

- É um benchmark relevante para histórico de compras.
- Não representa naturalmente o problema atual de classificação de propensão.
- É mais adequado para recomendação ou previsão de recompra.

### Olist

- Possui contexto de negócio e sinais relacionais ricos.
- Exigiria derivar um target binário e definir cuidadosamente a granularidade
  da análise.
- Apresenta maior ambiguidade inicial que o dataset escolhido.

### MovieLens

- É um benchmark clássico de recomendação.
- Não é aderente ao enquadramento atual do desafio.

## Justificativa do baseline

`LogisticRegression` foi escolhido como baseline porque é:

- simples;
- interpretável;
- padrão para classificação binária tabular;
- fácil de reproduzir;
- suficiente para o primeiro marco de engenharia de machine learning.

O objetivo inicial não é maximizar a performance. É estabelecer uma primeira
versão correta, reproduzível e documentável.

## Consequências da decisão

Esta decisão implica que:

- o projeto seja estruturado como classificação binária em nível de sessão;
- o primeiro pipeline de treinamento use `Revenue`;
- o preprocessing priorize clareza e reprodutibilidade;
- a avaliação utilize métricas padrão de classificação;
- futuros modelos sejam comparados com o baseline `LogisticRegression`.

## Documentação relacionada

- [Arquitetura](./ARCHITECTURE.md)
- [Status da entrega](./DELIVERY_STATUS.md)
- [Orientações para agentes](../AGENTS.md)
