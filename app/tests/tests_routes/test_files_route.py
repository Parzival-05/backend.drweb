import os
import base64
import pytest
from io import BytesIO
from app.modules.files.service import StorageService


def delete_file(client_file_owner, file_hash):
    if os.path.exists(StorageService.file_path(file_hash)):
        response = client_file_owner.delete("/api/files/", json={"file_hash": file_hash})
        print(response.json)
        assert response.status_code == 200


@pytest.fixture
def uploaded_file(auth_client):
    response = auth_client.post(
        "/api/files/",
        data={"file": (BytesIO(b"Test file content"), "test.txt")},
        content_type="multipart/form-data",
    )
    file_hash = response.json["file_hash"]
    yield file_hash
    delete_file(auth_client, file_hash)


def test_file_upload(auth_client):
    response = auth_client.post(
        "/api/files/",
        data={"file": (BytesIO(b"Hello World"), "hello.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert "file_hash" in response.json
    file_hash = response.json["file_hash"]
    assert len(file_hash) == 64

    file_path = StorageService.file_path(response.json["file_hash"])
    assert os.path.exists(file_path)
    delete_file(auth_client, file_hash)


def test_file_download(client, uploaded_file):
    response = client.get(f"/api/files/?file_hash={uploaded_file}")

    assert response.status_code == 200
    assert response.data == b"Test file content"
    assert "attachment" in response.headers["Content-Disposition"]
    assert "test.txt" in response.headers["Content-Disposition"]


def test_file_delete(auth_client, uploaded_file):
    response = auth_client.delete("/api/files/", json={"file_hash": uploaded_file})
    assert response.status_code == 200

    response = auth_client.get(f"/api/files/?file_hash={uploaded_file}")
    assert response.status_code == 400
    assert "File not found" in response.json["message"]

    file_path = StorageService.file_path(uploaded_file)
    assert not os.path.exists(file_path)


def test_unauthorized_upload(client):
    response = client.post(
        "/api/files/",
        data={"file": (BytesIO(b"Unauthorized"), "unauth.txt")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 401


def test_unauthorized_delete(client, uploaded_file):
    response = client.delete("/api/files/", json={"file_hash": uploaded_file})

    assert response.status_code == 401


def test_delete_another_user_file(client, uploaded_file):
    another_client_email = "another@example.com"
    another_client_password = "password456"
    client.post(
        "/api/users/",
        json={"email": another_client_email, "password": another_client_password},
    )

    creds = base64.b64encode(
        f"{another_client_email}:{another_client_password}".encode("utf-8")
    ).decode("utf-8")
    client.environ_base["HTTP_AUTHORIZATION"] = f"Basic {creds}"

    response = client.delete("/api/files/", json={"file_hash": uploaded_file})

    assert response.status_code == 400
    assert "File ownership error" in response.json["message"]


def test_download_nonexistent_file(client):
    response = client.get("/api/files/?file_hash=ubercapitalistdeathtrade")

    assert response.status_code == 400
    assert "File not found" in response.json["message"]
