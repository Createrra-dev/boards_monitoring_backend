from datetime import date, datetime, time
from app.exceptions import ObjectNotFoundException
from app.models.boards_state_history import BoardStateHistory
from app.schemes.boards import BoardAddDTO
from app.schemes.boards_state_history import BoardStateHistoryAddDTO, BoardStateHistoryAddRequestDTO, BoardStateHistoryDTO, BoardStateHistoryDTO
from app.services.base import BaseService


class BoardStateHistoryService(BaseService):
    
    async def get_all(self, organization_slug: str, board_slug: str, date_from: date, date_to: date) -> list[BoardStateHistoryDTO]:
        organization = await self.db.organizations.get_one_or_none(slug=organization_slug)
        if organization is None:
            raise ObjectNotFoundException
        board = await self.db.boards.get_one_or_none(slug=board_slug, organization_id=organization.id)
        if board is None:
            raise ObjectNotFoundException
        if date_from:
            date_from = datetime.combine(date_from, time.min)

        if date_to:
            date_to = datetime.combine(date_to, time.max)
        return await self.db.boards_state_history.get_filtered(
            *[BoardStateHistory.created_at <= date_to, BoardStateHistory.created_at >= date_from],
            order_by="created_at", 
            descending=True, 
            board_id=board.id
        )
    
    async def add(self, organization_slug: str, board_slug: str, data: BoardStateHistoryAddRequestDTO) -> BoardStateHistoryDTO:
        organization = await self.db.organizations.get_one_or_none(slug=organization_slug)
        if organization is None:
            raise ObjectNotFoundException
        board = await self.db.boards.get_one_or_none(slug=board_slug)
        if board is None:
            board = await self.db.boards.add(BoardAddDTO(organization_id=organization.id, name=board_slug, slug=board_slug))
        data = BoardStateHistoryAddDTO(board_id=board.id, **data.model_dump())
        state_hisory = await self.db.boards_state_history.add(data)
        await self.db.commit()
        return state_hisory
        