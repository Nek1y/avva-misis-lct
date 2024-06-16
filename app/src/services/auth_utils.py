from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

import src.params.auth as auth
import src.database.user_db as db
from ..database.models.models import User
from ..schemas.user_schemas import Token, TokenData


def hash_password(password: str) -> str:
    return auth.pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return auth.pwd_context.verify(plain_password, hashed_password)


async def reg_user(login: str, password: str):
    pass_hash = hash_password(password)
    new_user = await db.reg_user(login, pass_hash)

    return new_user


async def auth_user(login: str, password: str) -> User:
    user = await db.get_user_by_login(login)
    if not user:
        raise HTTPException(
            detail='login dont exist',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            detail='password is incorrect',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return user


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=10080)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        auth.SECRET_KEY,
        algorithm=auth.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        id = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(auth.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'}
    )

    token = verify_access_token(token, credentials_exception)

    user = await db.get_user_by_id(token.id)

    return user
