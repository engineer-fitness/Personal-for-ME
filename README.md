# Performance review backlog

This repository captures a small performance-review exercise. The goal is to identify the highest-value optimizations first and implement the cheapest, highest-impact fix.

## 10 performance improvements to consider

1. Memoize repeated expensive computations.
2. Add database indexes for hot query paths.
3. Use pagination and cursor-based fetching for large result sets.
4. Reduce N+1 query patterns by batching reads.
5. Cache frequently requested static content at the edge or in memory.
6. Compress and lazy-load large assets such as images and fonts.
7. Defer non-critical JavaScript and inline critical CSS.
8. Avoid repeated JSON serialization by reusing prepared payloads.
9. Prefer async I/O for external API calls and queue-backed jobs.
10. Replace repeated string operations with batch processing and tuple/list reuse.

## Implemented improvement

This branch includes a memoization-based optimization for repeated, expensive text normalization.

```python
from src.performance_cache import build_user_index

users = [
    {"id": "u-1", "name": " Alice  Smith "},
    {"id": "u-2", "name": "ALICE SMITH"},
]

print(build_user_index(users))
```

The underlying function caches normalized names so repeated calls avoid redoing the same work.
