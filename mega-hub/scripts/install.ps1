# Mega Hub installer - adds the official Claude plugin marketplace and the core plugins.
# Default is a dry run (prints the commands). Run with -Apply to execute them.
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Apply
#
# Every plugin below is verified to exist on the official marketplace
# (https://www.claudemarket.ai/plugins/anthropics-claude-plugins-official/<name>).
# The marketplace token used for install is "anthropics-claude-plugins-official".
# If your Claude Code already has the official marketplace under a different name,
# the per-plugin URLs printed at the end let you install any of these by hand.
param([switch]$Apply)

$marketplace = 'anthropics-claude-plugins-official'
$marketplaceAdd = 'claude plugin marketplace add anthropics/claude-plugins-official'
$plugins = @(
  'superpowers',
  'frontend-design',
  'feature-dev',
  'pr-review-toolkit',
  'hyperframes',
  'playground',
  'mcp-server-dev',
  'chrome-devtools-mcp',
  'mattpocock-skills',
  'notion'
)

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  Write-Host 'Claude Code CLI not found. Install it first: npm install -g @anthropic-ai/claude-code'
  Write-Host 'You can still install any plugin from its page (URLs printed below).'
}

function Run($cmd) {
  if ($Apply) {
    Write-Host ">> $cmd"
    try { Invoke-Expression $cmd } catch { Write-Host "   skipped: $($_.Exception.Message)" }
  } else {
    Write-Host "[dry run] $cmd"
  }
}

Run $marketplaceAdd
foreach ($p in $plugins) { Run "claude plugin install $p@$marketplace" }

if (-not $Apply) { Write-Host "`nNothing installed. Re-run with -Apply to install." }

Write-Host "`nPlugin pages (install any of these by hand if a name differs):"
foreach ($p in $plugins) { Write-Host "  $p  ->  https://www.claudemarket.ai/plugins/anthropics-claude-plugins-official/$p" }
Write-Host "`nConnectors need your own sign-in: Claude app > Settings > Connectors (see references/connectors.md)."
Write-Host "Find more skills/plugins live via the 'MCP & Skills Finder' connector."
