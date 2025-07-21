from redis.asyncio import Redis
import orjson


class RedisClient:
    def __init__(self, redis_url: str) -> None:
        self.redis = Redis.from_url(redis_url)

    async def get(self, key: str) -> dict[dict, int] | None:
        data = await self.redis.get(key)
        return orjson.loads(data) if data else None
    
    async def set(self, key: str, value: dict, expire_seconds: int = 3600) -> None:
        await self.redis.set(key, orjson.dumps(value), ex=expire_seconds)
    
    async def close(self):
        await self.redis.close()
