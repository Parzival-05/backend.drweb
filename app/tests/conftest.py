import pytest
from unittest.mock import patch

from app.app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_user_model():
    with patch("app.modules.user.route.UserModel") as mock:
        yield mock


@pytest.fixture
def mock_db():
    with patch("app.modules.user.route.db") as mock:
        yield mock
