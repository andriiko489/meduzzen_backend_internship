from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, model_validator

from crud.BaseCRUD import BaseCRUD
from db import pgdb
from models import models
from schemas.users import User


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    owner: Optional[User] = None


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

    @model_validator(mode='after')
    async def validate_its_owner_of_company(self):
        company = (
            await BaseCRUD(schema=Company, model=models.Company, session=pgdb.session).get(self.id))
        if company is None:
            raise HTTPException(detail="Company with this id doesnt exist", status_code=404)
        if self.owner_id != company.owner_id:
            raise HTTPException(detail="This user not owner of this company", status_code=403)
        return self
