from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from models import models


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    username: str
    hashed_password: str
    email: str
    is_active: bool
    company_id: Optional[int] = None


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    owner_id: int


class Invitation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    sender_id: Optional[int] = None
    receiver_id: int
    company_id: int


class Admin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    company_id: int
    user_id: int


class BasicAdmin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    company_id: int
    user_id: int
