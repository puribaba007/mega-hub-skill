---
name: mega-hub
description: One-stop hub that routes ANY request to the right one of 300+ skills, 140+ connectors (MCP), plugins and free AI tools - CEO/strategy, marketing, YouTube, social media, trading and finance, data, coding, DevOps, design, video, audio, docs, sales/CRM, productivity. Use when the user says "mega hub", "which skill/tool should I use", "do X with the best tool", "install everything", "set up my toolkit", "find a connector for", or when a task spans several domains and you need to pick the right skills and connectors.
---

# Mega Hub — 300+ skills, connectors, plugins & free tools in one place

This skill is a **router + catalog**. It does not copy other skills' code into itself
(that would break when they update); instead it knows every tool, picks the right one,
and tells the user exactly how to switch on anything that is missing.

## How to use this skill

1. **Classify the request** into one or more roles from the table below.
2. **Prefer what is already installed**: invoke the listed skill with the `Skill` tool,
   or call the already-connected MCP tool. Check the reminders/tool list — never guess a name.
3. **If a skill is missing**, look it up in `references/skills-catalog.md` and give the
   install command (or run `scripts/install.ps1` for the whole bundle).
4. **If a connector is needed**, look it up in `references/connectors.md`. Connectors need the
   user's own sign-in: tell them to add it in *Claude → Settings → Connectors* (or `/mcp`
   in a terminal). Never ask for passwords or API keys in chat.
5. **If no paid service is wanted**, pick from `references/free-ai-tools.md` (local, free,
   open-source alternatives).
6. Multi-domain jobs: chain skills in the order of the pipelines below and say which
   step you are on.

Reply in the user's language (Hindi/Hinglish if they wrote in Hindi).

## Role → first-choice tools

