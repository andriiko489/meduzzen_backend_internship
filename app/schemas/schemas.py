from __future__ import annotations

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class BaseResponse(BaseModel):
    msg: str


class TokenData(BaseModel):
    username: str | None = None
