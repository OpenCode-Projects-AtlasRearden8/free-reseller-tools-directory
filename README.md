# Free Reseller Tools Directory

A static, beginner-friendly directory of **free-tier tools for online resellers** — photo editing, keyword research, shipping calculators, sold-price lookups (free tiers), sales trackers, and label makers — plus an old-school prep setup guide.

Built in plain English by **Asdale Dynamics, LLC**. No affiliate links. No paid placements. No cookies, analytics, or personal data.

## What's inside

| Path | What it is |
|---|---|
| `site/index.html` | The directory itself: every tool with what it is, cost, limits, and a link verified live on **2026-11-03** |
| `site/style.css` | Styles for the page (plain CSS, no frameworks) |
| `data/tools.json` | The same directory as structured data (the single source the page and the checker agree on) |
| `docs/prep-setup.md` | *The Old-School Prep Setup* — bins, SKUs, photo booth, one-tab ledger, packing, weekly rhythm |
| `scripts/check.py` | Validation "tests": schema, link hygiene, page/data sync, LICENSE and README checks |

## Running it

It's a static site — nothing to build:

```bash
# just open it
open site/index.html            # macOS
xdg-open site/index.html        # Linux

# or serve it
python3 -m http.server 8000 --directory site
# then visit http://localhost:8000
```

## Verifying it

Run the checks (Python 3, standard library only):

```bash
python3 scripts/check.py
```

The checker validates: valid JSON, required fields on every entry, HTTPS-only links with no affiliate/referral parameters, `verified_on` dates, that every entry in `tools.json` appears in `site/index.html` (and vice versa), that the prep guide and LICENSE/README exist with required notices, and that no tool is listed in a missing category.

## Honest notes

- Free tiers change constantly. Every cost/limit line reflects the tool's site as checked on 2026-11-03; re-verify before relying on any of it.
- `130point` bot-blocks automated fetches (403), so it was verified live via its own about page content and current third-party sources; everything else was fetched directly.

## License

MIT — see `LICENSE`. © 2026 Asdale Dynamics, LLC
