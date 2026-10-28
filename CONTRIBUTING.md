# Contributing to Mega Hub

Thanks for helping make Mega Hub better! This repo is a **router + catalog** of Claude skills,
connectors, plugins and free tools — so most contributions are edits to the catalog or the router.

## Ways to contribute
- **Add a tool** — a skill, MCP connector, plugin or free/open-source tool that belongs in a category.
- **Fix a name/URL** — marketplace tokens and connector URLs change; corrections are very welcome.
- **Improve the router** — a clearer role → tool mapping in `mega-hub/SKILL.md`.
- **New pipeline** — a useful end-to-end chain (like the YouTube / trading / launch ones).

## How
1. Fork and create a branch: `git checkout -b add-<thing>`.
2. Edit the right file:
   - Router/table → `mega-hub/SKILL.md`
   - Skills → `mega-hub/references/skills-catalog.md`
   - Connectors → `mega-hub/references/connectors.md`
   - Plugins → `mega-hub/references/plugins-and-repos.md`
   - Free tools → `mega-hub/references/free-ai-tools.md`
3. Keep entries **verified**: a real skill/plugin name, a working connector URL, a real tool.
   For plugins, confirm the install works (`claude plugin install <name>@<marketplace>`).
4. Open a PR using the template. Describe what you added and how you verified it.

## Rules
- **Free first.** Prefer free / open-source / free-tier options.
- **No secrets.** Never commit API keys, tokens or passwords.
- **Ethical scope.** `code-forge` reverse-engineering and Replica entries are for authorized /
  CTF / learning use only — nothing that defeats protections, enables piracy or deceives users.
- Be accurate over exhaustive: a wrong name hurts more than a missing one.

By contributing you agree your work is released under the repo's MIT License.
