from datetime import date
from fastapi import APIRouter, HTTPException

from app.dependiences import DBDep
from app.exceptions import ObjectNotFoundException
from app.schemes.boards_state_history import BoardStateHistoryAddRequestDTO, BoardStateHistoryDTO
from app.services.boards_state_history import BoardStateHistoryService


router = APIRouter(prefix="/organizations/{organization_slug}/boards/{boards_slug}/history", tags=["История состояний плат"])


@router.get("/")
async def get_state_history(
    organization_slug: str, 
    boards_slug: str, 
    db: DBDep,
    date_from: date,
    date_to: date
) -> list[BoardStateHistoryDTO]:
    """Получение истории состояний платы"""
    try:
        return await BoardStateHistoryService(db).get_all(
            organization_slug, boards_slug, date_from, date_to
        )
    except ObjectNotFoundException:
        return []


@router.post("/")
async def create_state_history(organization_slug: str, boards_slug: str, db: DBDep, state_history: BoardStateHistoryAddRequestDTO) -> BoardStateHistoryDTO:
    """Добавление состояния платы"""
    try:
        return await BoardStateHistoryService(db).add(organization_slug, boards_slug, state_history)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Организация не найдена")
