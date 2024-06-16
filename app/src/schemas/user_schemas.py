from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str


class UserUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    login: str | None
    password: str | None


class UserOut(BaseModel):
    id: int
    login: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
