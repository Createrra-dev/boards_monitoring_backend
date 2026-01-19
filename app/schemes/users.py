from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserAddDTO(BaseModel):
    email: EmailStr
    hashed_password: str


class UserDTO(UserAddDTO):
    id: UUID

    class Config:
        from_attributes = True
