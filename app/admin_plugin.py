import io
import logging
import os
from typing import Any
from urllib.parse import parse_qsl

from app.services.auth import AuthService
from app.utils.db_manager import DBManager
from app.utils.tokens import JWTTokenService
from sqladmin.authentication import AuthenticationBackend
import sqladmin
from markupsafe import Markup
from sqladmin.authentication import login_required
from sqladmin.helpers import get_object_identifier
from starlette.datastructures import URL, FormData, MultiDict, UploadFile
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from wtforms import Field, widgets

from app.database import async_session
from app.configs.base_config import app_settings


class AdminAuth(AuthenticationBackend):
    """Бэкенд аутентификации для панели администратора (SQLAdmin).

    Реализует логику входа, выхода и проверки текущей админ-сессии.
    Работает через JWT-токен, который хранится в `request.session["token"]`.

    Используется SQLAdmin при доступе к `/admin`:
    - при логине создаёт токен и сохраняет его в сессии;
    - при каждом запросе проверяет валидность токена;
    - при логауте очищает сессию.
    """

    async def login(self, request: Request) -> bool:
        """Авторизация администратора в панели SQLAdmin.

        Ожидает форму с `email` и `password`, проверяет учетные данные
        через `AuthService.authenticate_admin`, и при успехе создаёт JWT-токен
        типа `"admin"`, который сохраняется в сессии.

        Args:
            request (Request): объект Starlette-запроса с формой (`email`, `password`).

        Returns:
            bool: `True`, если логин успешен; `False` — если проверка не прошла.

        Side Effects:
            - Записывает в `request.session["token"]` токен администратора.
            - При ошибках логирует исключение в стандартный `logging`.
        """
        form = await request.form()
        email, password = form["email"], form["password"]
        try:
            async with DBManager(session_factory=async_session) as db:
                user = await AuthService(db).authenticate_admin(email, password)
                request.session.update(
                    {
                        "token": JWTTokenService.create_access_admin_token(
                            {"sub": str(user.id)}
                        )
                    }
                )
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def logout(self, request: Request) -> bool:
        """Завершает сессию администратора.

        Просто очищает данные сессии.

        Args:
            request (Request): текущий запрос с активной сессией.

        Returns:
            bool: всегда `True`.
        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Проверяет, авторизован ли текущий администратор.

        Декодирует JWT-токен из сессии и проверяет существование администратора в БД.

        Args:
            request (Request): объект запроса, содержащий `session["token"]`.

        Returns:
            bool:
                - `True` — если токен валиден и администратор существует;
                - `False` — если токен отсутствует, невалиден или админ не найден.

        Workflow:
            1. Проверяет наличие токена в сессии.
            2. Декодирует токен через `TokenService.decode_jwt_token(..., "admin")`.
            3. Находит администратора в базе данных (`AuthService.get_one_or_none_admin`).
        """
        token = request.session.get("token")
        if (
            not token
            or (sub := JWTTokenService.decode_jwt_token(token, "admin")) is None
        ):
            return False
        async with DBManager(session_factory=async_session) as db:
            user = await AuthService(db).get_one_or_none(id=sub)
        if user is None:
            return False
        return True


