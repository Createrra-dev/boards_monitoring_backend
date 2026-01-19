from app.mappers.base import DataMapper
from app.models.boards_state_history import BoardStateHistory
from app.schemes.boards_state_history import BoardStateHistoryDTO


class BoardStatrHistoryDataMapper(DataMapper):
    """
    Маппер для преобразования ORM-модели `BoardStatrHistory` в Pydantic-схему `BoardStatrHistoryDTO`
    и обратно.

    Используется для администраторов.
    """

    db_model = BoardStateHistory
    schema = BoardStateHistoryDTO
