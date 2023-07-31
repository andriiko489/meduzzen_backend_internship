from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, ScalarResult

from crud.BaseCRUD import BaseCRUD
from crud.UserCRUD import user_crud
from db import pgdb
from models import models
from schemas import basic_schemas, invitation_schemas

default_session = pgdb.session


async def invitation_status(invitation, session=default_session):
    if invitation.sender_id == invitation.receiver_id:
        return 0
    sender_owner_of = await user_crud.get_by_owner_of(invitation.sender_id)
    receiver_owner_of = await user_crud.get_by_owner_of(invitation.receiver_id)
    stmt = select(models.Company).where(models.Company.id == invitation.company_id)
    company = (await session.execute(stmt)).scalars().first()  # .
    if company in sender_owner_of:
        if receiver_owner_of:
            return 2
        return 4
    elif company in receiver_owner_of:
        if sender_owner_of:
            return 3
        return 5
    else:
        return 1


invitation_status_dict = {0: "You cannot send invitation to yourself",
                          1: "Between sender and receiver nobody is owner of selected company",
                          2: "Selected receiver user are owner of company",
                          3: "Selected sender user are owner of company",
                          4: "From owner to user",
                          5: "From user to owner"}


class Status:
    success_canceled = "Invitation canceled successful"
    success_declined = "Invitation declined successful"


class InvitationCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Invitation, schema=basic_schemas.Invitation):
        super().__init__(session, model, schema)

    async def get(self, invitation_id: int) -> Optional[models.Invitation]:
        return await super().get(invitation_id)

    async def get_all(self) -> list[models.Invitation]:
        return await super().get_all()

    async def add(self, invitation: invitation_schemas.BasicInvitation):
        status = await invitation_status(invitation)
        if status > 3:
            return await super().add(invitation)
        raise HTTPException(detail=invitation_status_dict[status], status_code=418)

    async def delete(self, invitation_id: int):
        return await super().delete(invitation_id)

    async def cancel(self, invitation_id: int, current_user: basic_schemas.User):
        invitation = await self.get(invitation_id)
        if not invitation:
            raise HTTPException(detail="invitation not exist", status_code=418)
        if invitation.sender_id != current_user.id:
            raise HTTPException(detail="You not not received this invitation", status_code=418)
        else:
            await self.delete(invitation_id)
            return Status.success_canceled

    async def decline(self, invitation_id: int, current_user: basic_schemas.User):
        invitation = await self.get(invitation_id)
        if not invitation:
            raise HTTPException(detail="invitation not exist", status_code=418)
        if invitation.receiver_id != current_user.id:
            raise HTTPException(detail="You not not received this invitation", status_code=418)
        else:
            await self.delete(invitation_id)
            return Status.success_declined

    async def get_sent_invitations(self, user_id):
        stmt = select(models.Invitation).where(models.Invitation.sender_id == user_id)
        item = (await self.session.execute(stmt)).scalars().all()
        return item

    async def get_received_invitations(self, user_id):
        stmt = select(models.Invitation).where(models.Invitation.receiver_id == user_id)
        item = (await self.session.execute(stmt)).scalars().all()
        return item

    async def accept_invitation(self, invitation_id: int):
        invitation = await super().get(invitation_id)
        status = await invitation_status(await self.get(invitation_id))
        if status == 4:
            stmt = select(models.User).where(models.User.id == invitation.receiver_id)
        else:
            stmt = select(models.User).where(models.User.id == invitation.sender_id)
        db_user = (await self.session.execute(stmt)).scalars().first()
        db_user.company_id = invitation.company_id
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        await self.delete(invitation_id)
        return db_user


invitation_crud = InvitationCRUD()
