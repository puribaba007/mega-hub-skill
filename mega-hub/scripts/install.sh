#!/usr/bin/env bash
# Mega Hub installer (Mac/Linux). Dry run by default; pass --apply to execute.
set -u
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
cmds=(
  "claude plugin marketplace add anthropics/claude-plugins-official"
  "claude plugin marketplace add anthropics/skills"
  "claude plugin install document-skills@anthropic-agent-skills"
  "claude plugin marketplace add obra/superpowers-marketplace"
  "claude plugin install superpowers@superpowers-marketplace"
  "claude plugin install frontend-design@claude-plugins-official"
  "claude plugin install feature-dev@claude-plugins-official"
  "claude plugin install pr-review-toolkit@claude-plugins-official"
  "claude plugin install hyperframes@claude-plugins-official"
  "claude plugin install playground@claude-plugins-official"
  "claude plugin install mcp-server-dev@claude-plugins-official"
  "claude plugin install chrome-devtools-mcp@claude-plugins-official"
  "claude plugin install mattpocock-skills@claude-plugins-official"
  "claude plugin install notion@claude-plugins-official"
)
command -v claude >/dev/null || { echo "Install Claude Code first: npm install -g @anthropic-ai/claude-code"; exit 1; }
for c in "${cmds[@]}"; do
  if [ $APPLY = 1 ]; then echo ">> $c"; $c || echo "   skipped"; else echo "[dry run] $c"; fi
done
[ $APPLY = 1 ] || echo "Nothing installed. Re-run with --apply."
