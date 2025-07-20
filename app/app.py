from flask import Flask
from app.config.config import get_config_by_name
from app.initialize_functions import (
    initialize_middlewares,
    initialize_route,
    initialize_db,
    initialize_storage_service,
    initialize_swagger,
    initilize_logger,
)


def create_app(config=None) -> Flask:
    """
    Create a Flask application.

    Args:
        config: The configuration object to use.

    Returns:
        A Flask application instance.
    """
    app = Flask(__name__)

    config = get_config_by_name(config)
    app.config.from_object(config)

    # Initialize extensions
    initialize_db(app)

    # Register routes
    initialize_route(app)

    # Initialize Swagger
    initialize_swagger(app)

    # Initialize Swagger
    initialize_middlewares(app)

    # Initialize storage service
    initialize_storage_service()

    # Initialize logging
    initilize_logger(config)
    return app
