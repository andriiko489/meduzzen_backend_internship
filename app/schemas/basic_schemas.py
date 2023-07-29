from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    id: Optional[int] = None
    username: str
    hashed_password: str
    email: str
    is_active: bool
    company: Optional["Company"] = None
    owner_model: Optional["Owner"] = None


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

    owner: "Owner" = None


class Owner(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    user: Optional["User"] = None
    company: Optional[List["Company"]] = []
