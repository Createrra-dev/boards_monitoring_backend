import asyncio
import logging
import pathlib
import sys

import rich

if __name__ == "__main__":
    sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

    from app.database import async_session
    from app.services.auth import AuthService
    from app.utils.db_manager import DBManager


async def create_admin():
    """Асинхронная функция для интерактивного создания администратора.

    1. Запрашивает у пользователя email и пароль.
    2. Проверяет совпадение пароля и подтверждения.
    3. Добавляет администратора в базу данных через `AuthService.add_admin`.
    4. Логирует ошибки и выводит сообщения о статусе выполнения.

    Side Effects:
        - Создаёт запись администратора в базе данных.
        - Печатает сообщения в консоль с помощью `rich`.
        - В случае ошибок логирует их через `logging`.

    Raises:
        SystemExit: если пароли не совпадают.
    """
    email = input("Введите адрес электронной почты: ")
    password = input("Введите пароль: ")
    confirm_password = input("Повтороите пароль: ")
    if password != confirm_password:
        rich.print("[red]Пароли не совпадают")
        sys.exit(1)
    try:
        async with DBManager(session_factory=async_session) as db:
            await AuthService(db).add_admin(email, password)
        rich.print(f"[green]Администратор {email} успешно создан")
    except Exception as e:
        logging.error(e)
        rich.print("[red]Введите корректные данные")


if __name__ == "__main__":
    asyncio.run(create_admin())
