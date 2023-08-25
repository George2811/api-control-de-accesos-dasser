from main import app
from fastapi.testclient import TestClient

# pytest test_user.py
client = TestClient(app)

# Test: Comprueba que el endpoint "/users/2" devuelve código 200 y el Usuario correspondiente
def test_get_user_by_id():
    # Arrange
    status = 200
    user = {
        "id": 2,
        "name": "Vamos",
        "last_name": "string",
        "login": "string",
        "status": "string",
        "created_at": "2023-08-22T22:30:46",
        "updated_at": "2023-08-22T23:42:59"
    }

    # Act
    response = client.get("/users/2")

    # Assert
    assert response.status_code == status
    assert response.json() == user

# Test: Comprueba que el endpoint "/users" devuelve código 200 y los usuarios cuentan con los atributos esperados
def test_get_users():
    # Arrange
    status = 200
    expected_keys = ["id", "name", "last_name", "login", "status", "created_at", "updated_at"]

    # Act
    response = client.get("/users")
    users_data = response.json()

    # Assert
    assert response.status_code == status
    for user in users_data:
        assert all(key in user for key in expected_keys)
