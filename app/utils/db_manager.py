from app.repositories.organizations import OrganizationRepository
from app.repositories.boards import BoardRepository
from app.repositories.boards_state_history import BoardStateHistoryRepository
from app.repositories.users import UserRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.organizations = OrganizationRepository(self.session)
        self.boards = BoardRepository(self.session)
        self.boards_state_history = BoardStateHistoryRepository(self.session)
        self.users = UserRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()