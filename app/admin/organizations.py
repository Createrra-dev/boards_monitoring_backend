from sqladmin import ModelView

from app.models.organizations import Organization


class OrganizationAdmin(ModelView, model=Organization):
    """Представление модели `Organization` в панели администратора SQLAdmin.

    Управляет отображением и редактированием организаций.
    Позволяет просматривать список организаций, их название и slug.

    Attributes:
        details_template (str): Шаблон страницы с подробной информацией об организации.
        list_template (str): Шаблон страницы списка организаций.
        create_template (str): Шаблон для создания новой организации.
        edit_template (str): Шаблон для редактирования организации.
        column_list (list): Список колонок, отображаемых в таблице списка.
        column_labels (dict): Читаемые метки полей.
        name (str): Название модели в единственном числе.
        name_plural (str): Название модели во множественном числе.
        page_size (int): Количество записей на странице.
    """

    details_template = "details.html"
    list_template = "list.html"
    create_template = "create.html"
    edit_template = "edit.html"

    column_list = [
        Organization.id,
        Organization.name,
        Organization.slug,
        Organization.created_at,
        Organization.updated_at,
    ]

    name = "организация"
    name_plural = "Организации"

    column_labels = {
        Organization.id: "ID",
        Organization.name: "Название",
        Organization.slug: "Слаг",
        Organization.created_at: "Создано",
        Organization.updated_at: "Обновлено",
    }

    page_size = 50
