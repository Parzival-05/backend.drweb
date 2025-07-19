# backend.drweb
## Хранилище файлов с доступом по http

### Описание

Реализовать сервис, который предоставит HTTP API для загрузки (upload), скачивания (download) и удаления файлов.

Upload:
1. авторизованный пользователь загружает файл;
2. файл сохранятеся на диск в следующую структуру каталогов:
   - store/ab/abcdef12345..., где "abcdef12345..." - имя файла, совпадающее с его хэшем.
   - /ab/ - подкаталог, состоящий из первых двух символов хэша файла.
3. Алгоритм хэширования - на ваш выбор.
4. возвращает хэш загруженного файла;

Delete:
1. авторизованный пользователь передает хэш файла, который необходимо удалить;
2. если по хешу файл удалось найти в локальном хранилище, и файл принадлежит пользователю, то файл пользователя удаляется;

Download:
1. любой пользователь передаёт параметр - хэш файла;
2. если по хешу файл удалось найти в локальном хранилище, то возвращаем файл;

Тип авторизации пользователей: Basic. 
- Регистрация пользователей в сервисе не предусморена.

Основные требования:
- Python 3.x;
- Flask (желательно), aiohttp (только если был реальный опыт использования);

Результат работы должен быть в виде ссылки на git репозиторий с исходным кодом выполненного ТЗ.


### Run

```
docker compose up --watch --remove-orphans
```
Open via your browser:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
## For devs

### Install

1. Clone
    ```
    git clone https://github.com/Parzival-05/backend_drweb
    ```
2. Setup environment:
   ```
   pip install poetry
   poetry install
   ```
3. Run (don't forget to fil the .env file):
   ```
   poetry run python run.py
   ```

### .env file example

```
# App
FLASK_APP=run.py
FLASK_ENV=development 
# testing, development

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin

# Log
LOG_FILE=app.log
```