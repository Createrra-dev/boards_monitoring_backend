from contextlib import asynccontextmanager
import logging
import os
import sys
from pathlib import Path

import jinja2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

sys.path.append(str(Path(__file__).parent.parent))

from app import redis_manager
from app.admin.boards import BoardAdmin
from app.admin.organizations import OrganizationAdmin
from app.admin_plugin import AdminAuth, SQLAdmin
from app.configs.base_config import app_settings
from app.configs.logging_config import setup_logging
from app.database import async_engine
from app.routers.organizations import router as organizations_router
from app.routers.boards import router as boards_router
from app.routers.boards_state_history import router as boards_state_history_router
from app.admin.boards_state_history import BoardStateHistoryAdmin

setup_logging()

logger = logging.getLogger("logger")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()
    

app = FastAPI(lifespan=lifespan)

admin = SQLAdmin(
    app,
    async_engine,
    title="Панель администратора",
    authentication_backend=AdminAuth(secret_key=app_settings.SESSION_SECRET_KEY),
)

admin.add_view(OrganizationAdmin)
admin.add_view(BoardAdmin)
admin.add_view(BoardStateHistoryAdmin)


loader = jinja2.FileSystemLoader(os.path.join(str(app_settings.BASE_DIR), "templates"))
env = jinja2.Environment(loader=loader)
templates = Jinja2Templates(env=env)

app.mount("/statics", StaticFiles(directory="statics", check_dir=False), name="statics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=app_settings.ALLOWED_HOSTS,
)
app.add_middleware(SessionMiddleware, secret_key=app_settings.SESSION_SECRET_KEY)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=app_settings.ALLOWED_HOSTS)

app.include_router(organizations_router, prefix="/api/v1")
app.include_router(boards_router, prefix="/api/v1")
app.include_router(boards_state_history_router, prefix="/api/v1")