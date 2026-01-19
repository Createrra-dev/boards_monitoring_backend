import asyncio
import pathlib
import sys

import rich

if __name__ == "__main__":
    sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from app.commands.data.boards import BOARDS
from app.database import async_session
from app.utils.db_manager import DBManager
from app.schemes.boards import BoardAddDTO


async def fill_boards():
    boards_data = [BoardAddDTO(**language) for language in BOARDS]
    async with DBManager(session_factory=async_session) as db:
        await db.boards.add_bulk(boards_data)
        await db.commit()
    rich.print("[green]База данных с платами предзаполнена")


if __name__ == "__main__":
    asyncio.run(fill_boards())