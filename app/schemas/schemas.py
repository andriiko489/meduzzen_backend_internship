from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    email: str
    is_active: bool


class SignInUser(BaseModel):
    username: str
    password: str


class SignUpUser(User):
    pass


class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserList(BaseModel):
    pass


class UserDetail(BaseModel):
    username: str
