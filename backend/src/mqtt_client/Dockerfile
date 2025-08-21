FROM python:3.13-alpine

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/mqttclient

# Set the working directory
WORKDIR /mqttclient

# Install build dependencies including gcc and sqlite
RUN apk add --no-cache gcc musl-dev libffi-dev sqlite-dev

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* ./

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./backend/src/mqtt_client .

# Create non-root user
RUN addgroup --system --gid 1001 mqttclientuser
RUN adduser --system --uid 1001 mqttclientuser
RUN chown -R mqttclientuser:mqttclientuser /mqttclient

USER mqttclientuser

# Run the application
CMD ["python", "src/main.py"]
