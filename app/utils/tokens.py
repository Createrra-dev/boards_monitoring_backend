import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

from app.configs.base_config import app_settings
from jose import JWTError, jwt

from app.exceptions import DecodeTokenException, TokenKeysException, TokenTypeException


class JWTTokenService:
    """
    Сервис для генерации и валидации JWT токенов.
    """

    @classmethod
    def create_access_and_refresh_tokens(cls, data: dict) -> Tuple[str, str]:
        """
        Создаёт пару токенов: access и refresh.
        Args:
            data (dict): Данные, которые будут добпавлены в payload токена.
        Returns:
            Tuple[str, str]: Кортеж, который содержит access_token и refresh_token.
        """
        access_token = cls._create_jwt_token(
            data,
            "access",
            app_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        refresh_token = cls._create_jwt_token(
            data,
            "refresh",
            app_settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
        )
        return access_token, refresh_token

    @classmethod
    def create_access_admin_token(cls, data: dict) -> str:
        """
        Создаёт JWT токен для админа.
        Args:
            data (dict): Данные для payload.
        Returns:
            str: Сгенерированный JWT токен.
        """
        access_token = cls._create_jwt_token(
            data,
            "admin",
            app_settings.JWT_ACCESS_TOKEN_ADMIN_EXPIRE_DAYS,
        )
        return access_token

    @staticmethod
    def _create_jwt_token(data: dict, type: str, token_expire: int) -> str:
        """
        Создаёт JWT токен определённого типа.
        Args:
            data (dict): Данные для payload.
            type (str): Тип токена.
            token_expire (int): Время жизни токена.
        Returns:
            str: Сгенерированный JWT токен.
        """
        if type == "access":
            expire = datetime.now(timezone.utc) + timedelta(minutes=token_expire)
        elif type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(days=token_expire)
        elif type == "admin":
            expire = datetime.now(timezone.utc) + timedelta(days=token_expire)
        else:
            raise ValueError("Неверный тип токена. Ожидается 'access' или 'refresh'.")

        payload = data.copy()
        payload.update({"exp": expire, "type": type})

        token = jwt.encode(
            payload, app_settings.JWT_SECRET_KEY, algorithm=app_settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    def decode_jwt_token(token: str, token_type: str) -> Optional[Dict[str, Any]]:
        """
        Декодирует и проверяет JWT токен.
        Args:
            token (str): JWT токен.
        Returns:
            Optional[Dict[str, Any]]:
                - словарь с расшифрованными данными, если токен валиден;
                - None, если токен невалидный или не соответствует схеме.
        """
        try:
            decode_token = jwt.decode(
                token,
                app_settings.JWT_SECRET_KEY,
                algorithms=[app_settings.JWT_ALGORITHM],
            )
        except (JWTError, AttributeError):
            raise DecodeTokenException
        if set(decode_token.keys()) != {"sub", "exp", "type"}:
            raise TokenKeysException
        if decode_token.get("type") != token_type:
            raise TokenTypeException
        return uuid.UUID(decode_token.get("sub"))
