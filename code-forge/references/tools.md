# Code Forge — free tools by mode (install commands)

Windows: `winget install <id>` or `choco install <id>`. Mac: `brew install <id>`.
Python tools: `pip install <id>`. Node: `npm i -g <id>`.

## Replica (UI rebuild)
- Chromium / Playwright: `pip install playwright && playwright install`
- httrack (static copy of your own site): `winget install HTTrack.WinHTTrack`
- wget: `winget install JernejSimoncic.Wget`
- Penpot (open-source design): https://penpot.app (self-host or free cloud)
- Plugins: `clone-website`, `superdesign`, `figma`, `firecrawl`, `actionbook`

## Reverse engineering (authorized / CTF / learning)
- Ghidra: https://ghidra-sre.org (free NSA decompiler)
- radare2 / rizin + Cutter: `winget install rizin.rizin` ; Cutter from rizin.re
- GDB + pwndbg: `pip install pwndbg` (Linux/WSL) ; GEF alternative
- pwntools: `pip install pwntools`
- Frida: `pip install frida-tools`
- Binary triage: `binwalk` (`pip install binwalk`), Detect It Easy (DIE)
- .NET: ILSpy / dnSpyEx ; Java & Android: `jadx`, `apktool`
- Network: Wireshark (`winget install WiresharkFoundation.Wireshark`)
- Firmware/emulation: QEMU (`winget install SoftwareFreedomConservancy.QEMU`)
- Symbolic exec / memory forensics: angr (`pip install angr`), Volatility 3 (`pip install volatility3`)
- Plugins: `ghidra`, `reverse-engineering`, `systems-programming`

## Competitive programming
- Compilers: GCC/Clang (`winget install mingw` / `brew install gcc`), Python + PyPy
- VS Code + Competitive Companion (parse problems to files)
- cf-tool: https://github.com/xalanq/cf-tool (Codeforces submit/test)
- online-judge-tools: `pip install online-judge-tools` (download tests, test, submit)
- hyperfine (benchmark): `winget install sharkdp.hyperfine`
- Plugins: `cppcheatsheet`, `context7`, `b3ehive`, `competitive-ai-frameworks`

## Pro workflow
- perf / py-spy (`pip install py-spy`) / hyperfine for profiling
- pre-commit (`pip install pre-commit`), ruff, clang-tidy
- Plugins: `mattpocock-skills`, `pr-review-toolkit`, superpowers
