---
name: code-forge
description: All-in-one advanced coding skill - Replica (rebuild a website or app UI from a URL or screenshots you are allowed to use), reverse engineering for authorized security work, CTF and learning (your own binaries, APKs, firmware), competitive programming (Codeforces, LeetCode, AtCoder - patterns, templates, stress testing), and pro engineering workflow (TDD, debugging, review, performance). Use when the user says "replica", "clone this UI", "rebuild this layout", "reverse engineer", "decompile", "analyze this binary/APK", "CTF", "crackme", "competitive programming", "Codeforces", "LeetCode", "solve this problem", "TLE/WA", "optimize this algorithm", or "code-forge".
---

# Code Forge — Replica + Reverse Engineering + Competitive Coding

Pick the mode from the request and follow that section. These are the "actively competitive
coding" tools in one place. Each mode names the free tools and the best existing skills to chain.

## Scope and ethics (read first)
- **Reverse engineering** here is for work you are authorized to do: your own software, CTF
  challenges, crackmes, malware analysis in a sandbox, interoperability, and defensive research.
  Do not use it to defeat another product's protections, piracy, or to attack systems you don't own.
- **Replica** rebuilds layout/UI for learning or for sites you own or have permission to copy.
  Don't reproduce someone's trademarks, copy, images, or brand as if it were yours, and don't
  clone a site to deceive users (phishing, fake stores). Build the structure; use your own content.
- If a request crosses these lines, say so and offer the legitimate version.

## Mode 1 — Replica (rebuild a UI)
Goal: turn a URL or screenshots into clean, editable code.
1. Capture: built-in browser (`navigate` + `get_page_text`/`read_page`) or Chrome tools to read
   structure; screenshots for layout. For your own site, read the source directly.
2. Rebuild: use `frontend-design` (or `superdesign`, `waza-design`) to generate production-grade
   HTML/CSS or a Next.js/React version — match layout, spacing, typography, responsive breakpoints.
3. Verify: preview with the browser pane; compare side by side; swap in the user's own copy/assets.
- Chain skills: `frontend-design`, `superpowers:brainstorming` (scope), `artifact-design`.
- Plugins to install for this: `clone-website` (sharegpu), `superdesign`, `figma`, `firecrawl`/`brightdata-plugin` (read pages), `actionbook` (selectors).
- Free tools: Chromium devtools, Playwright, `wget`/`httrack` (static capture of your own site), Penpot.

## Mode 2 — Reverse engineering (authorized / CTF / learning)
Goal: understand how a binary or app works.
1. Triage: file type, strings, hashes, packers. Tools: `file`, `strings`, `binwalk`, `Detect It Easy`.
2. Static: disassemble/decompile. Tools: **Ghidra**, Cutter/rizin, radare2, objdump; .NET → ILSpy/dnSpy;
   Java/APK → jadx, apktool; Python → decompyle3/uncompyle6.
3. Dynamic: run in a VM/sandbox. Tools: x64dbg/GDB+pwndbg, Frida, strace/ltrace, Wireshark (protocols),
   QEMU (firmware), Android emulator.
4. Document findings and, for CTF, derive the solution/flag.
- Chain skills: `superpowers:systematic-debugging`, `code-forge` (this), security-review.
- Plugins to install: `ghidra` (und3rf10w-ai-ghidra-tools), `reverse-engineering` (77svene-nexus),
  `systems-programming` (77svene-nexus), `cppcheatsheet`.
- Free tools: Ghidra, radare2/rizin+Cutter, GDB+pwndbg+GEF, pwntools, Frida, jadx, apktool, Wireshark, QEMU, angr, Volatility.

## Mode 3 — Competitive programming
Goal: solve and optimize contest problems.
1. Read limits (n, time, memory) → target complexity before coding.
2. Pattern match: two pointers, binary search, DP, graphs (BFS/DFS/Dijkstra/DSU), greedy, number theory,
   segment tree/Fenwick, strings (KMP/Z/hashing), flows. See `references/cp-patterns.md`.
3. Use the templates in `references/cp-templates.md` (C++17 fast I/O, Python speedups).
4. Before submit: test edge cases, then **stress test** (brute vs fast on random inputs) to catch WA;
   for TLE, cut the complexity, not micro-tweaks. See `references/cp-patterns.md` "Debugging WA/TLE".
- Chain skills: `superpowers:test-driven-development` (stress harness), `code-mentor`.
- Plugins to install: `cppcheatsheet`, `context7` (docs), `b3ehive`/`competitive-ai-frameworks` (multi-agent solve).
- Free: GCC/Clang, Python+PyPy, CP editor (VS Code + Competitive Companion), cf-tool, oj (online-judge-tools).

## Mode 4 — Pro engineering workflow (always available)
TDD → implement → review → verify. Chain: `superpowers:writing-plans` →
`superpowers:test-driven-development` → `code-review` / `pr-review-toolkit` →
`superpowers:verification-before-completion`. Debugging: `superpowers:systematic-debugging`.
Performance: profile first (perf, py-spy, hyperfine), then optimize the hot path.

## Files
- `references/cp-patterns.md` — algorithm patterns by constraint, and a WA/TLE checklist
- `references/cp-templates.md` — ready C++ and Python contest templates + a stress-test harness
- `references/tools.md` — every tool above, with install commands, grouped by mode
