from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from models.token import ActiveToken
from models.user import User
from schemas.user import UserCreate
from settings.auth import (create_access_token, decode_token,
                           get_password_hash, oauth2_scheme, verify_password)
from settings.config import ACCESS_TOKEN_EXPIRE_MINUTES
from settings.database import get_db

router = APIRouter()


@router.post('/register', summary='Регистрация', tags=['Auth'])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Регистрация нового пользователя.

    #### Входящие данные:
    - `username`: Логин пользователя.
    - `password`: Пароль пользователя.

    #### Ответ:
    Сообщение о успешном создании пользователя либо ошибка,
    если пользователь уже существует или пароль некорректной длины.
    """
    existing_user = db.query(User).filter(
        User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400,
                            detail='Пользователь уже существует.')
    new_user = User(username=user.username,
                    hashed_password=get_password_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'Пользователь успешно создан'}


@router.post('/login', summary='Авторизация', tags=['Auth'])
async def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Получение JWT-токена при успешной авторизации.

    #### Входящие данные:
    - `username`: Логин пользователя.
    - `password`: Пароль пользователя.

    #### Ответ:
    Токен доступа (`access_token`) и тип токена (`Bearer`).
    """
    found_user = db.query(User).filter(User.username == user.username).first()
    if not found_user or not verify_password(user.password,
                                             found_user.hashed_password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                            detail='Неверные учетные данные')

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {'sub': found_user.username}, expires_delta=access_token_expires)
    active_token = ActiveToken(token_value=access_token, user_id=found_user.id)
    db.add(active_token)
    db.commit()

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.get('/me', summary='Проверка профиля пользователя', tags=['Auth'])
async def check_token(current_user=Depends(oauth2_scheme),
                      db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Проверка действительности текущего токена и получение
    информации о профиле пользователя.

    #### Входящие данные:
    - `current_user`: Токен аутентификации, полученный ранее при входе.

    #### Ответ:
    Если токен действителен, возвращает объект с информацией
    о пользователе и признаке действительности токена.
    """
    try:
        decoded_token = decode_token(current_user)
        user_login = decoded_token['sub']
        user = db.query(User).filter(User.username == user_login).first()
        active_token = db.query(ActiveToken).filter_by(
            token_value=current_user).first()
        if not active_token:
            raise HTTPException(status_code=401, detail='Токен не валиден.')

        return {"isValid": True, "username": user.username}
    except Exception as err:
        raise HTTPException(status_code=401, detail=str(err))


@router.post('/logout', summary='Выход', tags=['Auth'])
async def logout(current_user=Depends(oauth2_scheme),
                 db: Session = Depends(get_db)):
    """
    ### Цель метода:
    Осуществление выхода пользователя из системы путем
    удаления активного токена.

    #### Входящие данные:
    - `current_user`: Токен аутентификации, полученный ранее при входе.

    #### Ответ:
    Подтверждение успешного выхода из системы или
    сообщение об ошибке, если токен не найден.
    """
    try:
        active_token = db.query(ActiveToken).filter_by(
            token_value=current_user).first()
        if active_token:
            db.delete(active_token)
            db.commit()
            return {'message': 'Вы успешно вышли.'}
        else:
            raise HTTPException(status_code=401, detail='Токен не найден.')
    except Exception as err:
        raise HTTPException(status_code=401, detail=str(err))
