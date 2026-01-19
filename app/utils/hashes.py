from passlib.context import CryptContext


class HashService:
    """
    Сервис для работы с хешированием и проверкой паролей.
    Использует библиотеку `passlib` и алгоритм bcrypt для безопасного хранения паролей.
    """

    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    @classmethod
    def create_hash_password(cls, password: str) -> str:
        """
        Создает хеш для переданного пароля.
        Args:
            password (str): Пароль.

        Returns:
            str: Хэш пароля.
        """
        return str(cls.pwd_context.hash(password))

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет соответствие пароля и его хеша.
        Args:
            plain_password (str): Пароль.
            hashed_password (str): Хеш пароля, сохраненный в БД у пользователя.
        Returns:
            bool: True, если пароль корректный, иначе False.
        """
        return bool(cls.pwd_context.verify(plain_password, hashed_password))
