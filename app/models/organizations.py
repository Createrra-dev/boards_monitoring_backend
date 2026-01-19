from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, BaseORM

if TYPE_CHECKING:
    from app.models.boards import Board


class Organization(Base, BaseORM):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    
    boards: Mapped[list["Board"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    
    def __str__(self):
        return f"{self.name}"
