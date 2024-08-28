import random
import string
from typing import List, Dict, Any

from .conftest import client, prepare_database, login_user

def get_random_username(length=5):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_register():
    response = client.post(
        '/register',
        params={
            "username": get_random_username(),
            "password": get_random_password()
        }
    )
    assert response.status_code == 200
    assert response.json() == {"Success": True}


def test_wrong_register():
    wrong_response = client.post(
        '/register',
        params={
            "username": "admin",
            "password": "admin"
        }
    )
    assert wrong_response.status_code == 409
    assert wrong_response.json() == {"detail": "User exists"}


def test_wrong_login(login_user):
    response = client.post(
        '/login',
        params={
            "username": get_random_username(),
            "password": get_random_password()
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_with_wrong_password(login_user):
    response = client.post(
        '/login',
        params={
            "username": "admin",
            "password": get_random_password()
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login():
    response = client.post(
        '/login',
        params={
            "username": "admin",
            "password": "admin"
        }
    )
    assert response.status_code == 200


def test_add_note(login_user):
    response = client.post(
        "note/add",
        params={
            "text": "привет мир"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"Success": True}


def test_add_note_with_mistakes(login_user):
    response = client.post(
        "note/add",
        params={
            "text": "привед мир"
        }
    )
    assert response.status_code == 418

def test_get_user_note(login_user):
    response = client.get(
        "/user/note"
    )
    assert response.status_code == 200
