FROM python:3.13-alpine

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/app

WORKDIR /app

# Install build dependencies including gcc and sqlite
RUN apk add --no-cache gcc musl-dev libffi-dev sqlite-dev

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app

# Run the application server
CMD ["uvicorn", "backend.src.app.src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
