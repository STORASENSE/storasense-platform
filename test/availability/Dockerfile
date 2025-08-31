FROM python:3.13-slim

ENV POETRY_VERSION=1.8.3
ENV PYTHONPATH=/test
# Set the working directory
WORKDIR /test

RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver \
    gcc musl-dev libffi-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"
# Fix missing /dev/ptmx
RUN ln -sf /dev/pts/ptmx /dev/ptmx

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* ./

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --with test --no-interaction --no-ansi --no-root

COPY ./test/ ./test

CMD ["python", "./test/availability/main.py"]
