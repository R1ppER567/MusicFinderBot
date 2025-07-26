from aiogram import BaseMiddleware
from db.redis_client import RedisClient


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def __call__(self, handler, event, data):
        data['redis'] = self.redis_client
        return await handler(event, data)