class SQLAdmin(sqladmin.Admin):
    """
    Расширение Admin-интерфейса sqladmin с асинхронной поддержкой Starlette/FastAPI.
    Добавлены кастомные методы create/edit/delete/list/details с поддержкой загрузки файлов и редиректов.
    """

    @login_required
    async def delete(self, request: Request) -> Response:
        """Delete route."""
        await self._delete(request)

        identity = request.path_params["identity"]
        model_view = self._find_model_view(identity)

        params = request.query_params.get("pks", "")
        pks = params.split(",") if params else []
        for pk in pks:
            model = await model_view.get_object_for_delete(pk)
            if not model:
                raise HTTPException(status_code=404)

            await model_view.delete_model(request, pk)

        referer_url = URL(request.headers.get("referer", ""))
        referer_params = MultiDict(parse_qsl(referer_url.query))
        url = URL(str(request.url_for("admin:list", identity=identity)))
        url = url.include_query_params(**referer_params)
        return Response(content=str(url))

    @login_required
    async def list(self, request: Request) -> Response:
        """List route to display paginated Model instances."""

        await self._list(request)

        model_view = self._find_model_view(request.path_params["identity"])
        pagination = await model_view.list(request)
        pagination.add_pagination_urls(request.url)

        request_page = model_view.validate_page_number(
            request.query_params.get("page"), 1
        )

        if request_page > pagination.page:
            return RedirectResponse(
                request.url.include_query_params(page=pagination.page),
                status_code=302,
            )

        context = {
            "model_view": model_view,
            "pagination": pagination,
            "prod_url": app_settings.PRODUCTION_URL,
        }
        return await self.templates.TemplateResponse(
            request, model_view.list_template, context
        )

    @login_required
    async def details(self, request: Request) -> Response:
        """Details route."""

        await self._details(request)

        model_view = self._find_model_view(request.path_params["identity"])

        model = await model_view.get_object_for_details(request)
        if not model:
            raise HTTPException(status_code=404)

        context = {
            "model_view": model_view,
            "model": model,
            "title": model_view.name,
            "prod_url": app_settings.PRODUCTION_URL,
        }

        return await self.templates.TemplateResponse(
            request, model_view.details_template, context
        )

    @login_required
    async def index(self, request: Request) -> Response:
        return await self.templates.TemplateResponse(
            request, "index.html", {"prod_url": app_settings.PRODUCTION_URL}
        )

    async def login(self, request: Request) -> Response:
        assert self.authentication_backend is not None

        context = {"prod_url": app_settings.PRODUCTION_URL}
        if request.method == "GET":
            return await self.templates.TemplateResponse(request, "login.html", context)

        ok = await self.authentication_backend.login(request)
        if not ok:
            context["error"] = "Некорректные данные"
            return await self.templates.TemplateResponse(
                request, "login.html", context, status_code=400
            )
        return RedirectResponse(request.url_for("admin:index"), status_code=302)

    async def _handle_form_data(self, request: Request, obj: Any = None) -> FormData:
        """
        Handle form data and modify in case of UploadFile.
        This is needed since in edit page
        there's no way to show current file of object.
        """
        form = await request.form()
        form_data: list[tuple[str, str | UploadFile]] = []
        for key, value in form.multi_items():
            if not isinstance(value, UploadFile):
                form_data.append((key, value))
                continue

            should_clear = form.get(key + "_checkbox")
            empty_upload = len(await value.read(1)) != 1
            await value.seek(0)
            if should_clear:
                form_data.append((key, UploadFile(io.BytesIO(b""))))
            elif empty_upload and obj and getattr(obj, key):
                form_data.append((key, getattr(obj, key)))
            else:
                form_data.append((key, value))
        return FormData(form_data)

    async def save_file(self, file: UploadFile):
        with open(
            os.path.join(app_settings.BASE_DIR, "media", file.filename),
            "wb",
        ) as f:
            f.write(file.file.read())
        return f"/media/{file.filename}"

    @login_required
    async def create(self, request: Request) -> Response:
        """Create model endpoint."""

        await self._create(request)

        identity = request.path_params["identity"]
        model_view = self._find_model_view(identity)

        Form = await model_view.scaffold_form(model_view._form_create_rules)
        form_data = await self._handle_form_data(request)
        form = Form(form_data)

        context = {
            "model_view": model_view,
            "form": form,
            "prod_url": app_settings.PRODUCTION_URL,
        }

        if request.method == "GET":
            return await self.templates.TemplateResponse(
                request, model_view.create_template, context
            )

        if not form.validate():
            return await self.templates.TemplateResponse(
                request, model_view.create_template, context, status_code=400
            )

        form_data_dict = self._denormalize_wtform_data(form.data, model_view.model)
        try:
            obj = await model_view.insert_model(request, form_data_dict)
        except Exception as e:
            logging.exception(e)
            context["error"] = str(e)
            return await self.templates.TemplateResponse(
                request, model_view.create_template, context, status_code=400
            )

        url = self.get_save_redirect_url(
            request=request,
            form=form_data,
            obj=obj,
            model_view=model_view,
        )
        return RedirectResponse(url=url, status_code=302)

    @login_required
    async def edit(self, request: Request) -> Response:
        """Edit model endpoint."""

        await self._edit(request)

        identity = request.path_params["identity"]
        model_view = self._find_model_view(identity)

        model = await model_view.get_object_for_edit(request)
        if not model:
            raise HTTPException(status_code=404)

        Form = await model_view.scaffold_form(model_view._form_edit_rules)

        context = {
            "obj": model,
            "model_view": model_view,
            "form": Form(obj=model, data=self._normalize_wtform_data(model)),
            "prod_url": app_settings.PRODUCTION_URL,
        }

        if request.method == "GET":
            return await self.templates.TemplateResponse(
                request, model_view.edit_template, context
            )

        form_data = await self._handle_form_data(request, model)

        form = Form(form_data)
        if not form.validate():
            context["form"] = form
            return await self.templates.TemplateResponse(
                request, model_view.edit_template, context, status_code=400
            )

        form_data_dict = self._denormalize_wtform_data(form.data, model)
        try:
            if model_view.save_as and form_data.get("save") == "Save as new":
                obj = await model_view.insert_model(request, form_data_dict)
            else:
                obj = await model_view.update_model(
                    request, pk=request.path_params["pk"], data=form_data_dict
                )
        except Exception as e:
            logging.error(e)
            context["error"] = str(e)
            return await self.templates.TemplateResponse(
                request, model_view.edit_template, context, status_code=400
            )

        url = self.get_save_redirect_url(
            request=request,
            form=form_data,
            obj=obj,
            model_view=model_view,
        )
        return RedirectResponse(url=url, status_code=302)

    def get_save_redirect_url(
        self, request: Request, form: FormData, model_view: sqladmin.ModelView, obj: Any
    ) -> str | URL:
        """
        Get the redirect URL after a save action
        which is triggered from create/edit page.
        """
        identity = request.path_params["identity"]
        identifier = get_object_identifier(obj)

        if form.get("save") == "Сохранить":
            return request.url_for("admin:list", identity=identity)
        elif form.get("save") == "Сохранить и продолжить редактирование" or (
            form.get("save") == "Сохранить как новый объект"
            and model_view.save_as_continue
        ):
            return request.url_for("admin:edit", identity=identity, pk=identifier)
        return request.url_for("admin:create", identity=identity)


class FileInputWidget(widgets.FileInput):
    """
    File input widget with clear checkbox.
    """

    def __call__(self, field: Field, **kwargs: Any) -> str:
        if not field.flags.required:
            checkbox_id = f"{field.id}_checkbox"
            checkbox_label = Markup(
                f'<label class="form-check-label" for="{checkbox_id}">Clear</label>'
            )
            checkbox_input = Markup(
                f'<input class="form-check-input" type="checkbox" id="{checkbox_id}" '
                f'name="{checkbox_id}">'  # noqa: E501
            )
            checkbox = Markup(
                f'<div class="form-check">{checkbox_input}{checkbox_label}</div>'
            )
        else:
            checkbox = Markup()

        if field.data:
            data = field.data.split("/")[-1]
            current_value = Markup(
                f"<p>Текущий файл: <a href='{app_settings.PRODUCTION_URL}{field.data}' "
                f"target='_blank'>{data}</a></p>"
            )
            field.flags.required = False
            return current_value + checkbox + super().__call__(field, **kwargs)
        else:
            return super().__call__(field, **kwargs)


class FileField(Field):
    """
    WTForms поле для работы с файлами с кастомным FileInputWidget.
    """

    widget = FileInputWidget()

    def _value(self):
        return False
