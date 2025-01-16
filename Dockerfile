FROM python:3.11-alpine3.16

RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    curl \
    openssl-dev \
    gcc \
    libc-dev \
    bash \
    libpq \
    librdkafka-dev

RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock /src/
WORKDIR /src

RUN pip install --no-cache-dir wheel \
    && pip wheel --no-cache-dir --use-pep517 "aiokafka==0.12.0"

RUN poetry install

COPY ./src /src

EXPOSE 8000

CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload"]
