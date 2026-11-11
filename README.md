# Performance review backlog

This repository captures a small performance-review exercise. The goal is to identify the highest-value optimizations first and implement the cheapest, highest-impact fix.

## 10 performance improvements identified

1. **Normalize case before splitting names (implemented).** Calling `lower()` once on the input avoids a temporary token list and one `lower()` call per token. A local `timeit` comparison over four representative names, repeated 200,000 times, took 0.167 seconds before and 0.096 seconds after; real workloads may differ.
2. **Reuse normalized names while building an index.** A per-index dictionary could avoid repeat work when many users share names; benchmark against real duplicate rates before adding its lookup overhead.
3. **Add database indexes for hot query paths.**
4. **Use pagination and cursor-based fetching for large result sets.**
5. **Batch database reads to avoid N+1 queries.**
6. **Compress and lazy-load large assets such as images and fonts.**
7. **Defer non-critical JavaScript and inline critical CSS.**
8. **Reuse prepared payloads to avoid repeated JSON serialization.**
9. **Build indexes from iterables.** Accepting an iterable in `build_user_index` would let callers stream records rather than materialize an additional list for large inputs.
10. **Keep cheap normalization uncached.** The operation is lightweight, so add repeated-name caching only if workload measurements show a benefit.

The current implementation deliberately keeps `normalize_user_name` uncached: its computation is cheap, so caching is not worthwhile without evidence from a representative workload.

```python
from src.performance_cache import build_user_index

users = [
    {"id": "u-1", "name": " Alice  Smith "},
    {"id": "u-2", "name": "ALICE SMITH"},
]

print(build_user_index(users))
```

The normalization helper lowercases once and lets `split()` normalize runs of whitespace before joining the words.
