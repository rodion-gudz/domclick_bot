FROM python:3.10-slim-bullseye as builder
WORKDIR /src
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry==1.3.0
COPY pyproject.toml poetry.lock /src/
RUN poetry config virtualenvs.create true && poetry config virtualenvs.in-project true
RUN poetry install --only main --no-interaction --no-root

FROM python:3.10-slim-bullseye
WORKDIR /src

COPY --from=builder /src /src
COPY . /src/

EXPOSE 8080
ENV PATH="/src/.venv/bin/:$PATH"
CMD ["python", "-m", "app"]
