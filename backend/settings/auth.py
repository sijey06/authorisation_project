from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


def verify_password(plain_password, hashed_password):
    """Проверяет совпадение обычного пароля с его захешированным значением."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Хеширует переданный пароль с использованием алгоритма bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: Dict,
                        expires_delta: timedelta = timedelta(minutes=30)):
    """Создает JWT-токен доступа на основе заданных данных."""
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    """Декодирует JWT-токен обратно в словарь с данными."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
