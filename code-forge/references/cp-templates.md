# Competitive programming templates

## C++17 template (fast I/O)
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
#define all(x) (x).begin(), (x).end()

void solve() {
    int n; cin >> n;
    vector<ll> a(n);
    for (auto &x : a) cin >> x;
    // ... solution ...
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t = 1;
    cin >> t;              // remove if single test case
    while (t--) solve();
    return 0;
}
```

## Python template (fast I/O; run with PyPy when available)
```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    # ... solution ...

def main():
    t = int(input())      # remove if single test case
    for _ in range(t):
        solve()

main()
```

## Useful snippets (C++)
```cpp
// DSU
struct DSU {
    vector<int> p, r;
    DSU(int n): p(n), r(n, 0) { iota(all(p), 0); }
    int find(int x){ return p[x]==x ? x : p[x]=find(p[x]); }
    bool uni(int a,int b){ a=find(a); b=find(b); if(a==b) return false;
        if(r[a]<r[b]) swap(a,b); p[b]=a; if(r[a]==r[b]) r[a]++; return true; }
};

// Fenwick (BIT)
struct BIT {
    int n; vector<ll> t;
    BIT(int n): n(n), t(n+1, 0) {}
    void add(int i, ll v){ for(++i;i<=n;i+=i&-i) t[i]+=v; }
    ll sum(int i){ ll s=0; for(++i;i>0;i-=i&-i) s+=t[i]; return s; }
};

// binary search on answer
ll lo=0, hi=1e18;
while(lo<hi){ ll mid=(lo+hi)/2; if(ok(mid)) hi=mid; else lo=mid+1; }
// lo is the smallest value with ok(lo)==true
```

## Stress-test harness (bash) — find a failing case
Compile `fast` (your solution) and `brute` (obvious slow-but-correct), write `gen.py` (random input).
```bash
for i in $(seq 1 10000); do
  python gen.py $i > in.txt
  ./fast < in.txt > out1.txt
  ./brute < in.txt > out2.txt
  if ! diff -q out1.txt out2.txt >/dev/null; then
    echo "MISMATCH on test $i"; cat in.txt; break
  fi
done
```
`gen.py` uses the test index as a seed so a failing case is reproducible.
