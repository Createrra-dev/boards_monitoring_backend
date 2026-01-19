import functools
import inspect
from logging.config import dictConfig

from app.configs.base_config import logging_settings
from fastapi.concurrency import run_in_threadpool
from udp_logger.apm.udp_apm import UdpAsyncAPMHandler


def setup_logging() -> None:
    dictConfig(logging_settings.LOGGING)


UDPHandler = UdpAsyncAPMHandler(
    udp_host=logging_settings.UDP_HOST,
    udp_port=logging_settings.UDP_PORT,
    server_name=logging_settings.SERVER_NAME,
)


def apm(func):
    if inspect.iscoroutinefunction(func):
        return UDPHandler.apm(func)

    @functools.wraps(func)
    async def _async_wrapper(*args, **kwargs):
        return await run_in_threadpool(func, *args, **kwargs)

    return UDPHandler.apm(_async_wrapper)
