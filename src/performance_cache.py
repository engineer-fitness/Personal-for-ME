from __future__ import annotations

from collections.abc import Iterable, Mapping


def _canonicalize_user_name(raw_name: str) -> str:
    """Normalize whitespace and casing in a user name."""
    return " ".join(raw_name.lower().split())


def normalize_user_name(raw_name: str) -> str:
    """Return a lowercase user name with normalized whitespace."""
    return _canonicalize_user_name(raw_name)


def build_user_index(users: Iterable[Mapping[str, str]]) -> dict[str, str]:
    """Build a lookup map with normalized user names, reusing repeated names."""
    index: dict[str, str] = {}
    normalized_cache: dict[str, str] = {}

    for user in users:
        raw_name = user["name"]
        normalized_name = normalized_cache.get(raw_name)
        if normalized_name is None:
            normalized_name = normalize_user_name(raw_name)
            normalized_cache[raw_name] = normalized_name
        index[user["id"]] = normalized_name
    return index
