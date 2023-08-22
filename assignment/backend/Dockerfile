FROM python:3.9-slim-buster

ENV DATABASE_URL=/app/data/db.sqlite

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y sqlite3 libsqlite3-mod-spatialite gdal-bin python3-gdal curl build-essential libsqlite3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

RUN useradd --create-home appuser
USER appuser

COPY --chown=appuser . .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
