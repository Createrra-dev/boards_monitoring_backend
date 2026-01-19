from fastapi import APIRouter

from app.dependiences import DBDep
from app.schemes.organizations import OrganizationWithCountOffBoardsDTO
from app.services.organizations import OrganizationService


router = APIRouter(prefix="/organizations", tags=["Организации"])


@router.get("/")
async def get_organizations(db: DBDep) -> list[OrganizationWithCountOffBoardsDTO]:
    """Получение списка организаций с количеством неактивных плат"""
    return await OrganizationService(db).get_all_with_count_offline_boards()
    