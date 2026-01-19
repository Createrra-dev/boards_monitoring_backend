from app.schemes.organizations import OrganizationWithCountOffBoardsDTO
from app.services.base import BaseService


class OrganizationService(BaseService):
    
    async def get_all_with_count_offline_boards(self) -> list[OrganizationWithCountOffBoardsDTO]:
        return await self.db.organizations.get_all_with_count_offline_boards()