| Role / need | Skills to invoke first | Connectors that help |
|---|---|---|
| **CEO / strategy / weekly plan** | `tred-iq-ceo`, `social-media-skills:social-strategy`, `social-media-skills:goals-and-kpis`, `superpowers:brainstorming`, `superpowers:writing-plans` | Notion, Linear/Atlassian, monday.com, Google Calendar |
| **CMO / marketing** | `social-media-skills:campaign-and-launch-planning`, `content-engine`, `social-media-skills:content-calendar`, `social-media-skills:lead-magnets-and-funnels` | HubSpot, Klaviyo, Mailchimp, Supermetrics, Metricool |
| **YouTube channel** | `anthropic-skills:yt-plan`, `yt-script`, `yt-seo`, `yt-package`, `yt-chapters`, `yt-shorts`, `yt-retention`, `yt-audit`, `ai-youtube-os:daily` | vidIQ, Tubealfred (needs `/mcp` auth) |
| **Social media (IG/TikTok/X/LinkedIn)** | `social-media-skills:*` (90+ skills: hook-writer, reels-script, carousel-writer, thread-writer, hashtag-strategy …), `posty:posty`, `omnisocials:omnisocials` | Typefully, Metricool, TikTok for Business |
| **Video making / editing** | `hyperframes`, `hyperframes-registry`, `media-use`, `remotion-video-creation`, `manim-video`, `video-editing`, `videodb`, `ai-video-generation`, `tasteforge-video` | Higgsfield, AI Producer (Opus), Riverside, Tella, Cloudinary |
| **Voice / audio** | `voicestudio`, `social-media-skills:ai-voiceover`, `social-media-skills:suno`, `social-media-skills:ai-music-and-sound` | ElevenLabs, Speko |
| **Background music (for reels/videos)** | `social-media-skills:suno`, `social-media-skills:ai-music-and-sound`, `media-use` | ElevenLabs, Higgsfield, AI Producer; free: MusicGen, YouTube Audio Library, Pixabay Music |
| **Publish to YouTube** | `tubealfred-youtube:*`, `anthropic-skills:yt-package`, `social-media-skills:youtube-publishing-and-metadata` | omnisocials, posty, tubealfred-youtube, Metricool (each needs `/mcp` auth) |
| **Publish to Instagram** | `social-media-skills:instagram-reels-publishing`, `instagram-growth`, `posty:posty`, `omnisocials:omnisocials` | omnisocials, posty, Metricool (each needs `/mcp` auth) |
| **Images / design / thumbnails** | `social-media-skills:thumbnail-design`, `image-prompt`, `nano-banana`, `flux`, `ideogram`, `canva`, `frontend-design`, `fal-ai-media` | Canva, Figma, Adobe, Shutterstock |
| **Day trading** | `trader-scanner` → `trader-news` → `trader-entry` → `trader-exit` → `trader-timemachine` → `trader-budget` → `trader-risk` → `trader-broker`; plus `trader-alerts`, `trader-analyst`, `trader-pelosi` | Alpha Vantage, Financial Datasets, Webull, Clear Street, LunarCrush |
| **Finance / accounting (CFO)** | `anthropic-skills:xlsx`, `trader-analyst`, `dataviz` | QuickBooks, Zoho Books, Rillet, NumbersGame, Mollie, Deel |
| **Data / analytics / BI** | `dataviz`, `anthropic-skills:xlsx`, `agentdb-vector-search`, `anthropic-skills:deep-research` | PostHog, dbt, Blaze SQL, Dremio, Google Sheets, Supabase, Neon |
| **Coding / engineering (CTO)** | `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:subagent-driven-development`, `code-review`, `simplify`, `security-review`, `pair-programming`, `sparc-methodology`, `v3-*`; plugin `mattpocock-skills` (grill/spec/ticket) | GitHub (gh CLI), Atlassian, Exa, Microsoft Learn |
| **Replica / reverse-eng / competitive coding** | `code-forge` (clone a UI, authorized reverse engineering/CTF, Codeforces/LeetCode); plugins `clone-website`, `ghidra`, `reverse-engineering`, `cppcheatsheet` | Exa, Context7, GitHub |
| **GitHub / releases** | `github-code-review`, `github-multi-repo`, `github-project-management`, `github-release-management`, `github-workflow-automation`, `superpowers:finishing-a-development-branch` | GitHub |
| **DevOps / deploy / monitoring** | `hooks-automation`, `verification-quality`, `run` | Cloudflare, Railway, Datadog, Grafana, Supabase, Expo, v0 |
| **AI agents / swarms / memory** | `swarm-orchestration`, `swarm-advanced`, `agentdb-*`, `reasoningbank-*`, `flow-nexus-*`, `stream-chain`, `claude-api`, `omni-*`, `cli-*` | — |
| **Sales / CRM / leads** | `social-media-skills:social-selling-and-dm`, `tubealfred-youtube:youtube-comment-leads` | HubSpot, Salesforce, Pipedrive, Apollo.io, Zoho CRM, Salesloft |
| **Ops / projects / meetings (COO)** | `superpowers:executing-plans`, `schedule`, `loop`, `anthropic-skills:morning` | ClickUp, monday.com, Todoist, Asana-likes, Fathom, Grain, Circleback, Reclaim |
| **Google Workspace (G Suite)** | `anthropic-skills:google-workspace`; plugins `gws`, `gog-cli` | Google Docs, Sheets, Calendar, Microsoft 365 |
| **Multimedia / 3D / graphics (free)** | `hyperframes`, `manim-video`, `unreal-engine-cpp-pro`, `frontend-design`; free tools: Blender, ComfyUI, FFmpeg, GIMP, Krita (see `free-ai-tools.md`) | Cloudinary, Adobe, Canva |
| **Notes / knowledge base** | plugins `notion`, `airtable`; built-in `anthropic-skills:docs` | Notion, Microsoft 365 |
| **Docs / reports / decks** | `anthropic-skills:docx`, `pdf`, `pptx`, `xlsx`, `docs`, `artifact-design` | Google Docs, Notion, Microsoft 365, DocuSign |
| **Research** | `anthropic-skills:deep-research`, `social-media-skills:content-research-and-sourcing` | Exa, alphaXiv, bioRxiv |
| **Automation (no-code)** | `hooks-automation`, `schedule` | n8n, Make, Celigo, Prefect, CodeWords |
| **Build new skills / find more** | `anthropic-skills:skill-creator`, `skill-builder`, `superpowers:writing-skills`, `find-skills` | MCP & Skills Finder (13,900+ listings), LLM SkillHub |

## Ready-made pipelines

- **YouTube video end-to-end:** yt-plan → yt-script → voicestudio (voice) → hyperframes / media-use (video) → yt-package + yt-seo → yt-chapters → yt-shorts (repurpose) → tred-iq-ceo (weekly review).
- **Trade of the day:** trader-scanner → trader-news → trader-entry → trader-exit → trader-timemachine → trader-budget → trader-risk → trader-broker (paper by default, always asks first).
- **Product launch:** brainstorming → campaign-and-launch-planning → content-calendar → hook-writer / reels-script / carousel-writer → scheduling-and-queue → analytics-and-reporting.
- **Ship code:** brainstorming → writing-plans → test-driven-development → code-review → verification-before-completion → finishing-a-development-branch.

## Rules

- Never claim a connector is "connected" unless the tool list shows it. Most connectors are
  free to connect but the underlying service may need its own account or plan — say so.
- Money-moving actions (orders, payments, transfers) always need the user's explicit yes;
  trading defaults to paper.
- Do not paste secrets in chat; keys go in env vars or the service's own sign-in.
- When the catalog is out of date, search live: MCP & Skills Finder connector (`search_skills` /
  `search_plugins` / `search_mcp_servers`) or the MCP registry search.

## Files

- `references/skills-catalog.md` — every skill by category (300+), with install source
- `references/connectors.md` — 140+ real MCP connectors with URLs, by category
- `references/plugins-and-repos.md` — plugin marketplaces and GitHub repos to install from
- `references/free-ai-tools.md` — 100+ free / open-source AI tools to run locally
- `scripts/install.ps1` — one-shot installer for the plugin marketplaces (Windows; dry run by default)
