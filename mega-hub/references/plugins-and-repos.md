# Plugins (100+) and where to get them — all free to install

Every plugin below is a real listing on the MCP & Skills Finder directory (claudemarket.ai, Oct 2026).
Open the listing link for its exact install command. The general pattern in Claude Code is:

```
/plugin marketplace add <github-owner>/<repo>
/plugin install <plugin-name>@<marketplace-name>
```

The official marketplace comes pre-added: `/plugin install <name>@claude-plugins-official`.
Plugin = free; some connect to a service that has its own (often free-tier) account.

Listing base: `https://www.claudemarket.ai/plugins/<marketplace>/<plugin>`

## A. Official Anthropic marketplace (`anthropics-claude-plugins-official`) — 45
| Plugin | Use |
|---|---|
| hyperframes | HTML → video, captions, voiceover |
| runway-api | Video/image/audio generation |
| togetherai-skills | Open-model inference, image/video gen |
| frontend-design | Production-grade UI |
| feature-dev | Feature workflow with agents |
| pr-review-toolkit | PR review agents |
| mattpocock-skills | TDD, specs, code review |
| chrome-devtools-mcp | Drive/inspect Chrome |
| modern-web-guidance | Web best practices |
| playground | Interactive HTML playgrounds |
| mcp-server-dev | Build MCP servers |
| project-artifact | Live project status page |
| superdesign | UI + marketing graphics canvas |
| figma | Figma design → code |
| notion | Notion workspace |
| linear | Linear issues |
| slack | Slack search/messages |
| gitlab | GitLab repos, MRs, CI |
| firebase | Firestore, auth, hosting |
| airtable | Airtable ops database |
| looker | Looker / LookML |
| bigquery-data-analytics | BigQuery |
| cloud-sql-postgresql | Cloud SQL Postgres |
| alloydb | AlloyDB |
| spanner | Spanner |
| firestore-native | Firestore |
| google-cloud-storage | GCS buckets |
| knowledge-catalog | Data catalog |
| data-agent-kit-starter-pack | Google Cloud data engineering |
| railway | Deploy on Railway |
| netlify-skills | Netlify functions, deploy |
| mongodb-atlas | MongoDB Atlas |
| qdrant-skills | Vector search |
| aiven | Managed Postgres/Kafka (free tier) |
| lovable | Lovable apps |
| hostinger | Hosting, domains |
| aws-startup-advisor | AWS for startups |
| sagemaker-ai | AWS ML |
| amazon-location-service | Maps, geocoding |
| pigment | Business planning |
| coderabbit | AI code review |
| sonarqube | Code quality + security |
| qt-development-skills | Qt C++/QML |
| quarkus-agent | Quarkus Java |
| noibu | E-commerce errors/revenue |
| brightdata-plugin | Web scraping, Google search |
| learn-with-coursera | Learning paths |

## B. Anthropic Claude Code repo (`anthropics-claude-code`) — 3
feature-dev · frontend-design · pr-review-toolkit

## C. Design (`owl-listener-designer-skills`, `nexu-io-open-design`, `tw93-waza`) — 15
design-ops · design-research · design-systems · designer-toolkit · interaction-design · prototyping-testing · ui-design · ux-strategy · open-design (139 skills) · waza · waza-design · waza-think

## D. Video, media & YouTube — 14
youtube-transcript (intellectronica-agent-skills) · youtube (jcodesmore-jcodesmore-plugins) · skillkit (sacredvoid-skillkit: SVG logos, local Stable Diffusion, transcription) · golpo (golpo-ai-golpo-claude-skill) · notebooklm-enhanced (fakoli-fakoli-plugins) · product-video-creation · smart-screen-recorder (abhattacherjee-claude-code-skills) · video-tools (machine-intelligence-claude-code-plugins) · twelvelabs (teraflop-inc-twelvelabs-claude-plugin) · livekit-agent-skills · nano-banana-2 · nano-banana-pro (intellectronica-agent-skills) · editgeo · utilities (shaharsha-claude-skills)

## E. Google Workspace (G Suite) — 5
gws (fakoli-fakoli-plugins: Gmail, Calendar, Drive, Docs, Sheets, Slides, Meet — 100 skills) · gog-cli (intellectronica-agent-skills) · omriariav-workspace-cli · shaharsha-skills (gdoc-sync, gslides-sync, gsheets) · plus built-in skill `anthropic-skills:google-workspace`

## F. Marketing, SEO & sales — 22
firecrawl (official Firecrawl) · seo-dungeon (avalonreset) · marketing-skills (fianchettogianni, 40 skills) · marketing (alvarovillalbaa) · ad-alchemist · community-pulse · opportunity-master (zuttam-business-growth-mp) · ink · pitch-copy · pitch-landing · pitch-launch · pitch-message · pitch-position · pitch-recon (tonone-ai-tonone) · content-marketing · seo-analysis-monitoring · seo-content-creation · seo-technical-optimization (77svene-nexus) · antigravity-bundle-marketing-growth · antigravity-bundle-business-analyst (mit-network-antigravity-awesome-skills) · oxylabs · super-claudio

## G. C-suite, business & finance — 18
soleur (jikig-ai-soleur: full AI org — eng, finance, marketing, legal, ops, sales) · mint (tonone: P&L, runway, fundraising) · startup-business-analyst (77svene-nexus) · quantitative-trading (77svene-nexus) · business-health-diagnostic · acquisition-channel-advisor · feature-investment-advisor · finance-based-pricing-advisor · finance-metrics-quickref · saas-economics-efficiency-metrics · saas-revenue-growth-metrics (deanpeters-product-manager-skills) · cfa-core (227 offline finance tools) · market-intelligence · quant-trading-system (jmanhype) · axiom-product-management · financial-planner · xlsx · skill-creator (kimonarrow-ledgerskills)

## H. Coding, DevOps & agents — 22
beads (issue tracker) · prompts.chat · context-engineering (muratcankoylan) · headroom (context compression) · codeguard-security · code-critic · handoff · agent-session-resume · darkroom · emerging-techniques (orchestra-research) · relay · relay-audit · relay-deploy · relay-pipeline · relay-recon · relay-ship · flux-migrate · feat (tonone-ai-tonone) · axiom-devops-engineering · axiom-web-backend (tachyon-beep-skillpacks) · voltagent-infra · linux-shell-scriptor · devops-automation

## I. Compliance — 3
eu-ai-act · ccpa (sushegaad-claude-skills-governance-risk-and-compliance) · wooyun-legacy (security testing methodology)

## J. Mega bundles (many skills in one install)
claude-skills-collection (khalilbenaz: 349 skills, 34 domains) · open-design (139) · gws (100) · superpowers (obra/superpowers) · skills-selector (andersonlimahw-lemon-ai-hub)

**Total: 140+ plugins.** Find more live: MCP & Skills Finder `search_plugins`.

## GitHub repos behind the skills already in this bundle
- `anthropics/skills` — docx, pdf, pptx, xlsx, skill-creator (official)
- `anthropics/claude-plugins-official` — official plugin marketplace
- `obra/superpowers` — superpowers process skills
- `ruvnet/claude-flow` — agentdb, swarm, sparc, flow-nexus, v3-* skills
- `modelcontextprotocol/servers` — reference MCP servers (filesystem, git, fetch, memory …)
