# Comedy Calendar - Chicago, NY & LA

A comprehensive comedy show aggregator for three cities, using a dual-scraping approach for maximum coverage.

## 📊 Current Show Counts

- **Chicago**: 159 shows
- **New York**: 316 shows
- **Los Angeles**: 321 shows
- **Total**: 796 comedy shows

## 🏗️ Project Structure

```
.
├── scrapers/          # All scraping scripts
│   ├── chicago/       # Chicago scrapers (Do312)
│   ├── ny/            # NY scrapers (DoNYC + venues)
│   └── la/            # LA scrapers (DoLA + venues)
├── data/              # JSON data outputs
│   ├── chicago/       # shows.json, venue-info.json
│   ├── ny/            # ny-shows.json + venue files
│   └── la/            # la-shows.json + venue files
├── public/            # Static website files
│   ├── chicago/       # index.html, app.js, styles.css
│   ├── ny/            # index.html, app.js, styles.css
│   └── la/            # index.html, app.js, styles.css
├── docs/              # Documentation
├── archive/           # Deprecated/old files
└── design-options/    # Alternative CSS themes

```

## 🚀 Quick Start

### Scrape All Cities

```bash
# Chicago
./scrapers/chicago/scrape-all.sh

# New York
./scrapers/ny/scrape-all-ny.sh

# Los Angeles
./scrapers/la/scrape-all-la.sh
```

### View the Sites

Open the HTML files in your browser:
- Chicago: `public/chicago/index.html`
- New York: `public/ny/index.html`
- Los Angeles: `public/la/index.html`

## 🎯 Dual Scraping Approach

Each city uses a **dual approach** for comprehensive coverage:

### 1. Category Scraping (Broad Discovery)
- Scrapes the main comedy category page (Do312/DoNYC/DoLA)
- Captures shows at both preferred and other venues
- Good for discovering new venues

### 2. Custom Scrapers (Deep Coverage)
- Dedicated scrapers for preferred venues
- Handles venue-specific quirks (lazy loading, date selectors, etc.)
- Ensures we get ALL shows from key venues

### 3. Deduplication
- Merges both sources
- Removes duplicates based on (venue, date, time, title)
- Filters out stale shows (before today)

## 📋 Scrapers by City

### Chicago (Do312)
- **Category**: `scrape-category.py` - Comedy category page
- **Venues**: `scrape-do312-venues.py` - All 7 preferred venue pages
- **Merge**: `merge-chicago-shows.py`

**Preferred Venues**:
- The Second City
- iO Theater
- Annoyance Theatre
- Zanies Comedy Club
- Laugh Factory
- The Lincoln Lodge
- Den Theatre

### New York (DoNYC + Custom)
- **Category**: `scrape-category.py` - DoNYC comedy category
- **Custom Scrapers**:
  - `scrape-caveat.sh` - Caveat calendar
  - `scrape-union-hall.sh` - Union Hall (with lazy loading)
  - `scrape-comedy-cellar.sh` - Comedy Cellar (multi-date)
  - `scrape-the-stand.sh` - The Stand
  - `scrape-ucb-ny.py` - UCB Theatre
  - `scrape-bell-house.sh` - The Bell House
  - `scrape-gotham.sh` - Gotham Comedy Club
- **Merge**: `merge-ny-shows.py`

**Preferred Venues**:
- UCB Theatre
- Comedy Cellar (all rooms)
- Union Hall
- Caveat
- The Stand
- The Bell House
- Gotham Comedy Club

### Los Angeles (DoLA + Custom)
- **Category**: `scrape-category.py` - DoLA comedy category
- **Venue Pages**: `scrape-dola-venues.py` - Dynasty, Hollywood Improv, Laugh Factory
- **Custom Scrapers**:
  - `scrape-ucb-la.py` - UCB Franklin
  - `scrape-largo.sh` - Largo at the Coronet
  - `scrape-comedy-store.py` - The Comedy Store (all rooms)
  - `scrape-dynasty-typewriter.py` - Dynasty Typewriter
- **Merge**: `merge-la-shows.py`

**Preferred Venues**:
- UCB FRANKLIN
- The Comedy Store (all rooms)
- Largo at the Coronet
- Dynasty Typewriter
- Hollywood Improv
- The Laugh Factory
- The Groundlings Theatre

## 🛠️ Technologies Used

- **Python**: Main scraping language
- **agent-browser**: CLI browser automation for JS-heavy sites
- **cloudscraper**: Bypass Cloudflare protection
- **BeautifulSoup**: HTML parsing
- **Playwright**: Dynamic site scraping
- **Bash**: Orchestration scripts

## 📦 Data Format

All data files follow this structure:

```json
{
  "shows": [
    {
      "title": "Show Name",
      "venue": "Venue Name",
      "date": "2026-03-19T19:00:00Z",
      "time": "7:00 PM",
      "description": "Show description...",
      "url": "https://..."
    }
  ],
  "lastUpdated": "2026-03-19T10:30:00Z",
  "totalShows": 159,
  "sources": ["Do312 Comedy Category", "Do312 Venue Pages"]
}
```

## 🔧 Maintenance

### Add a New Venue

1. Create a scraper in `scrapers/{city}/`
2. Add it to `scrape-all-{city}.sh`
3. Add the venue to `merge-{city}-shows.py` sources
4. Update the preferred venues list in the frontend

### Update Scraping Schedule

Recommended: Run scrapers daily to keep data fresh.

### Troubleshooting

**"No shows found"**: Check if the website structure changed
**"Stale data"**: Run the merge script to filter old shows
**"Missing venue"**: Verify venue name matches exactly in the scraper

## 📝 Notes

- All dates are stored in ISO format with timezone
- Stale shows (before today) are automatically filtered during merge
- Venue sub-rooms (e.g., Comedy Cellar rooms) are preserved for user clarity
- Data protection: Scrapers won't overwrite good data with empty results

## 🎨 Design Options

Alternative CSS themes are available in `design-options/`:
- Dark club theme
- Minimalist Chicago
- Retro poster style

## 📄 License

This is a personal project for aggregating publicly available comedy show listings.
