from app.exceptions import ObjectNotFoundException
from app.schemes.boards_state_history import BoardStateHistoryAddDTO, BoardStateHistoryAddRequestDTO, BoardStateHistoryDTO, BoardStateHistoryDTO
from app.services.base import BaseService


class BoardStateHistoryService(BaseService):
    
    async def get_all(self, board_slug: str) -> list[BoardStateHistoryDTO]:
        board = await self.db.boards.get_one_or_none(slug=board_slug)
        if board is None:
            raise ObjectNotFoundException
        return await self.db.boards_state_history.get_filtered(order_by="created_at", descending=True, board_id=board.id)
    
    async def add(self, board_slug: str, data: BoardStateHistoryAddRequestDTO) -> BoardStateHistoryDTO:
        board = await self.db.boards.get_one_or_none(slug=board_slug)
        if board is None:
            raise ObjectNotFoundException
        data = BoardStateHistoryAddDTO(board_id=board.id, **data.model_dump())
        state_hisory = await self.db.boards_state_history.add(data)
        await self.db.commit()
        return state_hisory
        