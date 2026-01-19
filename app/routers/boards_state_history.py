from fastapi import APIRouter, HTTPException

from app.dependiences import DBDep
from app.exceptions import ObjectNotFoundException
from app.schemes.boards_state_history import BoardStateHistoryAddRequestDTO, BoardStateHistoryDTO
from app.services.boards_state_history import BoardStateHistoryService


router = APIRouter(prefix="/boards/{boards_slug}/history", tags=["История состояний плат"])


@router.get("/")
async def get_state_history(boards_slug: str, db: DBDep) -> list[BoardStateHistoryDTO]:
    """Получение истории состояний платы"""
    try:
        return await BoardStateHistoryService(db).get_all(boards_slug)
    except ObjectNotFoundException:
        return []


@router.post("/")
async def create_state_history(boards_slug: str, db: DBDep, state_history: BoardStateHistoryAddRequestDTO) -> BoardStateHistoryDTO:
    """Добавление состояния платы"""
    try:
        return await BoardStateHistoryService(db).add(boards_slug, state_history)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Плата не найдена")
