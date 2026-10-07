from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def _freeze(value: Any) -> Any:
    """Convert nested Python values into hashable cache keys."""
    if isinstance(value, dict):
        return tuple(sorted((str(key), _freeze(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    try:
        hash(value)
    except TypeError:
        if hasattr(value, "__dict__"):
            return tuple(sorted((key, _freeze(item)) for key, item in vars(value).items()))
        return repr(value)
    return value


def memoize(fn: Callable[..., R]) -> Callable[..., R]:
    """Cache repeated results using a canonical key built from the call arguments.

    The cache key is based on the bound function arguments rather than a single value,
    so repeated calls with equivalent positional or keyword inputs share the same result.
    """
    signature = inspect.signature(fn)
    cache: dict[tuple[tuple[str, Any], ...], R] = {}

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        key = tuple(sorted((name, _freeze(value)) for name, value in bound.arguments.items()))
        if key not in cache:
            cache[key] = fn(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache  # type: ignore[attr-defined]
    wrapper.cache_clear = cache.clear  # type: ignore[attr-defined]
    return wrapper


@memoize
def normalize_user_name(raw_name: str) -> str:
    """Normalize a user name with a small amount of expensive text processing."""
    tokens = [token.lower() for token in raw_name.strip().split()]
    return " ".join(tokens)


def build_user_index(users: list[dict[str, str]]) -> dict[str, str]:
    """Build a lookup map using the memoized normalization helper."""
    index: dict[str, str] = {}
    for user in users:
        index[user["id"]] = normalize_user_name(user["name"])
    return index
