from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, BaseORM

if TYPE_CHECKING:
    from app.models.organizations import Organization


class Board(Base, BaseORM):
    __tablename__ = "boards"

    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    
    organization: Mapped["Organization"] = relationship(
        back_populates="boards"
    )
    
    def __str__(self):
        return f"{self.name}"
