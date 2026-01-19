from app.mappers.boards_state_history import BoardStatrHistoryDataMapper
from app.models.boards_state_history import BoardStateHistory
from app.repositories.base import BaseRepository


class BoardStateHistoryRepository(BaseRepository):
    """
    Репозиторий для работы с сущностью `BoardStateHistory`.

    Наследует все CRUD-операции и фильтрацию от `BaseRepository`.

    Attributes:
        model (type[BoardStateHistory]): ORM-модель `BoardStateHistory`, с которой работает репозиторий.
        mapper (type[BoardStateHistoryDataMapper]): Класс для преобразования ORM-моделей `BoardStateHistory`
            в доменные объекты или DTO.
    """

    model = BoardStateHistory
    mapper = BoardStatrHistoryDataMapper
