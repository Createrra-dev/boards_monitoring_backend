from fastapi import APIRouter

from app.dependiences import DBDep
from app.schemes.boards import BoardWithStatusDTO
from app.services.boards import BoardService


router = APIRouter(prefix="/organizations/{organization_slug}/boards", tags=["Платы"])


@router.get("/")
async def get_boards(organization_slug: str, db: DBDep) -> list[BoardWithStatusDTO]:
    """Получение списка плат организации со статусом"""
    return await BoardService(db).get_all_with_status(organization_slug)
