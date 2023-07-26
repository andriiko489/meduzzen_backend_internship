from typing import Optional

from crud.BaseCRUD import BaseCRUD
from db import pgdb
from schemas import models, schemas

default_session = pgdb.session


class CompanyCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Company, schema=schemas.Company):
        super().__init__(session, model, schema)

    async def get_company(self, company_id: int) -> Optional[models.Company]:
        return await super().get(company_id)

    async def get_companies(self) -> list[models.Company]:
        return await super().get_all()

    async def add(self, company: schemas.Company) -> Optional[models.Company]:
        return await super().add(company)

    async def update(self, company: schemas.UpdateCompany) -> Optional[models.Company]:
        self.schema = schemas.UpdateCompany
        await super().update(company)
        return await self.get(company.id)


company_crud = CompanyCRUD()
