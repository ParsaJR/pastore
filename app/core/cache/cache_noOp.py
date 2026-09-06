
from app.core.cache.cache_interface import Cache


class NoOPCache(Cache):
    """A Cache Implementation that does no operation."""
    async def get(self, key: str) -> bytes | None:
        return None

    async def set(self, key: str, value: str, ttl: int) -> None:
        return None

    async def delete(self, key: str) -> None:
        return None
