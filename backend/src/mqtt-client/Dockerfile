FROM python:3.13-slim

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/mqtt-client

WORKDIR /mqtt-client

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* /mqtt-client/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Run the application server
CMD ["uvicorn", "mqtt-client.main:app", "--reload"]
