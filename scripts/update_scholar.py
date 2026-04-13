"""
Fetch Google Scholar citation data for Kedma Hamelberg's profile.
Writes results to _data/scholar.json for Jekyll to consume.

This script is designed to run in a GitHub Action on a weekly schedule.
It uses basic HTTP scraping with retry logic and user-agent rotation
to avoid being blocked by Google Scholar.
"""

import json
import re
import time
import random
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────
SCHOLAR_ID = "M8TAlNwAAAAJ"
SCHOLAR_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "_data" / "scholar.json"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

MAX_RETRIES = 3
# ────────────────────────────────────────────────────────────────────


def fetch_scholar_page(url: str) -> str:
    """Fetch the raw HTML of a Google Scholar profile page."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": random.choice(USER_AGENTS),
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = (attempt + 1) * 30 + random.randint(5, 15)
                print(f"  Rate-limited (429). Waiting {wait}s before retry {attempt + 1}/{MAX_RETRIES}...")
                time.sleep(wait)
            else:
                raise
        except urllib.error.URLError as e:
            print(f"  Network error: {e}. Retry {attempt + 1}/{MAX_RETRIES}...")
            time.sleep(10)
    raise RuntimeError(f"Failed to fetch {url} after {MAX_RETRIES} retries.")


def parse_citation_stats(html: str) -> dict:
    """
    Extract citation statistics from the Google Scholar profile HTML.
    Returns dict with total_citations, h_index, i10_index.
    """
    stats = {}

    # Google Scholar displays stats in a table with id="gsc_rsb_st"
    # Each row has: metric name | all-time value | since-year value
    # We extract the all-time values (first <td> with class "gsc_rsb_std")
    stat_values = re.findall(
        r'<td class="gsc_rsb_std"[^>]*>(\d+)</td>', html
    )

    if len(stat_values) >= 6:
        # Order: citations_all, citations_recent, h_all, h_recent, i10_all, i10_recent
        stats["total_citations"] = int(stat_values[0])
        stats["citations_recent"] = int(stat_values[1])
        stats["h_index"] = int(stat_values[2])
        stats["h_index_recent"] = int(stat_values[3])
        stats["i10_index"] = int(stat_values[4])
        stats["i10_index_recent"] = int(stat_values[5])
    elif len(stat_values) >= 2:
        # Fallback: at least get total citations
        stats["total_citations"] = int(stat_values[0])
        stats["h_index"] = int(stat_values[2]) if len(stat_values) > 2 else None
        stats["i10_index"] = int(stat_values[4]) if len(stat_values) > 4 else None
    else:
        # Last-resort: search for any citation count pattern
        match = re.search(r'Cited by[^\d]*(\d+)', html)
        if match:
            stats["total_citations"] = int(match.group(1))

    return stats


def parse_publications(html: str) -> list:
    """
    Extract the list of publications visible on the profile page.
    Returns list of dicts with title, authors, venue, year, citation_count, url.
    """
    publications = []

    # Each publication is in a <tr class="gsc_a_tr">
    rows = re.findall(
        r'<tr class="gsc_a_tr">(.*?)</tr>', html, re.DOTALL
    )

    for row in rows:
        pub = {}

        # Title and link
        title_match = re.search(
            r'<a[^>]*class="gsc_a_at"[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
            row, re.DOTALL,
        )
        if title_match:
            pub["url"] = "https://scholar.google.com" + title_match.group(1).replace("&amp;", "&")
            pub["title"] = re.sub(r"<[^>]+>", "", title_match.group(2)).strip()

        # Authors and venue (two <div class="gs_gray"> elements)
        gray_divs = re.findall(
            r'<div class="gs_gray">(.*?)</div>', row, re.DOTALL
        )
        if len(gray_divs) >= 1:
            pub["authors"] = re.sub(r"<[^>]+>", "", gray_divs[0]).strip()
        if len(gray_divs) >= 2:
            pub["venue"] = re.sub(r"<[^>]+>", "", gray_divs[1]).strip()

        # Citation count
        cite_match = re.search(
            r'<a[^>]*class="gsc_a_ac[^"]*"[^>]*>(\d+)</a>', row
        )
        if cite_match:
            pub["citations"] = int(cite_match.group(1))
        else:
            pub["citations"] = 0

        # Year
        year_match = re.search(
            r'<span class="gsc_a_h gsc_a_hc[^"]*"[^>]*>(\d{4})</span>', row
        )
        if year_match:
            pub["year"] = int(year_match.group(1))

        if pub.get("title"):
            publications.append(pub)

    return publications


def parse_yearly_citations(html: str) -> list:
    """
    Extract the per-year citation histogram data.
    Returns list of dicts with year and count.
    """
    yearly = []

    # The histogram years are in <span class="gsc_g_t">YYYY</span>
    years = re.findall(r'<span class="gsc_g_t"[^>]*>(\d{4})</span>', html)

    # The counts are in <span class="gsc_g_al">N</span> inside <a> tags
    counts = re.findall(r'<span class="gsc_g_al">(\d+)</span>', html)

    # If the simple pattern doesn't work, try the bar-height approach
    if not counts:
        counts = re.findall(r'gsc_g_a"[^>]*>.*?<span[^>]*>(\d+)</span>', html, re.DOTALL)

    for year, count in zip(years, counts):
        yearly.append({"year": int(year), "count": int(count)})

    return yearly


def main():
    print(f"Fetching Google Scholar profile: {SCHOLAR_ID}")
    print(f"URL: {SCHOLAR_URL}")

    html = fetch_scholar_page(SCHOLAR_URL)

    # Parse all data
    stats = parse_citation_stats(html)
    publications = parse_publications(html)
    yearly_citations = parse_yearly_citations(html)

    # Build output
    data = {
        "scholar_id": SCHOLAR_ID,
        "profile_url": f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_updated_human": datetime.now(timezone.utc).strftime("%B %d, %Y"),
        "stats": stats,
        "yearly_citations": yearly_citations,
        "publications": publications,
    }

    # Write to _data/scholar.json
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Data written to {OUTPUT_PATH}")
    print(f"  Total citations: {stats.get('total_citations', 'N/A')}")
    print(f"  h-index: {stats.get('h_index', 'N/A')}")
    print(f"  Publications found: {len(publications)}")
    print(f"  Year histogram entries: {len(yearly_citations)}")


if __name__ == "__main__":
    main()
