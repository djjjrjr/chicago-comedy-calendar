# Comedy Calendar - Complete Guide

## Overview

This project aggregates comedy shows from three cities using a **dual scraping approach**:
1. Broad category pages (Do312/DoNYC/DoLA) for discovery
2. Deep venue-specific scrapers for comprehensive coverage

**Current Coverage**: 796 total shows (Chicago: 159, NY: 316, LA: 321)

---

## Quick Commands

```bash
# Run all scrapers for all cities
./deploy.sh

# Run individual cities
./scrapers/chicago/scrape-all.sh
./scrapers/ny/scrape-all-ny.sh
./scrapers/la/scrape-all-la.sh

# View websites locally
open public/chicago/index.html
open public/ny/index.html
open public/la/index.html
```

---

## Architecture

### Data Flow

```
Category Scraper ────┐
                     ├──> Merge Script ──> Filter Stale ──> Dedupe ──> Final JSON
Venue Scrapers ──────┘
```

### Folder Structure

- **scrapers/** - All Python/Bash scraping scripts
- **data/** - JSON outputs (consumed by websites)
- **public/** - Static HTML/CSS/JS files
- **docs/** - Documentation
- **archive/** - Deprecated files

### Technologies

- **Python 3.11+** - Main scraping language
- **agent-browser** - CLI for browser automation (JS sites)
- **cloudscraper** - Bypass Cloudflare (UCB, Gotham, Bell House)
- **Playwright** - Dynamic rendering
- **BeautifulSoup** - HTML parsing

---

## Scraper Details

### Chicago (Do312.com)

**Sources:**
1. Category: `/events/comedy` (52 shows)
2. Venue pages: All 7 preferred venues (134 shows)
3. Merge & dedupe: 159 unique shows

**Scrapers:**
- `scrape-category.py` - Comedy category
- `scrape-do312-venues.py` - Loops through venue pages

**Preferred Venues:**
- The Second City, iO Theater, Annoyance Theatre
- Zanies, Laugh Factory, Lincoln Lodge, Den Theatre

### New York (DoNYC.com + Custom)

**Sources:**
1. Category: `/events/comedy` (74 shows)
2. Custom venue scrapers (8 venues, 410 shows)
3. Merge & filter stale: 316 current shows

**Scrapers:**
- `scrape-category.py` - DoNYC category
- `scrape-caveat.sh` - Caveat calendar
- `scrape-union-hall.sh` - Union Hall (lazy loading)
- `scrape-comedy-cellar.sh` - Multi-date scraping (28 dates)
- `scrape-the-stand.sh` - The Stand
- `scrape-ucb-ny.py` - UCB Theatre (Cloudflare bypass)
- `scrape-bell-house.sh` - Bell House
- `scrape-gotham.sh` - Gotham Comedy Club

**Why Custom Scrapers?**
- Comedy Cellar: Must iterate through 28 date options
- Union Hall: Lazy loading requires scrolling
- UCB/Gotham/Bell House: Cloudflare protection
- The Stand/Caveat: Better structured data from venue sites

### Los Angeles (DoLA.com + Custom + Venues)

**Sources:**
1. Category: `/events/comedy` (181 shows)
2. Venue pages: Dynasty, Hollywood Improv, Laugh Factory (110 shows)
3. Custom scrapers: UCB, Comedy Store, Largo (161 shows)
4. Merge & filter: 321 unique shows

**Scrapers:**
- `scrape-category.py` - DoLA category
- `scrape-dola-venues.py` - DoLA venue pages (3 venues)
- `scrape-ucb-la.py` - UCB Franklin
- `scrape-comedy-store.py` - All Comedy Store rooms
- `scrape-largo.sh` - Largo at the Coronet
- `scrape-dynasty-typewriter.py` - Dynasty (Squarespace site)

**Preferred Venues:**
- UCB Franklin, Comedy Store (all rooms)
- Largo, Dynasty Typewriter
- Hollywood Improv, Laugh Factory, Groundlings

---

## Data Format

### Input (Individual Scrapers)

Each scraper outputs:
```json
{
  "shows": [
    {
      "title": "Show Name",
      "venue": "Venue Name",
      "date": "2026-03-19T19:00:00Z",
      "time": "7:00 PM",
      "description": "Optional description",
      "url": "https://ticketlink.com"
    }
  ],
  "lastUpdated": "2026-03-19T10:00:00Z",
  "venue": "Venue Name",
  "totalShows": 42
}
```

### Output (Merged Data)

Merge scripts produce:
```json
{
  "shows": [...],
  "lastUpdated": "2026-03-19T10:30:00Z",
  "totalShows": 159,
  "sources": ["Do312 Comedy Category", "Do312 Venue Pages"]
}
```

**Deduplication Key**: `(venue, date[:10], time, title[:50])`

**Stale Filter**: Removes shows before today's date

---

## Common Tasks

### Add a New Venue Scraper

1. **Create the scraper:**
   ```bash
   cd scrapers/{city}
   cp scrape-ucb-ny.py scrape-new-venue.py
   # Edit scrape-new-venue.py with new venue URL/logic
   ```

2. **Add to master script:**
   ```bash
   # Edit scrapers/{city}/scrape-all-{city}.sh
   # Add: bash scrape-new-venue.sh
   ```

3. **Update merge script:**
   ```python
   # Edit scrapers/{city}/merge-{city}-shows.py
   # Add to sources list: 'new-venue-shows.json'
   ```

4. **Update frontend:**
   ```javascript
   // Edit public/{city}/app.js
   // Add venue to PREFERRED_VENUES array
   ```

### Debug a Failing Scraper

```bash
# Run individually with output
cd scrapers/{city}
bash -x scrape-venue.sh 2>&1 | tee debug.log

# For Python scrapers
python3 -v scrape-venue.py 2>&1 | tee debug.log
```

**Common Issues:**
- **Cloudflare blocking**: Use `cloudscraper` instead of `requests`
- **Lazy loading**: Add scrolling with `agent-browser eval`
- **Date parsing**: Sites may have changed date formats
- **Empty results**: Check if HTML structure changed

### Update Scraping Schedule

For production, set up a cron job:
```bash
crontab -e

# Run daily at 6 AM
0 6 * * * cd /path/to/project && ./deploy.sh >> logs/scrape.log 2>&1
```

### Verify Data Quality

```bash
# Check show counts
python3 << EOF
import json
for city in ['chicago', 'ny', 'la']:
    path = f'data/{city}/{"ny-shows" if city=="ny" else "la-shows" if city=="la" else "shows"}.json'
    data = json.load(open(path))
    print(f"{city.upper()}: {len(data['shows'])} shows")
EOF

# Check for stale data
python3 << EOF
import json
from datetime import datetime
data = json.load(open('data/chicago/shows.json'))
dates = [s['date'][:10] for s in data['shows']]
print(f"Date range: {min(dates)} to {max(dates)}")
print(f"Today: {datetime.now().date()}")
EOF
```

---

## Deployment

### Local Testing

1. Run scrapers: `./deploy.sh`
2. Open HTML files in browser
3. Verify show counts and dates

### Production Deployment

**Option 1: Static Hosting (GitHub Pages, Netlify)**
```bash
# Deploy public/ folder
cd public
git init
git add .
git commit -m "Deploy"
git push origin main
```

**Option 2: Server with Cron**
```bash
# Install on server
git clone repo
cd repo
pip3 install -r requirements.txt

# Set up cron
0 6 * * * cd /path/to/repo && ./deploy.sh
```

**Option 3: GitHub Actions**
```yaml
name: Update Shows
on:
  schedule:
    - cron: '0 6 * * *'
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: ./deploy.sh
      - run: git add data/ && git commit -m "Update" && git push
```

---

## Troubleshooting

### Problem: "No shows scraped"

**Check:**
1. Website structure changed? Inspect HTML
2. Cloudflare blocking? Use `cloudscraper`
3. JS rendering? Use `agent-browser` or `playwright`
4. Rate limiting? Add delays between requests

### Problem: "Stale data showing on site"

**Fix:**
```bash
# Re-run merge to filter old shows
cd scrapers/{city}
python3 merge-{city}-shows.py
```

### Problem: "Duplicate shows"

**Check deduplication logic in merge script:**
- Venue names must match exactly
- Time formats must be consistent
- Consider normalizing titles (lowercase, strip whitespace)

### Problem: "Preferred venue not showing"

**Check:**
1. Venue name in scraper matches frontend exactly
2. Scraper is included in `scrape-all-{city}.sh`
3. Output file is listed in merge script
4. Shows have recent dates (not filtered as stale)

---

## Performance Tips

1. **Run scrapers in parallel:**
   ```bash
   # In scrape-all-{city}.sh
   scrape-venue1.sh &
   scrape-venue2.sh &
   scrape-venue3.sh &
   wait
   ```

2. **Cache category page results:**
   - Category pages change less frequently
   - Consider caching for 6-12 hours

3. **Minimize browser automation:**
   - Use static scraping when possible
   - Browser automation (agent-browser) is slower

4. **Add request delays:**
   - Be respectful of server load
   - 1-2 second delays between requests

---

## Future Improvements

**Potential Enhancements:**
- [ ] Email notifications for scraper failures
- [ ] Historical data tracking (show popularity over time)
- [ ] Artist/comedian aggregation (shows by performer)
- [ ] Ticket price tracking
- [ ] Venue capacity/seating info
- [ ] User accounts for saved favorites
- [ ] Mobile app
- [ ] iCal export
- [ ] Location-based filtering (by neighborhood)
- [ ] Show recommendations based on user history

**Technical Debt:**
- [ ] Add unit tests for scrapers
- [ ] Centralize configuration (venues, URLs)
- [ ] Add schema validation for JSON outputs
- [ ] Improve error handling and logging
- [ ] Add retry logic with exponential backoff

---

## Contributing

When adding new features:

1. **Test locally first**: Run scraper multiple times
2. **Verify data format**: Match existing JSON structure
3. **Update documentation**: Add to this guide
4. **Check data protection**: Don't overwrite good data with empty results
5. **Commit with clear messages**: Explain what and why

---

## Contact & Support

For issues or questions, check:
- `archive/old-docs/` - Historical development notes
- Scraper source code - Often has inline comments
- Data files - Verify structure and format
