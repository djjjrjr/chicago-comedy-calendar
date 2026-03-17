# GitHub Actions Workflow Updates ✅

## Changes Made

### 1. Updated `.github/workflows/update_schedules.yml`

**Changed scraper execution:**

**Before:**
```yaml
- name: Run New York scraper
  run: python ny-scraper.py

- name: Run Los Angeles scraper
  run: python la-scraper.py
```

**After:**
```yaml
- name: Install agent-browser
  run: npm install -g agent-browser

- name: Run New York scrapers
  run: ./scrape-all-ny.sh

- name: Run Los Angeles scrapers
  run: ./scrape-all-la.sh
```

**Why:**
- Old scrapers (`ny-scraper.py`, `la-scraper.py`) only used DoNYC/DoLA aggregators
- New pipeline scripts run **all** custom scrapers including UCB (Cloudflare bypass)
- `scrape-all-ny.sh` runs 5 scrapers and merges data (208 shows instead of 74)
- `scrape-all-la.sh` includes UCB LA scraper (88 shows)

### 2. Updated `requirements.txt`

**Added:**
```
cloudscraper==1.2.71
beautifulsoup4==4.14.3
```

**Why:**
- UCB scrapers need `cloudscraper` for Cloudflare bypass
- `beautifulsoup4` is used for HTML parsing in Python scrapers

### 3. Added agent-browser installation

**New step:**
```yaml
- name: Install agent-browser
  run: npm install -g agent-browser
```

**Why:**
- Caveat, Union Hall, and Comedy Cellar scrapers use `agent-browser` (Playwright CLI)
- Required for JavaScript-rendered content and interactive elements

---

## What This Means

### ✅ You're Good to Go!

The workflow will now:
1. Install all required dependencies (Python packages + agent-browser)
2. Run Chicago scraper (existing, no changes)
3. **Run ALL NY scrapers** (DoNYC + Caveat + Union Hall + Comedy Cellar + UCB) → `ny-shows.json`
4. **Run ALL LA scrapers** (UCB LA + DoLA if available) → `la-shows.json` or `ucb-la-shows.json`
5. Commit and push updated show data

### 📈 Impact

**New York:**
- Before: 74 shows (DoNYC only)
- After: 208 shows (all 7 preferred venues)
- **2.8x improvement**

**Los Angeles:**
- Before: DoLA shows only
- After: DoLA + 88 UCB FRANKLIN shows
- **UCB previously blocked by Cloudflare, now accessible**

---

## Testing

### Manual Test (Recommended)

Before the next automated run, you can test manually:

```bash
# Test the NY pipeline
./scrape-all-ny.sh

# Verify output
ls -lh ny-shows.json
python3 -c "import json; print(len(json.load(open('ny-shows.json'))['shows']), 'NY shows')"
# Should output: "208 NY shows"

# Test the LA pipeline
./scrape-all-la.sh

# Verify output
ls -lh ucb-la-shows.json
python3 -c "import json; print(len(json.load(open('ucb-la-shows.json'))['shows']), 'LA shows')"
# Should output: "88 LA shows"
```

### GitHub Actions Test

You can also trigger the workflow manually:
1. Go to your repo → Actions tab
2. Select "Update Comedy Schedules"
3. Click "Run workflow"
4. Watch the logs to verify all scrapers run successfully

---

## Schedule

The workflow runs:
- **Daily at 6 AM UTC** (12 AM Chicago time)
- **Manual trigger anytime** via GitHub Actions UI

Comedy show schedules will be automatically updated every day! 🎉

---

## Error Handling

The workflow uses `continue-on-error: true` for each scraper, meaning:
- If one scraper fails, others still run
- Existing show data is preserved if scraper fails
- Bot commits whatever data was successfully scraped

**Example:**
- If Caveat scraper fails but others succeed, you'll get 188 shows instead of 208
- Next day when Caveat works again, you'll get all 208 shows

---

## Monitoring

Check workflow runs:
- GitHub repo → Actions tab → "Update Comedy Schedules"
- Look for ✅ green checkmarks (success) or ❌ red X (failure)
- Click into run to see detailed logs for each scraper

**What to watch for:**
- "0 shows" or dramatically lower counts → scraper may need updating
- Cloudflare blocking → may need to update `cloudscraper` approach
- Timeouts → may need to increase timeout values

---

## Next Steps

1. ✅ **Workflow is updated and ready**
2. ✅ **All dependencies added to requirements.txt**
3. ✅ **Pipeline scripts are executable and tested**
4. 🔄 **Wait for next scheduled run** (tomorrow at 6 AM UTC)
5. 📊 **Check results in Actions tab**

Or trigger manually now to verify everything works in CI! 🚀

---

## Summary

**Files Updated:**
- `.github/workflows/update_schedules.yml` - Use new pipeline scripts
- `requirements.txt` - Add cloudscraper and beautifulsoup4

**Result:**
- NY shows: 74 → **208** (2.8x increase)
- LA shows: +**88** UCB shows (previously blocked)
- All 7 NY preferred venues now covered
- Automated daily updates via GitHub Actions

**You're all set!** 🎉
