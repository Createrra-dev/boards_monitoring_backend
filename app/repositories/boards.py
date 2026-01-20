from datetime import datetime, timedelta

from sqlalchemy import case, select
from app.mappers.boards import BoardDataMapper, BoardWithStatusDataMapper
from app.models.boards import Board
from app.models.boards_state_history import BoardStateHistory, EventType, StatusType
from app.models.organizations import Organization
from app.repositories.base import BaseRepository
from app.configs.base_config import app_settings
from app.repositories.utils import get_latest_status
from app.schemes.boards import BoardWithStatusDTO


class BoardRepository(BaseRepository):
    """
    Репозиторий для работы с сущностью `Board`.

    Наследует все CRUD-операции и фильтрацию от `BaseRepository`.

    Attributes:
        model (type[Board]): ORM-модель `Board`, с которой работает репозиторий.
        mapper (type[BoardDataMapper]): Класс для преобразования ORM-моделей `Board`
            в доменные объекты или DTO.
    """

    model = Board
    mapper = BoardDataMapper
    
    async def get_all_with_status(self, organization_slug: str) -> list[BoardWithStatusDTO]:
        offline_threshold = datetime.now() - timedelta(seconds=app_settings.THRESHOLD_SEC)
        latest_status_cte = get_latest_status()
        stmt = (
            select(
                Board.id,
                Board.name,
                Board.slug,
                case(
                    (latest_status_cte.c.id.is_(None), "OFFLINE"),
                    (
                        (latest_status_cte.c.event == EventType.LWT) &
                        (latest_status_cte.c.created_at < offline_threshold),
                        "OFFLINE"
                    ),
                    (
                        (latest_status_cte.c.event == EventType.STATE) &
                        (latest_status_cte.c.created_at < offline_threshold),
                        "OFFLINE"
                    ),
                    else_="ONLINE"
                ).label("status")
            )
            .join(Organization, Organization.id == Board.organization_id)
            .outerjoin(
                latest_status_cte,
                (latest_status_cte.c.board_id == Board.id) &
                (latest_status_cte.c.rn == 1)
            )
            .where(Organization.slug == organization_slug)
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            BoardWithStatusDTO(
                id=row[0],
                name=row[1],
                slug=row[2],
                status=row[3]
            )
            for row in rows
        ]
        
    async def get_all_with_status_inner_join(self) -> list[BoardWithStatusDTO]:
        offline_threshold = datetime.now() - timedelta(seconds=app_settings.THRESHOLD_SEC)
        latest_status_cte = get_latest_status()

        stmt = (
            select(
                Board.id,
                Board.name,
                Board.slug,
                case(
                    (
                        (latest_status_cte.c.event == EventType.LWT) &
                        (latest_status_cte.c.created_at < offline_threshold),
                        "OFFLINE"
                    ),
                    (
                        (latest_status_cte.c.event == EventType.STATE) &
                        (latest_status_cte.c.created_at < offline_threshold),
                        "OFFLINE"
                    ),
                    else_="ONLINE"
                ).label("status")
            )
            .join(Organization, Organization.id == Board.organization_id)
            .join(
                latest_status_cte,
                (latest_status_cte.c.board_id == Board.id) &
                (latest_status_cte.c.rn == 1)
            )
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        return [
            BoardWithStatusDTO(
                id=row[0],
                name=row[1],
                slug=row[2],
                status=row[3]
            )
            for row in rows
        ]

