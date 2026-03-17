# NY Custom Scrapers - Complete Implementation Plan

## Goal
Build 4 custom scrapers to supplement DoNYC data and achieve 400-500+ total NY comedy shows.

---

## Current Status

✅ **Caveat Scraper** - COMPLETE (124 shows)
✅ **Comedy Cellar Scraper** - PROTOTYPE (10 shows, needs multi-date extension)
⏳ **Union Hall Scraper** - TO BUILD
⏳ **UCB Theatre Scraper** - TO BUILD

---

## Implementation Sequence

### Phase 1: Extend Comedy Cellar Scraper ✅ PRIORITY
**Goal**: Scrape all 28 available dates (~280 shows)

**Current State**: Working prototype scrapes single day (10 shows)

**Implementation Steps**:
1. Modify script to iterate through date dropdown
2. For each date:
   - Select date option
   - Use `agent-browser click` to trigger date change
   - Wait for page update
   - Extract all shows for that date
3. Combine all shows into single output
4. Test with 7 days first, then extend to 28

**Challenges**:
- Need to trigger dropdown change properly (click + wait)
- Page may load dynamically after date selection
- May need delays between date selections

**Estimated Output**: ~280 shows (28 days × 10 shows/day)

**Time Estimate**: 30-45 minutes to build and test

---

### Phase 2: Build Union Hall Scraper 🔍 INVESTIGATE FIRST
**Goal**: Scrape Union Hall events

**Current State**: Haven't investigated website yet

**Investigation Steps**:
1. Open https://www.unionhallny.com
2. Find events/calendar section
3. Identify data structure:
   - Is it a calendar widget?
   - Static HTML or dynamic JS?
   - DoNYC embedded or custom?
4. Check if Cloudflare or bot protection exists
5. Determine scraping complexity

**Possible Scenarios**:
- **Best case**: Uses DoNYC widget (no scraper needed!)
- **Medium**: Simple event list (similar to Caveat)
- **Worst case**: Complex calendar or bot protection

**Estimated Output**: 20-50 shows

**Time Estimate**:
- Investigation: 10 minutes
- Build (if needed): 20-30 minutes
- Total: 30-40 minutes

---

### Phase 3: Build UCB Theatre Scraper 🛡️ STEALTH MODE
**Goal**: Scrape UCB shows with Cloudflare bypass

**URL**: https://ucbcomedy.com/shows/new-york/

**Known Issues**: Cloudflare protection detected

**Implementation Approach**:

#### Option A: Try agent-browser with stealth techniques
```bash
1. Open UCB page normally
2. Wait extended time for Cloudflare check
3. Look for "I'm human" button and click if needed
4. If successful, extract show data
```

**Stealth Techniques**:
- Longer initial wait (10-15 seconds)
- Randomized delays between actions
- Check for Cloudflare challenge selectors
- May need to accept cookies first

#### Option B: If Option A fails, use Playwright Python with stealth plugin
```python
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

# Launch with stealth mode
# Navigate to UCB
# Extract shows
```

**Data Structure** (need to investigate):
- Calendar view or list view?
- Show cards or table format?
- Pagination?

**Estimated Output**: 50-100 shows

**Time Estimate**:
- Option A attempt: 30 minutes
- Option B (if needed): 60 minutes
- Total: 30-90 minutes

---

### Phase 4: Normalize and Combine All Data 📊
**Goal**: Merge all scrapers + DoNYC into single ny-shows.json

**Steps**:
1. Create merger script: `merge-ny-scrapers.sh`
2. Combine data sources:
   - DoNYC scraper output (Gotham, Stand, Bell House)
   - Comedy Cellar scraper output
   - Union Hall scraper output
   - Caveat scraper output
   - UCB scraper output
3. Normalize venue names across sources
4. Remove duplicates (by venue + date + time)
5. Sort by date
6. Output to `ny-shows.json`

**Venue Name Normalization**:
```javascript
// Comedy Cellar sub-venues should all map to "Comedy Cellar"
"Comedy Cellar - MacDougal Street" → "Comedy Cellar"
"Comedy Cellar - Village Underground" → "Comedy Cellar"
"Comedy Cellar - Fat Black Pussycat" → "Comedy Cellar"
```

**Time Estimate**: 20-30 minutes

---

## Total Estimated Timeline

| Phase | Task | Time | Shows |
|-------|------|------|-------|
| ✅ Done | Caveat scraper | — | 124 |
| 1 | Extend Comedy Cellar | 45 min | 280 |
| 2 | Build Union Hall | 40 min | 20-50 |
| 3 | Build UCB Theatre | 60 min | 50-100 |
| 4 | Merge all data | 30 min | — |
| **Total** | — | **~3 hours** | **474-554** |

---

## Success Criteria

For each scraper:
- ✅ Runs without errors
- ✅ Outputs valid JSON
- ✅ Shows have: title, venue, date, time, url
- ✅ Dates are ISO format
- ✅ No duplicate shows within scraper

For integration:
- ✅ All scrapers combined into ny-shows.json
- ✅ Total shows > 400
- ✅ No duplicates across scrapers
- ✅ Venue names match PREFERRED_VENUES array
- ✅ Calendar displays correctly

---

## Execution Plan

### Immediate Next Steps:
1. ✅ Extend Comedy Cellar scraper to 28 days
2. ✅ Test and verify output
3. ✅ Build Union Hall scraper (after investigation)
4. ✅ Build UCB scraper (with stealth)
5. ✅ Create merger script
6. ✅ Update GitHub Actions workflow

### Parallel Work (Later):
- Update venue-info-scraper to include custom venues
- Add custom scrapers to GitHub Actions
- Set different run frequencies:
  - Daily: DoNYC, Caveat, Comedy Cellar, Union Hall
  - Weekly: UCB (more intensive)

---

## Fallback Plans

**If Union Hall is too complex**: Skip and move to UCB, revisit later

**If UCB Cloudflare can't be bypassed**:
- Document the issue
- Keep UCB in preferred list
- Note "Shows TBD" until solution found
- May need paid proxy service or more advanced techniques

**If scrapers break**:
- DoNYC data will still work (Gotham, Stand, Bell House = 50+ shows)
- Caveat adds 124 shows
- Calendar still functional with 174+ shows minimum

---

## Let's Begin! 🚀

Starting with Phase 1: Extending Comedy Cellar scraper to 28 days...
