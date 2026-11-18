# Performance review backlog

This repository captures a small performance-review exercise.

## 10 performance improvements identified

1. **Use a normalized-name fast path.** Already-normalized names avoid `split()` and `join()` allocations.
2. **Reuse normalized names within an index build.** A per-index cache removes repeat normalization work for duplicate names.
3. **Add database indexes for hot query paths.**
4. **Use cursor-based pagination for large result sets.**
5. **Batch database reads to avoid N+1 queries.**
6. **Compress and lazy-load large assets.**
7. **Defer non-critical JavaScript and inline critical CSS.**
8. **Reuse prepared payloads to avoid repeated JSON serialization.**
9. **Stream index inputs instead of materializing a list.**
10. **Move to asynchronous I/O for latency-bound operations.**
