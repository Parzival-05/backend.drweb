import logging
import os
from flask import Flask
from flasgger import Swagger
from flask_compress import Compress
from sqlalchemy import text

from app.api_instance import api
from app.config.config import FILE_STORAGE_PATH, TEMP_FILE_STORAGE_PATH, BaseConfig
from app.db.base import db
from app.db.user import UserModel


def initialize_route(app: Flask):
    api.init_app(app)
    from app.modules.user.route import User, Users, ns_users
    from app.modules.files.route import Files, ns_files

    with app.app_context():
        # Compress responses
        Compress(app)

        # Users
        ns_users.add_resource(Users, "/")
        ns_users.add_resource(User, "/<int:user_id>")
        api.add_namespace(ns_users)

        # Files
        ns_files.add_resource(Files, "/")
        api.add_namespace(ns_files)


def initialize_db(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # add admin user if not exists
        admin = UserModel(email=os.environ.get("ADMIN_EMAIL"))  # type: ignore
        admin.hash_password(
            os.environ.get("ADMIN_PASSWORD")
        )  # obviously not secure, just for demo purposes
        db.session.execute(
            text(
                f"""INSERT INTO "user" (email, password) VALUES ('{admin.email}', '{admin.password}') ON CONFLICT DO NOTHING;"""
            )
        )
        db.session.commit()

    @app.teardown_appcontext
    def cleanup(exception=None):
        if exception:
            try:
                db.session.rollback()
            except Exception as e:
                logging.error("[DB ROLLBACK ERROR] %s", e)
        db.session.remove()


def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger


def initialize_middlewares(app: Flask):
    with app.app_context():
        from app.middlewares.log import log_request_info, start_timer  # noqa


def initialize_storage_service():
    os.makedirs(FILE_STORAGE_PATH, exist_ok=True)
    os.makedirs(TEMP_FILE_STORAGE_PATH, exist_ok=True)


def initilize_logger(config: BaseConfig):
    log_level = logging.DEBUG if config.DEBUG else logging.INFO
    logging.basicConfig(
        filename=config.LOG_CONFIG.LOG_FILE,
        filemode="a",
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s - %(message)s",
    )
