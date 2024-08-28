from typing import List, Dict, Optional, Any
import json
from pydantic import BaseModel
from fastapi import HTTPException


USER_FILE_PATH = "users.json"
NOTE_FILE_PATH = "notes.json"


def read_from_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def find_records_by_key(file_path: str, key, value):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
        return [record for record in data if record.get(key) == value]


def add_records(file_path: str, new_data: Dict[str, Any]):
    data = read_from_file(file_path)
    data.append(new_data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class SUser(BaseModel):
    id: int
    username: str
    password: str


class SNote(BaseModel):
    id: int
    id_user: int
    text: str


def dict_to_SUser(user_data: dict) -> SUser:
    return SUser(
        id=user_data["id"],
        username=user_data["username"],
        password=user_data["password"],
    )


def dict_to_SNote(note_data: dict) -> SNote:
    return SNote(
        id=note_data["id"], id_user=note_data["id_user"], text=note_data["text"]
    )


def get_users() -> List[Dict[str, Any]]:
    return read_from_file(USER_FILE_PATH)


def get_user_by_id(id_user: int) -> Optional[SUser]:
    user_data = find_records_by_key(USER_FILE_PATH, "id", id_user)
    if len(user_data) > 1:
        raise HTTPException(status_code=400, detail="More than one user with this id!")
    if len(user_data) == 0:
        return None
    return dict_to_SUser(user_data[0])


def get_user_by_username(username: str) -> Optional[SUser]:
    user_data = find_records_by_key(USER_FILE_PATH, "username", username)
    if len(user_data) > 1:
        raise HTTPException(
            status_code=400, detail="More than one user with this username!"
        )
    if len(user_data) == 0:
        return None
    return dict_to_SUser(user_data[0])


def get_last_id_user() -> int:
    data = read_from_file(USER_FILE_PATH)
    if len(data) > 0:
        return data[-1]["id"]
    return 0


def add_user(name: str, password: str) -> bool:
    id_user = get_last_id_user() + 1
    user = SUser(id=id_user, username=name, password=password)
    add_records(USER_FILE_PATH, user.model_dump())
    return True


def get_notes():
    return read_from_file(NOTE_FILE_PATH)


def get_note_by_id_note(id_note: int) -> SNote:
    note_data = find_records_by_key(NOTE_FILE_PATH, "id", id_note)
    return dict_to_SNote(note_data[0])


def get_note_by_id_user(id_user: int) -> List[SNote]:
    notes_data = find_records_by_key(NOTE_FILE_PATH, "id_user", id_user)
    return [dict_to_SNote(x) for x in notes_data]


def get_last_note_id() -> int:
    data = read_from_file(NOTE_FILE_PATH)
    if len(data) > 0:
        return int(data[-1]["id"])
    return 0


def add_new_note(id_user: int, text: str) -> bool:
    id_note = get_last_note_id() + 1
    data = SNote(id=id_note, id_user=id_user, text=text)
    add_records(NOTE_FILE_PATH, data.model_dump())
    return True
