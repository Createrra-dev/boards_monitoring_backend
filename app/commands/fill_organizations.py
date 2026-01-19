import asyncio
import pathlib
import sys

import rich

if __name__ == "__main__":
    sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

from app.commands.data.organizations import ORGANIZATIONS
from app.database import async_session
from app.utils.db_manager import DBManager
from app.schemes.organizations import OrganizationAddWithIDDTO


async def fill_organizations():
    organizations_data = [OrganizationAddWithIDDTO(**country) for country in ORGANIZATIONS]
    async with DBManager(session_factory=async_session) as db:
        await db.organizations.add_bulk(organizations_data)
        await db.commit()
    rich.print("[green]База данных с организациями предзаполнена")


if __name__ == "__main__":
    asyncio.run(fill_organizations())
