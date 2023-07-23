from __future__ import annotations

from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, field_validator


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    hashed_password: str
    email: str
    is_active: bool


class DbUser(User):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class BaseResponse(BaseModel):
    msg: str
    status_code: int


class UserResponse(BaseResponse):
    user: Optional[User] = None


class DbUserResponse(UserResponse):
    id: int


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

    @field_validator("email")
    def validate_email_no_changed(cls, value):
        if not value is None:
            raise HTTPException(detail="User cannot change email", status_code=404)
        return value


class UserList(BaseModel):
    pass


class UserDetail(BaseModel):
    username: str


class TokenData(BaseModel):
    username: str | None = None
