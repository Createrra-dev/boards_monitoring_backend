import aiohttp

from app.configs.base_config import app_settings

async def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{app_settings.BOT_TOKEN}/sendMessage"
    payload = {"chat_id": app_settings.GROUP_CHART_ID, "text": text}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return await resp.json()
