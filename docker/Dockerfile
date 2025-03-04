FROM python:3.13-slim as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.1

WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

COPY ../pyproject.toml ../poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ../internal ./internal
COPY ../configs ./configs
COPY ../entrypoint ./cmd

ENV PYTHONPATH="/app"

CMD ["uvicorn", "cmd.main:app", "--host", "0.0.0.0", "--port", "8000"]
