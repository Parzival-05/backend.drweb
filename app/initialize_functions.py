import logging
import os
from flask import Flask
from flasgger import Swagger

from app.api_instance import api
from app.config.config import FILE_STORAGE_PATH, BaseConfig
from app.db.base import db


def initialize_route(app: Flask):
    api.init_app(app)
    from app.modules.user.route import User, Users, ns_users
    from app.modules.files.route import Files, ns_files

    with app.app_context():
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


def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger


def initialize_middlewares(app: Flask):
    with app.app_context():
        from app.middlewares.log import log_request_info, start_timer  # noqa


def initialize_storage_service():
    os.makedirs(FILE_STORAGE_PATH, exist_ok=True)


def initilize_logger(config: BaseConfig):
    log_level = logging.DEBUG if config.DEBUG else logging.INFO
    logging.basicConfig(
        filename=config.LOG_CONFIG.LOG_FILE,
        filemode="a",
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s - %(message)s",
    )
