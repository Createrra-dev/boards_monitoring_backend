from app.exceptions import UserNotFoundException, VerifyPasswordException
from app.schemes.users import UserAddDTO, UserDTO
from app.services.base import BaseService
from app.utils.hashes import HashService


class AuthService(BaseService):
    
    async def add_admin(self, email: str, password: str):
        """
        Создает администратора с указанным email и паролем.

        Args:
            email: email администратора
            password: пароль (будет захеширован)

        Returns:
            None
        """
        hashed_password = HashService.create_hash_password(password)
        admin_data = UserAddDTO(
            email=email, hashed_password=hashed_password
        )
        await self.db.users.add(admin_data)
        await self.db.commit()
        
    async def authenticate_admin(self, email: str, password: str) -> UserDTO:
        """
        Аутентификация администратора по email и паролю.

        Args:
            email: email администратора
            password: пароль для проверки

        Raises:
            UserNotFoundException: если администратор не найден
            VerifyPasswordException: если пароль неверен

        Returns:
            AdminDTO: объект администратора
        """
        user = await self.get_one_or_none(email=email)
        if user is None:
            raise UserNotFoundException
        if not HashService.verify_password(password, user.hashed_password):
            raise VerifyPasswordException
        return user

    async def get_one_or_none(self, **filter_by) -> UserDTO | None:
        """
        Получает одного администратора по фильтру или None.

        Returns:
            AdminDTO | None
        """
        return await self.db.users.get_one_or_none(**filter_by)
