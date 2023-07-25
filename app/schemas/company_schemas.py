from typing import Optional

from pydantic import BaseModel, ConfigDict


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str


class AddCompany(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
