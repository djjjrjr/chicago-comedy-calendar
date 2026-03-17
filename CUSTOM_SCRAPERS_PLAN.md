# Custom Scrapers Implementation Plan

## Overview

We need to build 3 custom scrapers for NY preferred venues:
1. **Comedy Cellar** - Complex (multiple venues, date dropdown)
2. **Union Hall** - Medium complexity
3. **UCB Theatre** - Complex (Cloudflare protection, needs stealth)

---

## 1. Comedy Cellar Scraper

### URL
`https://www.comedycellar.com/new-york-line-up/`

### Complexity: **HIGH**

### Data Structure
- **Date dropdown**: 28 days of lineups available
- **Multiple venues** per day:
  - MacDougal Street (main venue)
  - Village Underground
  - Fat Black Pussycat (Bar)
  - Fat Black Pussycat (Lounge)
- **Multiple showtimes** per venue (e.g., 6:45pm, 8:45pm, 10:45pm)
- **Performer lineups** for each showtime

### Example Shows
- "6:45 pm show - MacDougal Street" with performers: Jon Laster, Orion Levine, Jeff Arcuri, etc.
- "7:00 pm show - Robert Kelly: A One Man Show: Final Fat"
- "10:30 pm show - Hot Soup in the FBPC"

### Scraping Approach
```bash
1. Navigate to lineup page
2. Get all date options from dropdown (28 days)
3. For each date:
   a. Select date from dropdown
   b. Wait for page to update
   c. Extract all shows for that day:
      - Showtime
      - Venue location
      - Performer names
      - Show title (if special show)
   d. Create individual show entries
4. Combine all shows into single JSON
```

### Challenges
- Multiple venues need to be treated as separate shows
- Need to iterate through 28 dates
- Some shows have special titles, others are just lineup showcases
- Need to distinguish between venue locations

### Estimated Shows: **150-300** (multiple shows per day × 28 days)

---

## 2. Union Hall Scraper

### URL
`https://www.unionhallny.com/` (need to investigate events page)

### Complexity: **MEDIUM**

### Status
- Need to investigate website structure
- Likely has a calendar or events page
- May have similar structure to other Brooklyn venues

### Next Steps
1. Open Union Hall website
2. Find events/calendar page
3. Identify data structure
4. Determine if it's scrapable or uses DoNYC

### Estimated Shows: **20-50**

---

## 3. UCB Theatre Scraper

### URL
`https://ucbcomedy.com/shows/new-york/`

### Complexity: **VERY HIGH**

### Challenges
- **Cloudflare protection** (identified in earlier research)
- Requires **Playwright stealth mode** to bypass
- May need additional anti-detection measures

### Requirements
- Playwright with stealth plugin
- User agent spoofing
- Potential need for realistic browsing behavior
- May need to solve CAPTCHAs (hopefully not)

### Scraping Approach
```bash
1. Launch Playwright with stealth mode
2. Navigate with realistic delays
3. Accept any cookie notices
4. Find events calendar
5. Extract show data
6. Handle pagination if needed
```

### Estimated Shows: **50-100**

---

## Implementation Strategy

### Phase 1: Build Comedy Cellar Scraper ✓ PRIORITY
**Why first**: Highest show count, well-structured data, no bot protection

### Phase 2: Investigate Union Hall
**Why second**: Likely simpler than UCB, good to validate our approach

### Phase 3: Build UCB Theatre Scraper
**Why last**: Most complex, may need troubleshooting, can be run less frequently

---

## Technical Requirements

### Current Tools Available
- ✅ `agent-browser` (Playwright-based)
- ✅ Bash scripting
- ✅ JSON output format

### May Need
- Playwright stealth plugin (for UCB)
- Python environment with Playwright (for more complex logic)
- Retry logic for failed scrapes
- Rate limiting between requests

---

## Data Format

All scrapers should output shows in this format:

```json
{
  "shows": [
    {
      "title": "Show title or performer lineup",
      "venue": "Comedy Cellar - MacDougal Street",
      "date": "2026-03-17T00:00:00Z",
      "time": "8:45 PM",
      "description": "Performers: Jon Laster, Orion Levine, Jeff Arcuri",
      "url": "https://www.comedycellar.com/reservations/..."
    }
  ],
  "lastUpdated": "2026-03-17T17:00:00Z",
  "venue": "Comedy Cellar",
  "totalShows": 150
}
```

---

## Integration Plan

After building scrapers:

1. **Test each scraper individually**
2. **Create merger script** that combines:
   - DoNYC data (Gotham, The Stand, Bell House)
   - Comedy Cellar custom data
   - Union Hall custom data
   - Caveat custom data
   - UCB custom data
3. **Output to `ny-shows.json`**
4. **Update GitHub Actions workflow** to run all scrapers
5. **Set different frequencies**:
   - DoNYC + simple scrapers: Daily
   - UCB (with Cloudflare): Weekly or bi-weekly

---

## Next Immediate Steps

1. ✅ Build Comedy Cellar scraper
2. Test with sample dates
3. Verify data quality
4. Move to Union Hall investigation

---

## Success Criteria

- Each scraper runs without errors
- Data format matches existing structure
- Shows have valid dates, titles, and URLs
- No duplicate shows across scrapers
- Total NY shows increase from ~74 to **300-400+**
