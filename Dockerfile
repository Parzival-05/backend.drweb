FROM python:3.13-alpine
WORKDIR /app

COPY . .

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry install --no-cache --only main

ENV APP_PORT=5000
ENV FLASK_APP wsgi.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]