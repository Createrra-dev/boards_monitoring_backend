from app.mappers.base import DataMapper
from app.models.organizations import Organization
from app.schemes.organizations import OrganizationDTO, OrganizationWithCountOffBoardsDTO


class OrganizationDataMapper(DataMapper):
    """
    Маппер для преобразования ORM-модели `Organization` в Pydantic-схему `OrganizationDTO`
    и обратно.

    Используется для администраторов.
    """

    db_model = Organization
    schema = OrganizationDTO


class OrganizationWithCountOffBoardsDataMapper(DataMapper):
    """
    Маппер для преобразования ORM-модели `Organization` в Pydantic-схему `OrganizationWithCountOffBoardsDTO`
    и обратно.

    Используется для администраторов.
    """

    db_model = Organization
    schema = OrganizationWithCountOffBoardsDTO
