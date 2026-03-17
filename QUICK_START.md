# Quick Start Guide - Comedy Show Scrapers

## 🚀 Run Everything (Recommended)

### New York - All Scrapers + Merge
```bash
./scrape-all-ny.sh
```

### Los Angeles - UCB Scraper
```bash
./scrape-all-la.sh
```

That's it! Results will be in `ny-shows.json` and `ucb-la-shows.json`.

---

## 📂 Output Files

**New York**:
- `ny-shows.json` - **208 shows** (merged, deduplicated, ready to use)

**Los Angeles**:
- `ucb-la-shows.json` - **88 shows** from UCB FRANKLIN

**Individual Sources** (for debugging):
- `ucb-ny-shows.json` - UCB Theatre NY raw data
- `caveat-shows.json` - Caveat raw data
- `union-hall-shows.json` - Union Hall raw data
- `comedy-cellar-shows.json` - Comedy Cellar raw data
- `ny-shows-donyc.json` - DoNYC aggregator data

---

## 🛠️ Run Individual Scrapers

If you need to run scrapers separately:

```bash
# NY Scrapers
./scrape-caveat.sh              # Caveat (20 shows)
./scrape-union-hall.sh          # Union Hall (16 shows)
./scrape-comedy-cellar.sh       # Comedy Cellar (10 shows)
python3 scrape-ucb-ny.py        # UCB NY (88 shows)

# LA Scrapers
python3 scrape-ucb-la.py        # UCB LA (88 shows)

# Merge NY Data
python3 merge-ny-shows-v2.py    # Combines all NY sources
```

---

## 📊 What's Included

### New York (208 shows from 7 venues)
1. **UCB Theatre** - 88 shows (Cloudflare bypassed!)
2. **Caveat** - 20 shows
3. **Union Hall** - 16 shows
4. **Comedy Cellar** - 10 shows
5. **Gotham Comedy Club** - DoNYC
6. **The Stand** - DoNYC
7. **The Bell House** - DoNYC

### Los Angeles
- **UCB FRANKLIN** - 88 shows (Cloudflare bypassed!)

---

## ⚡ Dependencies

**Already Installed**:
- ✅ `cloudscraper` - Cloudflare bypass library
- ✅ `beautifulsoup4` - HTML parsing
- ✅ `agent-browser` - Playwright CLI tool

**If Missing** (run once):
```bash
python3 -m pip install --break-system-packages cloudscraper beautifulsoup4
```

---

## 🔄 Scheduling (GitHub Actions)

Add to `.github/workflows/scrape-shows.yml`:

```yaml
name: Scrape Comedy Shows

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6am UTC
  workflow_dispatch:      # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          pip install cloudscraper beautifulsoup4
          npm install -g agent-browser

      - name: Run NY scrapers
        run: ./scrape-all-ny.sh

      - name: Run LA scrapers
        run: ./scrape-all-la.sh

      - name: Commit results
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add ny-shows.json ucb-la-shows.json
          git commit -m "Update show data" || echo "No changes"
          git push
```

---

## 🐛 Troubleshooting

### "No shows scraped" or "0 shows"
- **UCB Scraper**: Cloudflare may have updated detection
- **Other scrapers**: Website structure may have changed
- **Fix**: Check if website loads manually, update selectors

### "Element not found" (agent-browser)
- Website changed button/element IDs
- Update selectors in scraper script
- Example: `button:has-text('SHOW ALL')` → check current button text

### "ModuleNotFoundError: No module named 'cloudscraper'"
```bash
python3 -m pip install --break-system-packages cloudscraper beautifulsoup4
```

### Timeouts
- Increase timeout in script (default: 30 seconds for cloudscraper, 60s for agent-browser)
- Check if website is slow/down
- Run individual scraper to identify which one is timing out

---

## 📈 Results

**Before**: 74 NY shows (DoNYC only)
**After**: 208 NY shows (all 7 venues)
**Improvement**: **2.8x increase** 🎉

**LA**: Added 88 UCB shows (previously blocked by Cloudflare)

---

## 📖 More Info

- `SCRAPER_COMPLETE.md` - Full technical documentation
- `UCB_CLOUDFLARE_SOLUTIONS.md` - Cloudflare bypass details
- `FINAL_SCRAPERS_SUMMARY.md` - Implementation summary

---

## ✅ Quick Check

Verify everything is working:

```bash
# Run scrapers
./scrape-all-ny.sh

# Check output
ls -lh ny-shows.json      # Should be ~85KB
python3 -c "import json; print(len(json.load(open('ny-shows.json'))['shows']), 'shows')"
# Should output: "208 shows"
```

If you see **208 shows**, everything is working! 🎉
