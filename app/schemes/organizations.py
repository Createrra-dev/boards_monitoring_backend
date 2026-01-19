from pydantic import BaseModel
from uuid import UUID


class OrganizationAddDTO(BaseModel):
    name: str
    slug: str
    
    
class OrganizationAddWithIDDTO(OrganizationAddDTO):
    id: UUID
    

class OrganizationDTO(OrganizationAddDTO):
    id: UUID

    class Config:
        from_attributes = True
        
        
class OrganizationWithCountOffBoardsDTO(OrganizationAddDTO):
    id: UUID
    count_offline_boards: int

    class Config:
        from_attributes = True
