from datetime import datetime, timedelta
import jwt

SECRET_KEY = "f8c27ae8e5b853b25f59eff3929b6ef57b7b3610f3f4fb1e990b27e42dc38422"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(days=30)


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str) -> str:
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError as e:
        print(e)
