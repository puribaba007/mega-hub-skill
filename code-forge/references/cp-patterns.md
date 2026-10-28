# Competitive programming — pattern picker and WA/TLE checklist

## Choose complexity from n (≈10^8 ops/sec)
| n up to | Target | Typical techniques |
|---|---|---|
| 10–20 | O(2^n), O(n!) | bitmask DP, backtracking, meet-in-the-middle |
| 100–500 | O(n^3) | Floyd–Warshall, interval/matrix DP |
| 2,000–5,000 | O(n^2) | DP, two nested loops |
| 10^5–10^6 | O(n log n) | sort, binary search, segment tree/BIT, heap, DSU |
| 10^6–10^7 | O(n) / O(n log log n) | prefix sums, two pointers, sieve, hashing |
| 10^9+ | O(log n) / O(1) | math/closed form, fast exponentiation |

## Pattern by signal
- "k-th / smallest value that works" → **binary search on the answer**.
- "contiguous subarray/substring" → **sliding window / two pointers / prefix sums**.
- "shortest path" → BFS (unweighted), Dijkstra (non-neg), Bellman-Ford (neg), Floyd (all-pairs).
- "connected / groups / cycles" → **DSU** or DFS/BFS.
- "count ways / min cost over choices" → **DP**; define state + transition + base case.
- "ranges with updates" → **Fenwick / segment tree** (lazy for range updates).
- "pattern in string" → KMP, Z-function, or polynomial hashing.
- "max matching / max flow" → Hopcroft-Karp / Dinic.
- "primes / divisors / modular" → sieve, modpow, modular inverse, CRT.

## Debugging WA (wrong answer)
1. Re-read the statement: off-by-one, 1- vs 0-indexed, output format, multiple test cases.
2. Overflow: use `long long`; watch `a*b` and sums.
3. Edge cases: n=0/1, all equal, max values, negatives, empty, duplicates.
4. **Stress test** (see cp-templates.md) brute vs fast on random small inputs — it will print a failing case.

## Debugging TLE (time limit exceeded)
1. Recompute the complexity against n (table above) — you probably need a lower class, not micro-tweaks.
2. C++: fast I/O (`sync_with_stdio(false)`), avoid `endl` (use `"\n"`), pass by reference, reserve vectors.
3. Python: use PyPy, `sys.stdin`, avoid per-char work, prefer built-ins/`array`/`bisect`.
4. Remove accidental O(n^2) (e.g. `string +=` in a loop, repeated `.count()`/`in` on lists).

## Memory (MLE)
Prefer `int` over `long long` when safe, iterative over deep recursion, rolling DP arrays,
and free big structures between test cases.
