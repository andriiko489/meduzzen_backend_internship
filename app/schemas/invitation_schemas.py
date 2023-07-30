from typing import Optional

from pydantic import BaseModel, ConfigDict


class BasicInvitation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sender_id: Optional[int] = None
    receiver_id: int
    company_id: int


class SendInvitation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    receiver_id: int
    company_id: int
