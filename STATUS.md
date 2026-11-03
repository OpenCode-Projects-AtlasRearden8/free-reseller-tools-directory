# STATUS.md — Free Reseller Tools Directory

Last updated: 2026-11-03

## What was built

A static, no-dependency directory of free-tier tools for online resellers, by Asdale Dynamics, LLC:

- **`site/index.html` + `site/style.css`** — the directory page. 17 tools across 6 categories (Photo Editing, Keyword Research, Shipping Calculators, Sold-Price Lookups, Sales Trackers, Label Makers). Each entry states what it is, cost, limits, a link, and the date the link was verified live (2026-11-03). Plain CSS, no JavaScript, no cookies, no analytics, no affiliate links, no paid placements.
- **`data/tools.json`** — the same directory as structured data, including meta (policy on affiliates/placements/data) and a per-tool `verified_on` date.
- **`docs/prep-setup.md`** — "The Old-School Prep Setup": intake/prep/logging/listing/shipping stations, bin and SKU system, a $0 photo booth, the one-tab ledger, per-category prep tips, pack-and-ship workflow, a weekly low-energy rhythm, and a paper-trail (tax) section. General-information tone; explicitly not tax or financial advice.
- **`README.md`** — what's inside, how to run and verify, honest notes. Credits Asdale Dynamics, LLC.
- **`LICENSE`** — MIT, copyright line exactly: `Copyright (c) 2026 Asdale Dynamics, LLC`.
- **`scripts/check.py`** — validation suite (Python 3 standard library only).

## How to run it

Nothing to build; it's a static site:

```bash
# open directly
xdg-open site/index.html        # Linux (or just double-click)

# or serve
python3 -m http.server 8000 --directory site
# visit http://localhost:8000
```

## How to verify it

```bash
python3 scripts/check.py
```

Checks: required files exist; LICENSE copyright line is exact; README credits Asdale Dynamics, LLC; `tools.json` parses; every tool has all required fields (id, category, name, what_it_is, cost, limits, url, verified_on); URLs are HTTPS with no affiliate/referral parameters (`tag=`, `ref=`, `utm_`, bit.ly, etc.); verified dates are valid and in the past; category references resolve; every data entry has a matching article + link + verified date on the page (and no orphan page articles); the guide and CSS checks; scans for obvious secrets/API keys and personal email addresses.

## Verification results (2026-11-03)

- `python3 scripts/check.py` — **all 178 checks PASS, exit code 0**.
- HTTP smoke test: served `site/` with `python3 -m http.server`; `index.html` and `style.css` both load with **HTTP 200**.
- Link verification: every tool URL was fetched live on 2026-11-03 and its content confirmed (Photopea, GIMP, remove.bg, Canva, everbee.com, Google Trends, AnswerThePublic, Pirate Ship, USPS postcalc, eBay advanced search, PriceCharting, Flipwise, Google Sheets sign-in page, eBay selling/Seller Hub page, Avery, Labelary). 130point bot-blocks automated fetches (403) and was verified live via its own about-page content surfaced through search plus multiple 2026 third-party reviews; this is stated openly on its listing.

## Known gaps

- **Free tiers drift.** Costs/limits describe each tool's site as of 2026-11-03; quota numbers (e.g., Pirate Ship's no-account tools, EverBee's free search count, AnswerThePublic's daily cap) can change without notice. Re-verify before relying on any entry; a re-check pass should update `verified_on` dates.
- **Coverage is eBay/US-centric.** Sold-price lookups assume eBay; keyword research skews Etsy (EverBee). Amazon, Mercari, Poshmark, and non-US marketplaces are not yet covered.
- **`130point` cannot be deep-verified by automation** because of its bot blocking; the entry says so.
- **No screenshot/thumbnail imagery** — the page is intentionally text-only for zero-maintenance and privacy.
- **Single-page site** — no category permalink pages or search; fine at 17 entries, revisit if the list grows past ~40.
- **`docs/prep-setup.md`** is markdown only; there is no rendered HTML version inside `site/` (the README describes how to view markdown comfortably).

## Not included (by design)

- Anyone's personal data, secrets, or API keys (checked by `scripts/check.py`).
- Affiliate links, referral parameters, or paid placements (checked, and stated on the page).
- Any publishing/deployment step — this repo is local-first; nothing is pushed or published anywhere.
