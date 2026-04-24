# Ironclad Marketplace

> **Internal use only — Ironclad employees.** This marketplace and its plugins contain Ironclad brand assets, fonts, templates, and internal guidance. Do not share externally, publish publicly, or distribute outside Ironclad. See `NOTICE.md` for terms.

Maintainer: **Ally Lyman** · ally.lyman@ironcladhq.com

---

## What's in here

| Plugin | What it does |
|---|---|
| `ironclad-branding` | Ironclad brand guidelines skill for creating on-brand assets — HTML pages, presentations, one-pagers, social posts, landing pages, event banners, email templates. Includes the official color palette, typography, logo files, fonts, icon set, and a PowerPoint template. |

More Ironclad plugins may be added over time — check back, or run `/plugin marketplace update ironclad-marketplace`.

---

## How to install (for Ironclad teammates)

This marketplace is hosted on a **private GitHub repo**, so you'll need to authenticate once. After that it's one line.

### One-time setup: authenticate GitHub

Pick whichever you already use:

**Option A — GitHub CLI (easiest):**
```bash
gh auth login
```
Follow the prompts, pick HTTPS, and authenticate with your Ironclad GitHub account.

**Option B — SSH key:** If you already push to Ironclad repos over SSH, you're done.

**Option C — Personal access token (needed for auto-updates):**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```
Add that line to your `~/.zshrc` or `~/.bashrc` so Claude Code can auto-update the marketplace in the background. Create a token at https://github.com/settings/tokens with `repo` scope.

### Install the marketplace

In Claude Code, run:

```
/plugin marketplace add allylyman-ui/ironclad-marketplace
```

### Install the branding plugin

```
/plugin install ironclad-branding@ironclad-marketplace
```

### Verify it's working

```
/plugin list
```
You should see `ironclad-branding` as active.

Then in any Claude Code or Cowork session, ask Claude to "make a branded one-pager for X" or "use Ironclad branding" and the skill will trigger automatically.

---

## Updating

```
/plugin marketplace update ironclad-marketplace
/plugin install ironclad-branding@ironclad-marketplace    # pulls the latest version
```

---

## For Ally (the maintainer) — how to ship updates

1. Edit files under `plugins/ironclad-branding/` (usually `skills/ironclad-branding/SKILL.md` or the brand spec in `references/`).
2. Bump the `version` in `plugins/ironclad-branding/.claude-plugin/plugin.json`.
3. Commit + push to the private GitHub repo.
4. Tell the team to run `/plugin marketplace update ironclad-marketplace`.

See `DISTRIBUTION.md` for a step-by-step on the initial push to private GitHub.

---

## Folder layout

```
ironclad-marketplace/
├── .claude-plugin/
│   └── marketplace.json          ← the marketplace manifest
├── plugins/
│   └── ironclad-branding/
│       ├── .claude-plugin/
│       │   └── plugin.json        ← the plugin manifest
│       └── skills/
│           └── ironclad-branding/
│               ├── SKILL.md
│               ├── references/
│               │   └── brand-spec.md
│               └── assets/
│                   ├── logos/         ← Ironclad + Jurist logo files
│                   ├── fonts/         ← Moderat + SangBleu Kingdom
│                   ├── icons/         ← 22 official Ironclad icons
│                   └── templates/     ← ironclad-template.pptx
├── README.md
├── NOTICE.md                      ← internal-use terms
└── DISTRIBUTION.md                ← how to host + update
```
