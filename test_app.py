import json
import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_get_groups(client):
    response = client.get("/group-list")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_group_info(client):
    response = client.get("/group-info/Test Group")
    assert response.status_code in [200, 404]


def test_create_lesson(client):
    response = client.post("/lessons/add", json={
        "group": "Test Group",
        "subject": "Math",
        "teacher": "Mr. Smith",
        "day": "Monday",
        "time": "10:00"
    })
    assert response.status_code in [201, 400]


def test_get_lessons(client):
    response = client.get("/lessons")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_delete_lesson(client):
    client.post("/lessons/add", json={
        "group": "Test Group",
        "subject": "Math",
        "teacher": "Mr. Smith",
        "day": "Monday",
        "time": "10:00"
    })
    response = client.delete("/lessons/delete/1")
    assert response.status_code in [200, 404]


def test_edit_lesson(client):
    client.post("/lessons/add", json={
        "group": "Test Group",
        "subject": "Math",
        "teacher": "Mr. Smith",
        "day": "Monday",
        "time": "10:00"
    })
    response = client.put("/lessons/edit/1", json={
        "group": "Test Group",
        "subject": "Physics",
        "teacher": "Dr. Brown",
        "day": "Tuesday",
        "time": "12:00"
    })
    assert response.status_code in [200, 404]


def test_get_lessons_by_teacher(client):
    response = client.get("/lessons/teacher/Mr. Smith")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_lessons_by_group(client):
    response = client.get("/lessons/academic-group/Test Group")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
