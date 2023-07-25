from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from crud.BaseCRUD import BaseCRUD
from db.connect_to_pgdb import engine
from schemas import models, company_schemas

default_session = AsyncSession(engine)


class CompanyCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Company, schema=company_schemas.Company):
        super().__init__(session, model, schema)

    async def get_company(self, company_id: int) -> Optional[models.Company]:
        return await super().get(company_id)

    async def get_companies(self) -> list[models.Company]:
        return await super().get_all()

    async def add(self, company: company_schemas.Company) -> Optional[models.Company]:
        return await super().add(company)


company_crud = CompanyCRUD()
