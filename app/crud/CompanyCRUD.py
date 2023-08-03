from typing import Optional

from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db import pgdb
from models import models
from schemas import company_schemas, basic_schemas

default_session = pgdb.session


class CompanyCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Company, schema=basic_schemas.Company):
        super().__init__(session, model, schema)

    async def get_company(self, company_id: int) -> Optional[models.Company]:
        return await super().get(company_id)

    async def get_companies(self) -> list[models.Company]:
        return await super().get_all()

    async def get_members(self, company_id: int):
        stmt = select(models.User).where(models.User.company_id == company_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items

    async def get_quizzes(self, company_id: int):
        stmt = select(models.Quiz).where(models.Quiz.company_id == company_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items

    async def get_admins(self, company_id: int):
        stmt = select(models.Admin).where(models.Admin.company_id == company_id)
        items = (await self.session.execute(stmt)).scalars().all()
        print(items)
        return items

    async def add(self, company: basic_schemas.Company) -> Optional[models.Company]:
        return await super().add(company)

    async def update(self, company: company_schemas.UpdateCompany) -> Optional[models.Company]:
        self.schema = company_schemas.UpdateCompany
        await super().update(company)
        return await self.get(company.id)

    async def delete(self, company_id: int) -> Optional[models.Company]:
        return await super().delete(company_id)


company_crud = CompanyCRUD()
