from pydantic import BaseModel
from uuid import UUID

from app.models.boards_state_history import StatusType


class BoardAddDTO(BaseModel):
    organization_id: UUID
    name: str
    slug: str


class BoardDTO(BoardAddDTO):
    id: UUID

    class Config:
        from_attributes = True
        
        
class BoardWithStatusDTO(BaseModel):
    id: UUID
    name: str
    slug: str
    status: StatusType

    class Config:
        from_attributes = True