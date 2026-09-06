import redis.asyncio as redis

from app.core.cache.cache_interface import Cache


class RedisCache(Cache):
    def __init__(self, redis: redis.Redis):
        self.redis = redis

    async def get(self, key: str) -> str | bytes | None:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ttl: int) -> None:
        await self.redis.set(key, value, ex=ttl)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)
