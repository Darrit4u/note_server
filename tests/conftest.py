import pytest
from fastapi.testclient import TestClient
import json
from src.app import app, get_db
from src.app import get_password_hash
from src.db import JsonDB

test_session_db = JsonDB(
    user_file_path="tests/test_db/users.json",
    note_file_path="tests/test_db/notes.json",
)


def override_get_db():
    return test_session_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    with open("tests/test_db/users.json", "w") as file:
        json.dump(
            [{"id": 1, "username": "admin", "password": get_password_hash("admin")}],
            file,
        )

    open("tests/test_db/notes.json", "w").close()


@pytest.fixture(autouse=True, scope="session")
def login_user():
    client.post("/login", params={"username": "admin", "password": "admin"})
