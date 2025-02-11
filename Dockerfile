FROM python:3.9.13-alpine

EXPOSE 8080

WORKDIR /code

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY . /code

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --without test

CMD ["poetry", "run", "uvicorn", "fastapi_tema.aplication.main:app", "--host", "localhost", "--port", "8000"]
