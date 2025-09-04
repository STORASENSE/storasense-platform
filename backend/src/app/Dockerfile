FROM python:3.13-alpine

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/app

WORKDIR /app

# Install build dependencies including gcc and sqlite
RUN apk add --no-cache gcc musl-dev libffi-dev sqlite-dev openssl-dev librdkafka-dev

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

# Create non-root user
RUN addgroup --system --gid 1001 appuser
RUN adduser --system --uid 1001 appuser

RUN pip install --no-cache-dir confluent-kafka==2.10.0

USER appuser

# Run the application server
CMD ["uvicorn", "backend.src.app.src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
