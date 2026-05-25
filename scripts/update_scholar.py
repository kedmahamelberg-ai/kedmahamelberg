"""
Fetch Google Scholar citation data for Kedma Hamelberg's profile via SerpAPI.
Writes results to _data/scholar.json for Jekyll to consume.

SerpAPI is used because Google Scholar blocks direct requests from
datacenter IPs (including GitHub Actions). The free tier (100 searches/month)
is far more than enough for a weekly cron.

If SERPAPI_KEY is missing or the request fails, the script exits cleanly
(code 0) without overwriting the existing _data/scholar.json, so the
workflow does not turn red and the site keeps showing the last known data.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

SCHOLAR_ID = "M8TAlNwAAAAJ"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "_data" / "scholar.json"
MAX_PUBLICATIONS = 20


def fetch_serpapi(api_key: str) -> dict:
    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "hl": "en",
        "num": "100",
        "api_key": api_key,
    }
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_stat(table_rows: list, key: str) -> int:
    """SerpAPI returns cited_by.table as a list of single-key dicts."""
    for row in table_rows:
        if key in row:
            return int(row[key].get("all", 0))
    return 0


def transform(payload: dict) -> dict:
    cited_by = payload.get("cited_by", {})
    table = cited_by.get("table", [])

    stats = {
        "total_citations": extract_stat(table, "citations"),
        "h_index": extract_stat(table, "h_index"),
        "i10_index": extract_stat(table, "i10_index"),
    }

    articles = payload.get("articles", []) or []
    articles_sorted = sorted(
        articles,
        key=lambda a: int((a.get("cited_by") or {}).get("value") or 0),
        reverse=True,
    )[:MAX_PUBLICATIONS]

    publications = []
    for art in articles_sorted:
        cb = art.get("cited_by") or {}
        publications.append({
            "title": art.get("title", ""),
            "authors": art.get("authors", ""),
            "venue": art.get("publication", ""),
            "year": int(art["year"]) if art.get("year", "").isdigit() else art.get("year", ""),
            "citations": int(cb.get("value") or 0),
            "url": art.get("link", ""),
        })

    yearly = [
        {"year": int(pt.get("year")), "count": int(pt.get("citations") or 0)}
        for pt in cited_by.get("graph", [])
        if pt.get("year")
    ]

    now = datetime.now(timezone.utc)
    return {
        "scholar_id": SCHOLAR_ID,
        "profile_url": f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en",
        "last_updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_updated_human": now.strftime("%B %d, %Y"),
        "stats": stats,
        "yearly_citations": yearly,
        "publications": publications,
    }


def main() -> int:
    api_key = os.environ.get("SERPAPI_KEY", "").strip()
    if not api_key:
        print("⚠ SERPAPI_KEY not set. Skipping update; existing data preserved.")
        return 0

    print(f"Fetching Google Scholar profile via SerpAPI: {SCHOLAR_ID}")
    try:
        payload = fetch_serpapi(api_key)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
        print(f"⚠ SerpAPI request failed: {e}. Existing data preserved.")
        return 0
    except json.JSONDecodeError as e:
        print(f"⚠ Could not parse SerpAPI response: {e}. Existing data preserved.")
        return 0

    if "error" in payload:
        print(f"⚠ SerpAPI returned error: {payload['error']}. Existing data preserved.")
        return 0

    data = transform(payload)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Data written to {OUTPUT_PATH}")
    print(f"  Total citations: {data['stats']['total_citations']}")
    print(f"  h-index:         {data['stats']['h_index']}")
    print(f"  i10-index:       {data['stats']['i10_index']}")
    print(f"  Publications:    {len(data['publications'])}")
    print(f"  Yearly entries:  {len(data['yearly_citations'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
