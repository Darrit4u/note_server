from fastapi import FastAPI
from pydantic import BaseModel
from json_db_lite import JSONDatabase

# инициализация объекта
user_db = JSONDatabase(file_path='users.json')
note_db = JSONDatabase(file_path='notes.json')

app = FastAPI()

def get_users():
    return user_db.get_all_records()


def add_user(user: dict):
    user_db.add_records(user)
    return True


def get_notes():
    return note_db.get_all_records()


def add_note(data: dict):
    note_db.add_records(data)
    return True


class User(BaseModel):
    id: int
    name: str
    password: str


class Note(BaseModel):
    id: int
    id_user: int
    text: str


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/register")
def register():
    pass

@app.post("/auth")
def auth():
    pass

@app.get("/user/{id_user}")
def get_user(id_user: int):
    pass

@app.get("/user/{id_user}/note")
def get_note_by_user_id(id_user: int):
    pass

@app.get("/note/{id_note}")
def get_note_by_id(id_note: int):
    pass

@app.post("/note/add")
def add_note(text: str):
    pass
