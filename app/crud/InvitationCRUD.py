from enum import Enum
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from crud.UserCRUD import UserCRUD
from db import pgdb
from models import models

default_session = pgdb.session


async def invitation_status(invitation, session=default_session):
    if invitation.sender_id == invitation.receiver_id:
        return InvitationStatus.CANNOT_SEND_TO_YOURSELF
    user_crud = UserCRUD(session)
    sender_role = await user_crud.get_role(invitation.sender_id, invitation.company_id)
    receiver_role = await user_crud.get_role(invitation.receiver_id, invitation.company_id)
    if receiver_role is None or sender_role is None:
        return InvitationStatus.NOT_FOUND
    if sender_role == -1:
        return InvitationStatus.SENDER_ANOTHER_COMPANY
    if receiver_role == -1:
        return InvitationStatus.RECEIVER_ANOTHER_COMPANY
    if sender_role == 0:
        if receiver_role > 1:
            return InvitationStatus.TO_OWNER
        return InvitationStatus.RECEIVER_CANNOT_ANSWER
    elif receiver_role == 0:
        if sender_role > 1:
            return InvitationStatus.TO_USER
        return InvitationStatus.YOU_CANNOT_SEND
    else:
        return InvitationStatus.BOTH_HAVE_COMPANIES


class InvitationStatus(Enum):
    CANNOT_SEND_TO_YOURSELF = "You cannot send invitation to yourself"
    BOTH_HAVE_COMPANIES = "Between sender and receiver both have company"
    RECEIVER_CANNOT_ANSWER = "Receiver cannot answer to this invitation"
    YOU_CANNOT_SEND = "You cannot send this invitation"
    TO_USER = "From owner to user"
    TO_OWNER = "From user to owner"
    SENDER_ANOTHER_COMPANY = "Sender have another company"
    RECEIVER_ANOTHER_COMPANY = "Receiver have another company"
    NOT_FOUND = "Company or users not found"


class ResponseStatus:
    success_canceled = "Invitation canceled successful"
    success_declined = "Invitation declined successful"


class InvitationCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Invitation):
        super().__init__(session, model)

    async def get(self, invitation_id: int) -> Optional[models.Invitation]:
        return await super().get(invitation_id)

    async def get_all(self) -> list[models.Invitation]:
        return await super().get_all()

    async def add(self, invitation):
        status = await invitation_status(invitation, self.session)
        if status in [InvitationStatus.TO_OWNER, InvitationStatus.TO_USER]:
            return await super().add(invitation)
        raise HTTPException(detail=status.value, status_code=418)

    async def delete(self, invitation_id: int):
        return await super().delete(invitation_id)

    async def cancel(self, invitation_id: int, current_user):
        invitation = await self.get(invitation_id)
        if not invitation:
            raise HTTPException(detail="invitation not exist", status_code=418)
        if invitation.sender_id != current_user.id:
            raise HTTPException(detail="You not not received this invitation", status_code=418)
        else:
            await self.delete(invitation_id)
            return ResponseStatus.success_canceled

    async def decline(self, invitation_id: int, current_user):
        invitation = await self.get(invitation_id)
        if not invitation:
            raise HTTPException(detail="invitation not exist", status_code=418)
        if invitation.receiver_id != current_user.id:
            raise HTTPException(detail="You not not received this invitation", status_code=418)
        else:
            await self.delete(invitation_id)
            return ResponseStatus.success_declined

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
        status = await invitation_status(await self.get(invitation_id), self.session)
        if status == InvitationStatus.TO_USER:
            stmt = select(models.User).where(models.User.id == invitation.receiver_id)
        elif status == InvitationStatus.TO_OWNER:
            stmt = select(models.User).where(models.User.id == invitation.sender_id)
        db_user = (await self.session.execute(stmt)).scalars().first()
        db_user.company_id = invitation.company_id
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        await self.delete(invitation_id)
        return db_user


invitation_crud = InvitationCRUD()
