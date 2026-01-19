from app.configs.base_config import app_settings
from app.utils.redis_manager import RedisManager


redis_manager = RedisManager(host=app_settings.REDIS_HOST, port=app_settings.REDIS_PORT)
