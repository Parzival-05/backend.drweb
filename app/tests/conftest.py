import base64
import os
from dotenv import load_dotenv
import pytest
from unittest.mock import patch

from app.app import create_app

load_dotenv()
os.environ["FLASK_ENV"] = "testing"


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


@pytest.fixture
def admin_client(app):
    client = app.test_client()
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    creds = base64.b64encode(f"{admin_email}:{admin_password}".encode()).decode()
    client.environ_base["HTTP_AUTHORIZATION"] = f"Basic {creds}"
    return client


@pytest.fixture
def auth_client(app):
    client = app.test_client()
    client.post(
        "/api/users/", json={"email": "test@example.com", "password": "password123"}
    )
    creds = base64.b64encode(b"test@example.com:password123").decode()
    client.environ_base["HTTP_AUTHORIZATION"] = f"Basic {creds}"
    return client
