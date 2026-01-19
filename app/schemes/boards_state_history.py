from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.models.boards_state_history import EventType, StatusType


class BoardStateHistoryDTO(BaseModel):
    id: UUID
    board_id: UUID
    event: EventType
    status: StatusType
    created_at: datetime

    class Config:
        from_attributes = True


class BoardStateHistoryAddDTO(BaseModel):
    board_id: UUID
    event: EventType
    status: StatusType
    
    
class BoardStateHistoryAddRequestDTO(BaseModel):
    event: EventType
    status: StatusType