from app.mappers.users import UserDataMapper
from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """
    Репозиторий для работы с сущностью `User`.

    Наследует все CRUD-операции и фильтрацию от `BaseRepository`.

    Attributes:
        model (type[User]): ORM-модель `User`, с которой работает репозиторий.
        mapper (type[UserDataMapper]): Класс для преобразования ORM-моделей `User`
            в доменные объекты или DTO.
    """

    model = User
    mapper = UserDataMapper
