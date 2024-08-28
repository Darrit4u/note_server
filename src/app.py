from typing import List, Dict, Any
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import requests

from src.db import SUser, SNote
from src.db import JsonDB
from src.jwt_token import create_jwt_token, verify_jwt_token

app = FastAPI()

session_db = JsonDB(user_file_path="users.json", note_file_path="notes.json")


def get_db() -> JsonDB:
    return session_db


# хэширование пароля

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_token(request: Request) -> str:
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    return token


def get_current_user(
    token: str = Depends(get_token), db: JsonDB = Depends(get_db)
) -> SUser:
    payload = verify_jwt_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token is not exist")

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=401, detail="Токен истек")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не найден ID пользователя")

    user = db.get_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# api


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.post("/register")
def register_user(
    username: str, password: str, db: JsonDB = Depends(get_db)
) -> Dict[str, bool]:
    if db.get_user_by_username(username) is not None:
        raise HTTPException(status_code=409, detail="User exists")

    hashed_password = get_password_hash(password)
    db.add_user(username, hashed_password)

    return {"Success": True}


@app.post("/login")
def authenticate_user(
    response: Response, username: str, password: str, db: JsonDB = Depends(get_db)
) -> Dict[str, Any]:
    user = db.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = verify_password(password, user.password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.id})
    response.set_cookie(key="users_access_token", value=jwt_token, httponly=True)
    return {"access_token": jwt_token, "refresh_token": None}


@app.get("/user/note")
def get_user_note(
    cur_user: SUser = Depends(get_current_user), db: JsonDB = Depends(get_db)
) -> List[SNote]:
    return db.get_note_by_id_user(int(cur_user.id))


@app.get("/user/{id_user}")
def get_user(id_user: int, db: JsonDB = Depends(get_db)) -> SUser:
    return db.get_user_by_id(id_user)


@app.post("/note/add")
def add_note(
    text: str, cur_user: SUser = Depends(get_current_user), db: JsonDB = Depends(get_db)
) -> Dict[str, bool]:
    response = requests.get(
        "https://speller.yandex.net/services/spellservice.json/checkText",
        params={"text": text},
        timeout=10,
    )

    if response.json():
        raise HTTPException(status_code=418, detail=response.json())

    id_user = cur_user.id
    db.add_new_note(id_user=id_user, text=text)
    return {"Success": True}


@app.get("/note/{id_note}")
def get_note_by_id(
    id_note: int,
    cur_user: SUser = Depends(get_current_user),
    db: JsonDB = Depends(get_db),
) -> SNote:
    note_data = db.get_note_by_id_note(id_note)
    if cur_user.id != note_data.id_user:
        raise HTTPException(
            status_code=401, detail="You don't have access to this note"
        )
    return note_data
