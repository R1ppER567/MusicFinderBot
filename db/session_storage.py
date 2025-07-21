from db.redis_client import RedisClient


def build_key(user_id: int, message_id: int) -> str:
    return f'session:{user_id}:{message_id}'


async def loads_data(
    redis: RedisClient, 
    user_id: int, 
    message_id: int
) -> dict[dict, int] | None:
    key = build_key(user_id, message_id)
    return await redis.get(key)


async def save_tracks(
        redis: RedisClient, 
        user_id: int, 
        message_id: int, 
        tracks: list[dict], 
        page: int = 1
) -> None:
    key = build_key(user_id, message_id)
    await redis.set(key, {'tracks': tracks,'page': page})


async def get_tracks(
        redis: RedisClient, 
        user_id: int, 
        message_id: int
) -> tuple[list[dict], int] | None:
    data = await loads_data(redis, user_id, message_id)
    return data['tracks'], data['page'] if data else None


async def update_page(
        redis: RedisClient, 
        user_id: int, 
        message_id: int, 
        page: int
) -> None:
    data = await loads_data(redis, user_id, message_id)
    if data:
        await save_tracks(user_id, message_id, data['tracks'], page)
