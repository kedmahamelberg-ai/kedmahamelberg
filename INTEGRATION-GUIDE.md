# Google Scholar → Jekyll Integration Guide

Auto-updating Google Scholar citation metrics for your Jekyll + Minimal Mistakes website.

---

## How It Works

```
GitHub Action (weekly) → scrapes Google Scholar → writes _data/scholar.json → Jekyll rebuilds → live stats on site
```

The Action runs every Monday at 06:00 UTC. You can also trigger it manually from the Actions tab.

---

## Installation (5 Steps)

### Step 1: Copy the files into your repo

Place these files in your Jekyll repository:

```
your-site/
├── .github/
│   └── workflows/
│       └── update-scholar.yml     ← scheduled scraper
├── _data/
│   └── scholar.json               ← auto-updated data (seed file included)
├── _includes/
│   └── scholar-stats.html         ← the visual component
├── assets/
│   └── css/
│       └── scholar-stats.css      ← styles
└── scripts/
    └── update_scholar.py          ← Python scraper
```

### Step 2: Load the CSS

Add this line to your `_config.yml` under the existing `head_scripts` or create a `_includes/head/custom.html`:

**Option A — Add to `_includes/head/custom.html`:**
```html
<link rel="stylesheet" href="{{ '/assets/css/scholar-stats.css' | relative_url }}">
```

**Option B — If you already have `_includes/head-custom.html`:**
Add the same `<link>` tag inside that file.

### Step 3: Add the component to your homepage

In your homepage file (likely `_pages/home.md` or `index.md` or `index.html`), add:

```liquid
{% include scholar-stats.html %}
```

Place it wherever you want the widget to appear. For example, after your intro text and before the "Explore" section:

```markdown
**Currently seeking tenure-track positions in digital marketing & AI**.
Open to research collaborations and AI education partnerships.

---

{% include scholar-stats.html %}

---

### 🔍 Explore
```

### Step 4: Enable GitHub Actions

Your repository needs GitHub Actions enabled with **write permissions**:

1. Go to **Settings → Actions → General**
2. Under "Workflow permissions", select **Read and write permissions**
3. Save

### Step 5: Run the first update

1. Go to the **Actions** tab in your repository
2. Select **"Update Google Scholar Data"** from the sidebar
3. Click **"Run workflow"**
4. Wait ~30 seconds — check that `_data/scholar.json` was updated

The site will rebuild automatically via GitHub Pages.

---

## Customization

### Show only metrics (no publications list)

In `_includes/scholar-stats.html`, remove or comment out the "Recent publications" block (lines between the `{% if site.data.scholar.publications.size > 0 %}` and its `{% endif %}`).

### Change update frequency

Edit `.github/workflows/update-scholar.yml`, line 13:
```yaml
# Every day at 06:00 UTC:
- cron: "0 6 * * *"

# Every Monday at 06:00 UTC (default):
- cron: "0 6 * * 1"

# Every 1st and 15th of the month:
- cron: "0 6 1,15 * *"
```

### Adjust the design

Edit `assets/css/scholar-stats.css`. The component uses BEM naming (`scholar-impact__*`) so it won't conflict with Minimal Mistakes styles.

Key variables to tweak:
- `#1a73e8` — accent blue (Google Scholar blue)
- `#4285f4` — bar chart fill
- `#24292f` — headings
- `#57606a` — secondary text

---

## Troubleshooting

**Action fails with "Rate limited (429)"**
Google Scholar occasionally blocks automated requests. The script retries 3 times with increasing delays. If it still fails, it will succeed on the next scheduled run. Your existing `_data/scholar.json` remains unchanged.

**Numbers show 0**
Run the workflow manually once (Step 5). The seed file ships with placeholder zeros.

**CSS not loading**
Make sure the `<link>` tag path matches where you placed the CSS file. Check browser DevTools for 404 errors.

---

## Architecture

- **No API keys required** — pure HTML scraping of your public Scholar profile
- **No client-side fetching** — data is baked into the site at build time (fast, no CORS issues)
- **Graceful degradation** — if the Action fails, old data persists; the widget simply shows the last known values
- **Privacy-safe** — no tracking scripts, no third-party calls from visitors' browsers
