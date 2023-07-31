from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db import pgdb
from models import models
from schemas import basic_schemas, invitation_schemas
from services.auth import Auth

default_session = pgdb.session


async def invitation_status(invitation):
    if invitation.sender_id == invitation.receiver_id:
        return 0
    sender_role = await Auth.get_role(invitation.sender_id, invitation.company_id)
    receiver_role = await Auth.get_role(invitation.receiver_id, invitation.company_id)
    if sender_role == -1:
        return 6
    if receiver_role == -1:
        return 7
    if sender_role == 0:
        if receiver_role > 1:
            return 5
        return 2
    elif receiver_role == 0:
        if sender_role > 1:
            return 4
        return 3
    else:
        return 1


invitation_status_dict = {0: "You cannot send invitation to yourself",
                          1: "Between sender and receiver both have company",
                          2: "Receiver cannot answer to this invitation",
                          3: "You cannot send this invitation",
                          4: "From owner to user",
                          5: "From user to owner",
                          6: "Sender have another company",
                          7: "Receiver have another company"}


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
        if status in [4, 5]:
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
