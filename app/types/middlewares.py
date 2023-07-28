from typing import Any, Awaitable, Callable, Dict, TypeVar

T = TypeVar("T")

Handler = Callable[[T, Dict[str, Any]], Awaitable[Any]]
Data = Dict[str, Any]
MiddlewareReturnType = Any
