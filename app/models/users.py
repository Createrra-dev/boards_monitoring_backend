from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, BaseORM


class User(Base, BaseORM):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
