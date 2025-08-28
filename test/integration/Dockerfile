FROM python:3.13-alpine

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/mqttclient

# Set the working directory
WORKDIR /test

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock* ./
# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --with test --no-interaction --no-ansi --no-root



COPY ./test/ ./test
RUN chmod +x ./test/integration/entrypoint.sh
ENTRYPOINT ["./test/integration/entrypoint.sh"]
