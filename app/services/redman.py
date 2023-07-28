from redis.asyncio import Redis


class Redman:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_openai_keys(self) -> set[str]:
        result: set[bytes] = await self.redis.smembers("openai_keys")
        return {x.decode() for x in result}

    async def get_random_openai_key(self) -> str | None:
        # Remove "noqa" when normal async method will be added
        result = await self.redis.srandmember("openai_keys")  # noqa
        return result.decode() if result else None

    async def add_openai_key(self, *keys: str) -> None:
        await self.redis.sadd("openai_keys", *keys)

    async def remove_openai_key(self, *keys: str) -> None:
        await self.redis.srem("openai_keys", *keys)

    async def get_enable_streaming(self) -> bool:
        return bool(int(await self.redis.get("enable_streaming") or True))

    async def toggle_streaming(self) -> bool:
        await self.redis.set(
            "enable_streaming", int(not await self.get_enable_streaming())
        )
        return await self.get_enable_streaming()
