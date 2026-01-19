from datetime import datetime, timedelta

from sqlalchemy import case, func, select
from app.mappers.organizations import OrganizationDataMapper
from app.models.boards import Board
from app.models.boards_state_history import EventType, StatusType
from app.models.organizations import Organization
from app.repositories.base import BaseRepository
from app.configs.base_config import app_settings
from app.repositories.utils import get_latest_status
from app.schemes.organizations import OrganizationWithCountOffBoardsDTO


class OrganizationRepository(BaseRepository):
    """
    Репозиторий для работы с сущностью `Organization`.

    Наследует все CRUD-операции и фильтрацию от `BaseRepository`.

    Attributes:
        model (type[Organization]): ORM-модель `Organization`, с которой работает репозиторий.
        mapper (type[OrganizationDataMapper]): Класс для преобразования ORM-моделей `Organization`
            в доменные объекты или DTO.
    """

    model = Organization
    mapper = OrganizationDataMapper
    
    async def get_all_with_count_offline_boards(self):
        offline_threshold = datetime.now() - timedelta(seconds=app_settings.THRESHOLD_SEC)
        latest_status_cte = get_latest_status()
        offline_condition = (
            (latest_status_cte.c.id.is_(None)) |
            (
                (latest_status_cte.c.event == EventType.LWT) &
                (latest_status_cte.c.status == StatusType.OFFLINE)
            ) |
            (
                (latest_status_cte.c.event == EventType.STATE) &
                (latest_status_cte.c.created_at < offline_threshold)
            )
        )
        stmt = (
            select(
                Organization.id,
                Organization.name,
                Organization.slug,
                func.sum(
                    case(
                        (offline_condition, 1),
                        else_=0
                    )
                ).label("count_offline_boards")
            )
            .select_from(Organization)
            .join(Board, Board.organization_id == Organization.id)
            .outerjoin(
                latest_status_cte,
                (latest_status_cte.c.board_id == Board.id) &
                (latest_status_cte.c.rn == 1)
            )
            .group_by(Organization.id)
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        return [
            OrganizationWithCountOffBoardsDTO(
                id=row[0],
                name=row[1],
                slug=row[2],
                count_offline_boards=row[3]
            )
            for row in rows
        ]
