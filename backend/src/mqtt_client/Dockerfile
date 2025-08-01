FROM python:3.13-alpine

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/mqtt-client

# Set the working directory
WORKDIR /mqtt-client

# Install build dependencies including gcc
RUN apk add --no-cache gcc musl-dev libffi-dev

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /mqtt-client/

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /mqtt-client/

# Run the application
CMD ["python", "main.py"]
