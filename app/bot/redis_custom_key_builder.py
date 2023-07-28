from typing import Literal

from aiogram.fsm.storage.base import DEFAULT_DESTINY, StorageKey
from aiogram.fsm.storage.redis import KeyBuilder


class UserIdKeyBuilder(KeyBuilder):
    def __init__(
        self,
        *,
        prefix: str = "fsm",
        separator: str = ":",
        with_bot_id: bool = False,
        with_destiny: bool = False,
    ) -> None:
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_destiny = with_destiny

    def build(
        self, key: StorageKey, part: Literal["data", "state", "lock"]
    ) -> str:
        parts = [self.prefix]
        if self.with_bot_id:
            parts.append(str(key.bot_id))
        # Ignores chat_id, so each message of user will be isolated
        parts.extend(["custom", str(key.user_id)])
        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(_wrong_destiny)
        parts.append(part)
        return self.separator.join(parts)


_wrong_destiny = (
    "Redis key builder is not configured "
    "to use key destiny other the default.\n"
    "\n"
    "Probably, you should set `with_destiny=True` in for DefaultKeyBuilder.\n"
    "E.g: `RedisStorage(redis, "
    "key_builder=DefaultKeyBuilder(with_destiny=True))`"
)
