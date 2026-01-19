import asyncio

from app.configs.celery_config import celery_app

from app.dependiences import get_db
from app.services.boards import BoardService
from app import redis_manager


async def _check_boards_status():
    await redis_manager.connect()
    async for db in get_db():
        await BoardService(db).check_boards_status()
    await redis_manager.close()


@celery_app.task(name="check_boards_status")
def check_boards_status():
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(_check_boards_status())
