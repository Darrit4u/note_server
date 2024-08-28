from typing import List, Dict, Optional, Any
import json
from pydantic import BaseModel
from fastapi import HTTPException


class SUser(BaseModel):
    id: int
    username: str
    password: str


class SNote(BaseModel):
    id: int
    id_user: int
    text: str


class JsonDB:
    def __init__(self, user_file_path: str, note_file_path: str):
        self.user_file_path = user_file_path
        self.note_file_path = note_file_path

    @staticmethod
    def read_from_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def find_records_by_key(file_path: str, key, value):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
            return [record for record in data if record.get(key) == value]

    def add_records(self, file_path: str, new_data: Dict[str, Any]):
        data = self.read_from_file(file_path)
        data.append(new_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def dict_to_SUser(user_data: dict) -> SUser:
        return SUser(
            id=user_data["id"],
            username=user_data["username"],
            password=user_data["password"],
        )

    @staticmethod
    def dict_to_SNote(note_data: dict) -> SNote:
        return SNote(
            id=note_data["id"], id_user=note_data["id_user"], text=note_data["text"]
        )

    def get_users(self) -> Optional[List[Dict[str, Any]]]:
        return self.read_from_file(self.user_file_path)

    def get_user_by_id(self, id_user: int) -> Optional[SUser]:
        user_data = self.find_records_by_key(self.user_file_path, "id", id_user)
        if len(user_data) > 1:
            raise HTTPException(
                status_code=400, detail="More than one user with this id!"
            )
        if len(user_data) == 0:
            return None
        return self.dict_to_SUser(user_data[0])

    def get_user_by_username(self, username: str) -> Optional[SUser]:
        user_data = self.find_records_by_key(self.user_file_path, "username", username)
        if len(user_data) > 1:
            raise HTTPException(
                status_code=400, detail="More than one user with this username!"
            )
        if len(user_data) == 0:
            return None
        return self.dict_to_SUser(user_data[0])

    def get_last_id_user(self) -> int:
        data = self.read_from_file(self.user_file_path)
        if len(data) > 0:
            return data[-1]["id"]
        return 0

    def add_user(self, name: str, password: str) -> bool:
        id_user = self.get_last_id_user() + 1
        user = SUser(id=id_user, username=name, password=password)
        self.add_records(self.user_file_path, user.model_dump())
        return True

    def get_notes(self) -> Optional[List[Dict[str, Any]]]:
        return self.read_from_file(self.note_file_path)

    def get_note_by_id_note(self, id_note: int) -> SNote:
        note_data = self.find_records_by_key(self.note_file_path, "id", id_note)
        return self.dict_to_SNote(note_data[0])

    def get_note_by_id_user(self, id_user: int) -> List[SNote]:
        notes_data = self.find_records_by_key(self.note_file_path, "id_user", id_user)
        return [self.dict_to_SNote(x) for x in notes_data]

    def get_last_note_id(self) -> int:
        data = self.read_from_file(self.note_file_path)
        if len(data) > 0:
            return int(data[-1]["id"])
        return 0

    def add_new_note(self, id_user: int, text: str) -> bool:
        id_note = self.get_last_note_id() + 1
        data = SNote(id=id_note, id_user=id_user, text=text)
        self.add_records(self.note_file_path, data.model_dump())
        return True
