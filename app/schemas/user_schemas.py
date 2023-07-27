from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, ConfigDict, EmailStr

from schemas.basic_schemas import User


class AddUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    hashed_password: str
    email: EmailStr
    is_active: bool


class UserResponse(BaseModel):
    msg: str
    user: Optional[User] = None


class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("email")
    def validate_email_no_changed(cls, value):
        if not value is None:
            raise HTTPException(detail="User cannot change email", status_code=403)
        return value
