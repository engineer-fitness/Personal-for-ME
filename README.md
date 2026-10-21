# Performance review backlog

This repository captures a small performance-review exercise. The goal is to identify the highest-value optimizations first and implement the cheapest, highest-impact fix.

## 10 performance improvements identified

1. **Normalize case before splitting names (implemented).** Calling `lower()` once on the input avoids a temporary token list and one `lower()` call per token. A local `timeit` comparison over four representative names, repeated 200,000 times, took 0.167 seconds before and 0.096 seconds after; real workloads may differ.
2. **Reuse normalized names while building an index.** A per-index dictionary could avoid repeat work when many users share names; benchmark against real duplicate rates before adding its lookup overhead.
3. **Fast-path hashable tuples in `_freeze`.** Tuples are recursively traversed before the existing hashability check, even when the tuple is already a valid key.
4. **Specialize memoization for common call shapes.** `memoize` binds arguments, applies defaults, sorts names, and recursively freezes values on every lookup; a simpler path for fixed, positional scalar arguments could reduce that overhead.
5. **Use `functools.lru_cache` for hashable-only functions.** The generic `memoize` decorator supports nested mutable inputs, but that flexibility costs more than a native cache for simpler functions.
6. **Avoid default binding when it is unnecessary.** `apply_defaults()` is needed to make omitted and explicit defaults share a key, but functions without defaults could skip that work.
7. **Reduce canonical-key sorting for restricted signatures.** Sorting makes keyword and positional forms equivalent; decorators with a narrower call contract could avoid sorting and key reconstruction.
8. **Bound cache growth.** `memoize` retains every result indefinitely; a bounded cache can prevent memory pressure and garbage-collection cost for long-lived, high-cardinality functions.
9. **Build indexes from iterables.** Accepting an iterable in `build_user_index` would let callers stream records rather than materialize an additional list for large inputs.
10. **Keep cheap normalization uncached.** The generic cache-key construction can outweigh this short string operation, so normalization should remain direct unless workload measurements show repeated-name caching wins.

The current implementation deliberately keeps `normalize_user_name` uncached: its computation is cheap, and memoization would add signature binding, key construction, and cache access without reliably avoiding enough work.

```python
from src.performance_cache import build_user_index

users = [
    {"id": "u-1", "name": " Alice  Smith "},
    {"id": "u-2", "name": "ALICE SMITH"},
]

print(build_user_index(users))
```

The normalization helper lowercases once and lets `split()` normalize runs of whitespace before joining the words.
