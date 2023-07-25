from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas import schemas


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    owner: Optional[schemas.User] = None


class AddCompany(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
