FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src \
    POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_SYSTEM_GIT_CLIENT=true \
    DVC_NO_ANALYTICS=true

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock README.md Makefile ./
RUN poetry install --with dev --no-root

COPY . .
RUN mkdir -p artifacts mlruns data/external data/processed

CMD ["make", "train"]
