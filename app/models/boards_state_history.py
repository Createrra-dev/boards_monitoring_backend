from datetime import datetime
from enum import Enum
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, BaseORM


class EventType(Enum):
    STATE = "STATE"
    LWT = "LWT"
    
    
class StatusType(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class BoardStateHistory(Base, BaseORM):
    __tablename__ = "boards_state_history"

    board_id: Mapped[UUID] = mapped_column(ForeignKey("boards.id", ondelete="CASCADE"))
    event: Mapped[EventType]
    status: Mapped[StatusType]
