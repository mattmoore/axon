FROM python:3.13

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --root-user-action=ignore --upgrade pip \
 && pip install --root-user-action=ignore poetry

RUN poetry lock \
 && poetry install --no-root

COPY . /app

RUN poetry lock && poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "axon.server:run", "--host", "0.0.0.0", "--port", "8000"]
