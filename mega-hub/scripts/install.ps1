# Mega Hub installer - adds the free plugin marketplaces and core plugins to Claude Code.
# Default is a dry run (prints the commands). Run with -Apply to execute them.
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Apply
param([switch]$Apply)

$commands = @(
  'claude plugin marketplace add anthropics/claude-plugins-official',
  'claude plugin marketplace add anthropics/skills',
  'claude plugin install document-skills@anthropic-agent-skills',
  'claude plugin marketplace add obra/superpowers-marketplace',
  'claude plugin install superpowers@superpowers-marketplace',
  'claude plugin install frontend-design@claude-plugins-official',
  'claude plugin install feature-dev@claude-plugins-official',
  'claude plugin install pr-review-toolkit@claude-plugins-official',
  'claude plugin install hyperframes@claude-plugins-official',
  'claude plugin install playground@claude-plugins-official',
  'claude plugin install mcp-server-dev@claude-plugins-official',
  'claude plugin install chrome-devtools-mcp@claude-plugins-official',
  'claude plugin install mattpocock-skills@claude-plugins-official',
  'claude plugin install notion@claude-plugins-official'
)

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Host 'Claude Code CLI not found. Install it first: npm install -g @anthropic-ai/claude-code'
  exit 1
}

foreach ($c in $commands) {
  if ($Apply) {
    Write-Host ">> $c"
    try { Invoke-Expression $c } catch { Write-Host "   skipped: $($_.Exception.Message)" }
  } else {
    Write-Host "[dry run] $c"
  }
}

if (-not $Apply) { Write-Host "`nNothing installed. Re-run with -Apply to install." }
Write-Host 'Connectors need your own sign-in: Claude app > Settings > Connectors (see references/connectors.md).'
