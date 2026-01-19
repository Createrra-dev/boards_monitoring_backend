from sqladmin import ModelView

from app.models.boards import Board


class BoardAdmin(ModelView, model=Board):
    """Представление модели `Board` в панели администратора SQLAdmin.

    Управляет отображением и редактированием плат.
    Связывает плату с организацией, позволяет управлять именем и slug.

    Attributes:
        details_template (str): Шаблон страницы с подробной информацией о плате.
        list_template (str): Шаблон страницы списка плат.
        create_template (str): Шаблон для создания новой платы.
        edit_template (str): Шаблон для редактирования платы.
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
        Board.id,
        Board.organization,
        Board.name,
        Board.slug,
        Board.created_at,
        Board.updated_at,
    ]

    name = "плата"
    name_plural = "Платы"

    column_labels = {
        Board.id: "ID",
        Board.organization: "Организация",
        Board.name: "Название",
        Board.slug: "Слаг",
        Board.created_at: "Создано",
        Board.updated_at: "Обновлено",
    }

    page_size = 50
