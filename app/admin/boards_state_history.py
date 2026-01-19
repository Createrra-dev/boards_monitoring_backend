from sqladmin import ModelView

from app.models.boards_state_history import BoardStateHistory


class BoardStateHistoryAdmin(ModelView, model=BoardStateHistory):
    """Представление модели `BoardStateHistory` в панели администратора SQLAdmin.

    Управляет отображением истории состояния плат.
    Позволяет видеть событие, статус и привязанную плату.

    Attributes:
        details_template (str): Шаблон страницы с подробной информацией.
        list_template (str): Шаблон страницы списка записей.
        create_template (str): Шаблон для создания новой записи.
        edit_template (str): Шаблон для редактирования записи.
        column_list (list): Отображаемые колонки в списке.
        column_labels (dict): Читаемые названия полей.
        name (str): Название модели в единственном числе.
        name_plural (str): Название модели во множественном числе.
        page_size (int): Количество записей на странице.
    """

    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"

    column_list = [
        BoardStateHistory.id,
        BoardStateHistory.board_id,
        BoardStateHistory.event,
        BoardStateHistory.status,
        BoardStateHistory.created_at,
        BoardStateHistory.updated_at,
    ]

    name = "состояние платы"
    name_plural = "История состояний плат"

    column_labels = {
        BoardStateHistory.id: "ID",
        BoardStateHistory.board_id: "Плата",
        BoardStateHistory.event: "Событие",
        BoardStateHistory.status: "Статус",
        BoardStateHistory.created_at: "Создано",
        BoardStateHistory.updated_at: "Обновлено",
    }

    page_size = 50

