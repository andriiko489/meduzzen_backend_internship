from fastapi import APIRouter, Depends

from crud.InvitationCRUD import invitation_crud
from models import models
from schemas import user_schemas, invitation_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/invitation",
    tags=["invitation"])


@router.get("/all/")
async def get_users(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await invitation_crud.get_all()


@router.get("/get")
async def get_user(invitation_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    invitation = await invitation_crud.get(invitation_id=invitation_id)
    return invitation


@router.post("/send")
async def send(invitation: invitation_schemas.SendInvitation,
                   current_user: user_schemas.User = Depends(Auth.get_current_user)):
    invitation = invitation_schemas.BasicInvitation(**invitation.model_dump())
    invitation.sender_id = current_user.id
    db_invitation: models.Invitation = await invitation_crud.add(invitation=invitation)
    return db_invitation


@router.delete("/cancel")
async def cancel(invitation_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await invitation_crud.cancel(invitation_id, current_user)


@router.delete("/decline")
async def cancel(invitation_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await invitation_crud.decline(invitation_id, current_user)


@router.get("/get_sent_invitations")
async def get_sent_invitations(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    invitations = await invitation_crud.get_sent_invitations(user_id=current_user.id)
    return invitations


@router.get("/get_received_invitations")
async def get_received_invitations(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    invitations = await invitation_crud.get_received_invitations(user_id=current_user.id)
    return invitations


@router.patch("/accept_invite")
async def accept_invite(invite_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await invitation_crud.accept_invitation(invite_id)
