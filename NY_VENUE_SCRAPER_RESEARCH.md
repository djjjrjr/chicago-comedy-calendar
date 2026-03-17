# NY Venue Scraper Research - Custom Scraper Feasibility

Investigation completed: March 17, 2026

## Summary

Investigated 4 major NY comedy venues not appearing in DoNYC data to determine feasibility of building custom scrapers.

## Venues Investigated

### 1. ✅ Comedy Cellar - **SCRAPABLE**

**Website:** https://www.comedycellar.com/new-york-line-up/

**Structure:**
- Date dropdown selector with ~30 days of future dates
- Shows listed for selected date
- Multiple venues/rooms: MacDougal Street, Village Underground, Fat Black Pussycat (Bar)
- Each show displays: Time, Venue/Room, Comedians (with links to bios)

**Data Format:**
```
6:45 pm show - MacDougal Street
Jon Laster (WINNER OF STAND UP NBC)
Orion Levine (COMEDY CENTRAL, THE LATE LATE SHOW WITH JAMES CORDEN)
Jeff Arcuri (THE LATE SHOW WITHSTEPHEN COLBERT)
...
```

**Scraping Approach:**
1. Iterate through date dropdown options
2. Select each date
3. Wait for shows to load
4. Extract show time, venue/room, and performer names
5. Create events per show

**Complexity:** Medium
- Dynamic dropdown requires Playwright
- Well-structured HTML
- Need to handle multiple rooms as separate venues or combined

**Estimated Dev Time:** 4-6 hours

---

### 2. ✅ Union Hall - **SCRAPABLE**

**Website:** https://unionhallny.com/calendar

**Structure:**
- Visual calendar grid with event cards
- Each card shows: Date, Event image, Title, Description
- Mix of comedy and music events

**Data Format:**
- Calendar view with clickable event cards
- Events have dates displayed on cards (e.g., "Mar 18")
- Need to identify which events are comedy vs other types

**Scraping Approach:**
1. Load calendar page
2. Extract all event cards
3. Parse date from card
4. Extract title and click through for details if needed
5. Filter for comedy-related keywords

**Complexity:** Medium
- Visual layout may require careful selector work
- Need keyword filtering for comedy events
- May need to click into individual events for full details

**Estimated Dev Time:** 4-6 hours

---

### 3. ❌ Carolines on Broadway - **CLOSED/INACTIVE**

**Website:** https://www.carolines.com

**Status:** **VENUE APPEARS TO BE CLOSED**

**Findings:**
- Homepage shows: "Thank You for 30 Years of Laughter in Times Square!"
- Message about following social media for "latest news"
- No active shows or calendar
- Redirects to New York Comedy Festival website

**Recommendation:** **Remove from preferred venues list** - venue is not operating

---

### 4. ⚠️ UCB Theatre - **CLOUDFLARE PROTECTED**

**Website:** https://ucbcomedy.com/shows

**Status:** Behind Cloudflare protection, cannot scrape with standard tools

**Findings:**
- Cloudflare "Just a moment..." challenge page
- Cannot access with automated browser tools
- Would require:
  - Cloudflare bypass techniques (unreliable, may violate ToS)
  - Manual token extraction
  - Proxy rotation

**Complexity:** Very High / Not Recommended
- Cloudflare makes automated scraping extremely difficult
- Even with bypass, would be fragile and high-maintenance
- Risk of IP blocks

**Alternative:** Check if UCB lists shows on other platforms (Instagram, Eventbrite, etc.)

---

## Recommendations

### Option A: Implement 2 Custom Scrapers (Recommended)
**Venues:** Comedy Cellar + Union Hall

**Pros:**
- These 2 venues are clearly scrapable
- Would add significant value (Comedy Cellar is very popular)
- Moderate development effort
- Combined with DoNYC data, would cover major venues

**Cons:**
- Maintenance needed if sites change
- Still missing UCB Theatre

**Implementation:**
1. Build `comedy-cellar-scraper.py`
2. Build `union-hall-scraper.py`
3. Update `ny-scraper.py` to merge all 3 data sources
4. Update preferred venues list to remove Carolines

---

### Option B: Keep DoNYC Only
**Accept:** Only venues with DoNYC listings appear as "preferred"

**Pros:**
- No additional maintenance
- Single data source
- Reliable

**Cons:**
- Missing Comedy Cellar (major venue)
- Less comprehensive coverage

---

### Option C: Partial Implementation
**Immediate:** Build Comedy Cellar scraper only (highest value)
**Later:** Add Union Hall when needed

---

## Updated Preferred Venues Recommendation

**Current List:**
1. Comedy Cellar ❌ (not in DoNYC, **needs custom scraper**)
2. Gotham Comedy Club ✅ (in DoNYC)
3. The Stand ✅ (in DoNYC)
4. The Bell House ✅ (in DoNYC)
5. Union Hall ❌ (not in DoNYC, **needs custom scraper**)
6. Carolines on Broadway ❌ (**CLOSED - REMOVE**)
7. UCB Theatre ❌ (not scrapable)

**Recommended New List (if going with custom scrapers):**
1. Comedy Cellar (custom scraper)
2. Gotham Comedy Club (DoNYC)
3. The Stand (DoNYC)
4. The Bell House (DoNYC)
5. Union Hall (custom scraper)
6. Eastville Comedy Club (DoNYC) - **NEW** (6 shows currently)
7. The PIT Loft (DoNYC) - **NEW** (4 shows currently)

---

## FINAL DECISION (March 17, 2026)

**Venues to Scrape:**
1. ✅ Comedy Cellar (custom scraper with date dropdown)
2. ✅ Union Hall (custom scraper with calendar)
3. ✅ UCB Theatre (custom scraper with Playwright stealth mode to bypass Cloudflare)

**Carolines Replacement:** **The Stand** (already in DoNYC data with 6 shows)

**Final Preferred Venues List:**
1. Comedy Cellar (custom scraper)
2. Gotham Comedy Club (DoNYC)
3. The Stand (DoNYC) - **REPLACES CAROLINES**
4. The Bell House (DoNYC)
5. Union Hall (custom scraper)
6. The Stand (DoNYC) - wait, duplicate! Need to pick between Stand and another venue
7. UCB Theatre (custom scraper with stealth mode)

**Corrected Final List:**
1. Comedy Cellar (custom scraper)
2. Gotham Comedy Club (DoNYC)
3. The Stand (DoNYC) - replaces Carolines
4. The Bell House (DoNYC)
5. Union Hall (custom scraper)
6. Comic Strip Live NYC (DoNYC) - historic venue
7. UCB Theatre (custom scraper)

## Next Steps

**Implementation Plan:**
1. Create `comedy-cellar-scraper.py` (medium complexity)
2. Create `union-hall-scraper.py` (medium complexity)
3. Create `ucb-theatre-scraper.py` (high complexity - stealth mode, can run less frequently)
4. Modify `ny-scraper.py` to be a merger script that:
   - Runs DoNYC scraper
   - Runs Comedy Cellar scraper
   - Runs Union Hall scraper
   - Runs UCB scraper (with error handling for Cloudflare failures)
   - Merges all data into `ny-shows.json`
   - Deduplicates if same show appears in multiple sources
5. Update NY preferred venues list
6. Add venue info for new venues
7. Update HTML filter buttons
8. Configure UCB scraper to run less frequently (e.g., twice per day instead of daily)

**Estimated Total Time:** 12-18 hours for complete implementation
