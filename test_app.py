import pytest
from app import app, db


@pytest.fixture
# pylint: disable=redefined-outer-name
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    response = client.post("/lessons/add", data={
        "teacher": "Mr. Smith",
        "academic_group": "Test Group",
        "subject": "Math",
        "day": "Monday",
        "class_order": "1"
    })
    assert response.status_code == 201


def test_get_lessons(client):
    response = client.get("/lessons")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_delete_lesson(client):
    client.post("/lessons/add", data={
        "teacher": "Mr. Smith",
        "academic_group": "Test Group",
        "subject": "Math",
        "day": "Monday",
        "class_order": "1"
    })
    response = client.delete("/lessons/delete/1")
    assert response.status_code == 200


def test_edit_lesson(client):
    client.post("/lessons/add", data={
        "teacher": "Mr. Smith",
        "academic_group": "Test Group",
        "subject": "Math",
        "day": "Monday",
        "class_order": "1"
    })
    response = client.put("/lessons/edit/1", data={
        "teacher": "Dr. Brown",
        "academic_group": "Test Group",
        "subject": "Physics",
        "day": "Tuesday",
        "class_order": "2"
    })
    assert response.status_code == 200


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


def test_add_lesson_missing_fields(client):
    response = client.post("/lessons/add", data={
        "teacher": "Mr. Smith",
    })
    assert response.status_code == 400


def test_get_non_existent_lesson(client):
    response = client.get("/lessons/teacher/NonExistentTeacher")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0
