from app.models.boards_state_history import StatusType
from app.schemes.boards import BoardWithStatusDTO
from app.services.base import BaseService
from app import redis_manager
from app.utils.telegram_bot import send_telegram_message


class BoardService(BaseService):
    
    async def get_all_with_status(self, organization_slug: str) -> list[BoardWithStatusDTO]:
        return await self.db.boards.get_all_with_status(organization_slug)

    async def check_boards_status(self):
        boards = await self.db.boards.get_all_with_status_inner_join()
        for board in boards:
            redis_key = f"{board.slug}"
            prev_status_bytes = await redis_manager.get(redis_key)
            prev_status = StatusType(prev_status_bytes.decode()) if prev_status_bytes else None
            await redis_manager.set(redis_key, board.status.value)
            if board.status == StatusType.OFFLINE and prev_status == StatusType.ONLINE:
                await send_telegram_message(f"⚠️ Плата {board.name} вышла из строя")
            elif board.status == StatusType.ONLINE and prev_status == StatusType.OFFLINE:
                await send_telegram_message(f"✅ Плата {board.name} снова онлайн")
