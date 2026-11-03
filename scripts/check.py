#!/usr/bin/env python3
"""Validation checks for the Free Reseller Tools Directory.

Run: python3 scripts/check.py
Exit code 0 = all checks pass. Standard library only.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "tools.json"
SITE = ROOT / "site" / "index.html"
STYLE = ROOT / "site" / "style.css"
GUIDE = ROOT / "docs" / "prep-setup.md"
LICENSE = ROOT / "LICENSE"
README = ROOT / "README.md"
STATUS = ROOT / "STATUS.md"

FAILURES = []


def check(name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(f"{name}: {detail}")


def main():
    # --- files exist -------------------------------------------------------
    for path in (DATA, SITE, STYLE, GUIDE, LICENSE, README):
        check(f"file exists: {path.relative_to(ROOT)}", path.is_file())
    check("file exists: STATUS.md", STATUS.is_file())
    if FAILURES:
        print("\nMissing files; aborting remaining checks.")
        return 1

    # --- LICENSE exact copyright line --------------------------------------
    license_text = LICENSE.read_text(encoding="utf-8")
    check(
        "LICENSE copyright line exact",
        "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text
        and license_text.startswith("MIT License"),
    )

    # --- README credit ------------------------------------------------------
    readme_text = README.read_text(encoding="utf-8")
    check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme_text)
    check(
        "README has no affiliate language",
        not re.search(r"\baffiliate link", readme_text, re.IGNORECASE)
        or "No affiliate links" in readme_text,
    )

    # --- data/schema --------------------------------------------------------
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
        check("data/tools.json parses as JSON", True)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        check("data/tools.json parses as JSON", False, str(exc))
        return 1

    meta = data.get("meta", {})
    check("meta has title and description", bool(meta.get("title")) and bool(meta.get("description")))
    check(
        "meta updated_on is a valid date string",
        bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(meta.get("updated_on", "")))),
    )

    categories = {c["id"]: c["name"] for c in data.get("categories", [])}
    check("at least 5 categories", len(categories) >= 5, f"found {len(categories)}")

    tools = data.get("tools", [])
    check("at least 10 tools listed", len(tools) >= 10, f"found {len(tools)}")

    required_fields = ("id", "category", "name", "what_it_is", "cost", "limits", "url", "verified_on")
    ids = set()
    for tool in tools:
        tid = tool.get("id", "<no id>")
        missing = [f for f in required_fields if not tool.get(f)]
        check(f"tool '{tid}' has all required fields", not missing, f"missing {missing}" if missing else "")
        if tid in ids:
            check(f"tool id '{tid}' unique", False, "duplicate id")
        ids.add(tid)

        check(
            f"tool '{tid}' category is known",
            tool.get("category") in categories,
            tool.get("category", ""),
        )
        url = tool.get("url", "")
        check(f"tool '{tid}' URL is https", url.startswith("https://"), url)
        check(
            f"tool '{tid}' URL has no affiliate/referral params",
            not re.search(r"[?&](tag|ref|affiliate|aff|utm_)=|\bbit\.ly\b", url, re.IGNORECASE),
            url,
        )
        check(
            f"tool '{tid}' verified_on is a valid date string",
            bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(tool.get("verified_on", "")))),
        )
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(tool.get("verified_on", ""))):
            check(
                f"tool '{tid}' verified_on is in the past",
                date.fromisoformat(tool["verified_on"]) <= date.today(),
                tool["verified_on"],
            )
        for field in ("what_it_is", "cost", "limits"):
            check(
                f"tool '{tid}' field '{field}' is substantive",
                len(str(tool.get(field, ""))) >= 30,
                f"{len(str(tool.get(field, '')))} chars",
            )

    # --- site page sync ------------------------------------------------------
    site_text = SITE.read_text(encoding="utf-8")
    for tool in tools:
        check(
            f"tool '{tool['id']}' has an article in site/index.html",
            f'id="tool-{tool["id"]}"' in site_text,
        )
        check(
            f"tool '{tool['id']}' link is on the page",
            f'href="{tool["url"]}"' in site_text,
        )
        check(
            f"tool '{tool['id']}' verified date shown on page",
            tool["verified_on"] in site_text,
        )
    page_ids = set(re.findall(r'id="tool-([a-z0-9-]+)"', site_text))
    data_ids = {t["id"] for t in tools}
    check("page has no tool articles missing from data", not (page_ids - data_ids), str(page_ids - data_ids))

    check("page title set", "<title>" in site_text and "Reseller" in site_text)
    check("page links to prep guide", "docs/prep-setup.md" in site_text)
    check("page says no affiliate links", "No affiliate links" in site_text)
    check("css file referenced", 'href="style.css"' in site_text)
    style_text = STYLE.read_text(encoding="utf-8")
    check("css has body rule", "body {" in style_text)

    # --- guide ---------------------------------------------------------------
    guide_text = GUIDE.read_text(encoding="utf-8")
    for topic in ("SKU", "photo", "ledger", "Pack-and-ship", "bins"):
        check(f"guide mentions '{topic}'", topic.lower() in guide_text.lower())
    check("guide has license footer", "Asdale Dynamics, LLC" in guide_text)

    # --- hygiene: no secrets or personal data --------------------------------
    all_text = "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in (DATA, SITE, STYLE, GUIDE, README, STATUS)
        if p.is_file()
    )
    secret_patterns = re.compile(
        r"(api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9]{16,}"
        r"|sk-[A-Za-z0-9]{20,}"
        r"|ghp_[A-Za-z0-9]{20,}"
        r"|BEGIN (RSA |EC |DS)?PRIVATE KEY"
        r"|password\s*[:=]\s*['\"]?\S"
        r"|\b[A-Za-z0-9._%+-]+@(?:example|test)\.(?!com\b))",
        re.IGNORECASE,
    )
    check("no obvious secrets or API keys", not secret_patterns.search(all_text))

    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", all_text)
    allowed = {"support@photopea.com", "hello@everbee.io"}
    bad = [e for e in emails if e not in allowed]
    check(
        "no personal email addresses",
        not bad,
        str(bad),
    )

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
