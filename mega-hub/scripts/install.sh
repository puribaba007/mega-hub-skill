#!/usr/bin/env bash
# Mega Hub installer (Mac/Linux). Dry run by default; pass --apply to execute.
#
# Every plugin below is verified to exist on the official marketplace
# (https://www.claudemarket.ai/plugins/anthropics-claude-plugins-official/<name>).
# The marketplace token used for install is "anthropics-claude-plugins-official".
# If your Claude Code already has the official marketplace under another name,
# use the per-plugin URLs printed at the end to install any of these by hand.
set -u
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1

MARKET="anthropics-claude-plugins-official"
MARKET_ADD="claude plugin marketplace add anthropics/claude-plugins-official"
PLUGINS=(superpowers frontend-design feature-dev pr-review-toolkit hyperframes playground mcp-server-dev chrome-devtools-mcp mattpocock-skills notion)

command -v claude >/dev/null || {
  echo "Claude Code CLI not found. Install it first: npm install -g @anthropic-ai/claude-code"
  echo "You can still install any plugin from its page (URLs printed below)."
}

run() {
  if [ $APPLY = 1 ]; then echo ">> $1"; eval "$1" || echo "   skipped"; else echo "[dry run] $1"; fi
}

run "$MARKET_ADD"
for p in "${PLUGINS[@]}"; do run "claude plugin install $p@$MARKET"; done

[ $APPLY = 1 ] || echo "Nothing installed. Re-run with --apply."

echo ""
echo "Plugin pages (install any of these by hand if a name differs):"
for p in "${PLUGINS[@]}"; do echo "  $p  ->  https://www.claudemarket.ai/plugins/anthropics-claude-plugins-official/$p"; done
echo ""
echo "Connectors need your own sign-in: Claude app > Settings > Connectors (see references/connectors.md)."
echo "Find more skills/plugins live via the 'MCP & Skills Finder' connector."
