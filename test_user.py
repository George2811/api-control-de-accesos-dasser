from main import app
from fastapi.testclient import TestClient

# pytest test_user.py
client = TestClient(app)

# Test: Comprueba que el endpoint "/users/1" devuelve código 200 y el Usuario correspondiente
def test_get_user_by_id():
    # Arrange
    status = 200
    user = {
        "id": 1,
        "name": "Manuel",
        "last_name": "Ramírez",
        "login": "Manu75",
        "status": "Activo",
        "created_at": "2023-08-22T22:30:46",
        "updated_at": "2023-08-24T21:52:41"
    }

    # Act
    response = client.get("/users/1")

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
