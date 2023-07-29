from typing import Optional

from crud.BaseCRUD import BaseCRUD
from crud.CompanyCRUD import default_session
from models import models
from schemas import basic_schemas


class OwnerCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Owner, schema=basic_schemas.Owner):
        super().__init__(session, model, schema)

    async def get_all(self) -> list[models.Owner]:
        return await super().get_all()

    async def add(self, owner: basic_schemas.Owner) -> Optional[models.Owner]:
        return await super().add(owner)


owner_crud = OwnerCRUD()
