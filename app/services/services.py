import redis
from typing import Optional, Tuple
from app.config.config import settings
from app.utils.logging import logger

class RedisService:
    
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_timeout=settings.REDIS_TIMEOUT,
                socket_connect_timeout=settings.REDIS_CONNECT_TIMEOUT
            )
            logger.info(f"Подключение к Redis установлено: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        except Exception as e:
            logger.error(f"Ошибка подключения к Redis: {e}")
            raise
    
    async def get_address_by_phone(self, phone: str) -> Tuple[Optional[str], bool]:
        try:
            address = self.redis_client.get(phone)
            return address, True
        except redis.RedisError as e:
            logger.error(f"Ошибка при получении данных из Redis: {e}")
            return None, False
    
    async def save_phone_address(self, phone: str, address: str) -> bool:
        try:
            return bool(self.redis_client.set(phone, address))
        except redis.RedisError as e:
            logger.error(f"Ошибка при сохранении данных в Redis: {e}")
            return False
    
    async def delete_phone_address(self, phone: str) -> bool:
        try:
            return bool(self.redis_client.delete(phone))
        except redis.RedisError as e:
            logger.error(f"Ошибка при удалении данных из Redis: {e}")
            return False
            
    async def ping(self) -> bool:
        try:
            return bool(self.redis_client.ping())
        except redis.RedisError as e:
            logger.error(f"Ошибка при проверке доступности Redis: {e}")
            return False
