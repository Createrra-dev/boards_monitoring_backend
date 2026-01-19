from datetime import datetime
import uuid

from sqlalchemy import UUID, DateTime, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.configs.base_config import postgres_settings

async_engine = create_async_engine(
    postgres_settings.DB_URL,
    pool_recycle=3600,
    echo=False,
    future=True,
)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


class TimeStampORM:
    """Базовый класс для моделей SQLAlchemy"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class BaseORM(TimeStampORM):
    """Базовый класс для моделей SQLAlchemy"""

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
