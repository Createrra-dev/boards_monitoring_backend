from app.mappers.base import DataMapper
from app.models.users import User
from app.schemes.users import UserDTO


class UserDataMapper(DataMapper):
    """
    Маппер для преобразования ORM-модели `User` в Pydantic-схему `UserDTO`
    и обратно.

    Используется для администраторов.
    """

    db_model = User
    schema = UserDTO
