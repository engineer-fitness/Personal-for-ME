from src.performance_cache import build_user_index, memoize


def test_memoize_reuses_result_for_same_key() -> None:
    calls = {"count": 0}

    @memoize
    def expensive_lookup(value: str) -> str:
        calls["count"] += 1
        return value.upper()

    assert expensive_lookup("alice") == "ALICE"
    assert expensive_lookup("alice") == "ALICE"
    assert calls["count"] == 1


def test_build_user_index_uses_normalized_names() -> None:
    users = [
        {"id": "u-1", "name": " Alice  Smith "},
        {"id": "u-2", "name": "ALICE SMITH"},
    ]

    index = build_user_index(users)

    assert index == {"u-1": "alice smith", "u-2": "alice smith"}
