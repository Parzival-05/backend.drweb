from unittest.mock import MagicMock


def test_get_users_returns_list(client, mock_user_model):
    user1 = MagicMock(id=1, email="user1@example.com")
    user2 = MagicMock(id=2, email="user2@example.com")
    mock_user_model.query.all.return_value = [user1, user2]

    resp = client.get("/api/users/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert data[0]["id"] == 1
    assert data[0]["email"] == "user1@example.com"
    assert data[1]["id"] == 2


def test_post_user_creates_user(client, mock_user_model, mock_db):
    mock_user_model.query.filter_by.return_value.first.return_value = None
    user_instance = MagicMock(id=1, email="new@example.com")
    mock_user_model.return_value = user_instance

    resp = client.post(
        "/api/users/",
        json={"email": "new@example.com", "password": "secret"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    user_instance.hash_password.assert_called_once_with("secret")
    mock_db.session.add.assert_called_once_with(user_instance)
    mock_db.session.commit.assert_called_once()


def test_post_user_already_exists(client, mock_user_model):
    mock_user_model.query.filter_by.return_value.first.return_value = MagicMock()

    resp = client.post(
        "/api/users/",
        json={"email": "exists@example.com", "password": "secret"},
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert "User already exists" in data["message"]


def test_get_user_by_id_found(client, mock_user_model):
    user = MagicMock(id=5, email="found@example.com")
    mock_user_model.query.get.return_value = user

    resp = client.get("/api/users/5")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 5
    assert data["email"] == "found@example.com"


def test_get_user_by_id_not_found(client, mock_user_model):
    mock_user_model.query.get.return_value = None

    resp = client.get("/api/users/999")
    assert resp.status_code == 400
    data = resp.get_json()
    assert "not found" in data["message"]
