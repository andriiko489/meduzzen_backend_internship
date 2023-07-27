from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    id: Optional[int] = None
    username: str
    hashed_password: str
    email: str
    is_active: bool


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    owner: Optional[User] = None
