import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Save and restore the original activities state for isolation
    original = {k: v.copy() for k, v in activities.items()}
    yield
    activities.clear()
    activities.update({k: v.copy() for k, v in original.items()})

client = TestClient(app)

def test_get_activities():
    # Arrange: (nothing extra needed)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"  # Already signed up in initial data
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
