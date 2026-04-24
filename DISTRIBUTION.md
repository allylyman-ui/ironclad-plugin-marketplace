# Distribution Guide

How to get this marketplace onto your private GitHub repo and into your teammates' hands. Written for Ally — you only do the "initial push" once.

---

## TL;DR

Your repo: `allylyman-ui/ironclad-marketplace`

1. Push this folder to it.
2. Grant `read` access to your team.
3. Teammates run two commands in Claude Code.

---

## Step 1 — Push this folder to your repo

You already created the repo on GitHub (`ironclad-marketplace`). From the `ironclad-marketplace/` folder on your laptop:

```bash
cd ~/path/to/ironclad-marketplace
git init
git add .
git commit -m "Initial commit — ironclad-branding plugin v1.0.0"
git branch -M main
git remote add origin git@github.com:allylyman-ui/ironclad-marketplace.git
git push -u origin main
```

Swap `git@github.com:<...>.git` for the HTTPS URL if you don't use SSH, e.g.:
`https://github.com/allylyman-ui/ironclad-marketplace.git`

---

## Step 2 — Grant access to your team

On the repo's GitHub page → **Settings → Collaborators and teams**.

Grant `Read` access to whichever of these applies:
- A GitHub Team (e.g. `@your-org/sales`) — best for larger audiences.
- Individual teammates by username — fine for smaller teams.

**Do not make the repo public.** The bundled fonts (Moderat, SangBleu Kingdom) are commercially licensed and cannot be redistributed.

---

## Step 3 — Tell your teammates

Paste this in Slack / email:

> **Hey team** — I put together a Claude Code plugin with Ironclad branding so anything Claude generates for you (decks, one-pagers, HTML, emails) looks on-brand automatically.
>
> **Install steps:**
> 1. Make sure you're authenticated to GitHub — run `gh auth login` in your terminal if you haven't (pick HTTPS).
> 2. In Claude Code, run:
>    ```
>    /plugin marketplace add allylyman-ui/ironclad-marketplace
>    /plugin install ironclad-branding@ironclad-marketplace
>    ```
> 3. Verify with `/plugin list` — you should see `ironclad-branding` active.
>
> That's it. Ask Claude to "make a branded one-pager" or "use Ironclad branding" and it'll just work.
>
> **Important:** This is Ironclad-internal — do not share the repo URL externally. See `NOTICE.md` in the repo for full terms.
>
> Questions → me (ally.lyman@ironcladhq.com).

---

## Why a private repo works for Claude Code

Claude Code's plugin loader resolves `/plugin marketplace add owner/repo` by running a `git clone` under the hood. Because GitHub requires auth for private repos, each teammate needs their own auth on the machine. Three options, in order of ease:

| Method | What they do once | Auto-updates? |
|---|---|---|
| **GitHub CLI** (`gh auth login`) | Run it once, follow prompts | Manual only — run `/plugin marketplace update` to refresh |
| **SSH key** | Already works if they push to Ironclad repos | Same as above |
| **`GITHUB_TOKEN` env var** | Create a PAT with `repo` scope, export in `~/.zshrc` | ✅ Yes — Claude Code auto-pulls on startup |

For a sales team, **`gh auth login` is probably enough** — most people are fine running `/plugin marketplace update` manually when you tell them to.

---

## Shipping updates later

```bash
cd ~/path/to/ironclad-marketplace
# edit files under plugins/ironclad-branding/ ...
# bump version in plugins/ironclad-branding/.claude-plugin/plugin.json
git add .
git commit -m "Bump ironclad-branding to 1.1.0 — updated brand colors"
git push
```

Then Slack the team:

> Ironclad branding plugin v1.1.0 is out. Run `/plugin marketplace update ironclad-marketplace` and then `/plugin install ironclad-branding@ironclad-marketplace` to get it.

---

## Pinning to a version / branch

If you want stability, teammates can pin:

```
/plugin marketplace add allylyman-ui/ironclad-marketplace@v1.0.0
```

(where `v1.0.0` is a git tag you push.)

---

## Folder layout recap

```
ironclad-marketplace/
├── .claude-plugin/marketplace.json
├── README.md
├── NOTICE.md
├── DISTRIBUTION.md  ← this file
└── plugins/
    └── ironclad-branding/
        ├── .claude-plugin/plugin.json
        └── skills/ironclad-branding/
            ├── SKILL.md
            ├── references/brand-spec.md
            └── assets/
                ├── logos/       ← 7 logo variants (Ironclad + Jurist)
                ├── fonts/       ← 7 OTF files
                ├── icons/       ← 22 PNG icons
                └── templates/   ← ironclad-template.pptx (FY27 deck template)
```
