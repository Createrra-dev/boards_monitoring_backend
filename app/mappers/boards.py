from app.mappers.base import DataMapper
from app.models.boards import Board
from app.schemes.boards import BoardWithStatusDTO, BoardDTO


class BoardDataMapper(DataMapper):
    """
    Маппер для преобразования ORM-модели `Board` в Pydantic-схему `BoardDTO`
    и обратно.

    Используется для администраторов.
    """

    db_model = Board
    schema = BoardDTO
    
    
class BoardWithStatusDataMapper(DataMapper):
    """
    Маппер для преобразования ORM-модели `Board` в Pydantic-схему `BoardWithStatusDTO`
    и обратно.

    Используется для администраторов.
    """

    db_model = Board
    schema = BoardWithStatusDTO
