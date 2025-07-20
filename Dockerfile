FROM python:3.13-alpine
WORKDIR /app

COPY . .

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry install --no-cache --only main

EXPOSE 5000

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--worker-class", "gevent", "--workers", "6"]