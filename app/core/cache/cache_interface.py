# Python doesn't have a triditional OOP like Java. Python does oop by a class-based approach.
# Here i define a "Cache" class, which acts similar to the Golang's Interfaces.
# It says "Anything calls itself a Cache, should provide these three methods".
class Cache():
    """Cache is a abstract class that describes a generic Cache implementation"""
    async def get(self, key: str) -> str | bytes | None:
        ...

    async def set(self, key: str, value: str, ttl: int) -> None:
        ...

    async def delete(self, key: str) -> None:
        ...
