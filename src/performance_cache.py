from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def memoize(fn: Callable[[T], R]) -> Callable[[T], R]:
    """Cache repeated, expensive results for hashable inputs.

    This keeps the optimization cheap to apply: the function body remains unchanged,
    but repeated calls with identical arguments avoid redoing the same work.
    """
    cache: dict[T, R] = {}

    @wraps(fn)
    def wrapper(value: T) -> R:
        if value not in cache:
            cache[value] = fn(value)
        return cache[value]

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
