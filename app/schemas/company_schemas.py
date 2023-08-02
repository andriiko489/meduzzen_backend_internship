from typing import Optional

from pydantic import BaseModel, ConfigDict


class AddCompany(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: Optional[str] = None


class RequestUpdateCompany(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None


class UpdateCompany(RequestUpdateCompany):
    owner_id: Optional[int] = None
