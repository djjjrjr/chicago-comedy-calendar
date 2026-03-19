# Comedy Scraper Fixes & Improvements - Implementation Plan

## Priority 1: Critical Fixes (Immediate Impact)

### 1. Fix Chicago Scraper Pagination ⚠️ CRITICAL
**Issue**: Scraper stops after page 1-2 because it looks for "Next" button that doesn't exist
**Impact**: Missing 99% of comedy events (5,000+ events across 200+ pages)
**Solution**: Use `?page=N` URL parameters instead of looking for Next button
**Estimated gain**: +4,900 shows
**Complexity**: Easy (modify pagination logic)
**Agent**: chicago-scraper-fixer

### 2. Fix NY Merge Script Deduplication ⚠️ CRITICAL
**Issue**:
- Comedy Cellar: 104 shows scraped → 11 in final data (93 shows lost)
- Caveat: 124 shows scraped → 20 in final data (104 shows lost)
**Impact**: Losing 197 already-scraped shows
**Solution**: Debug merge-ny-shows-v2.py deduplication logic
**Estimated gain**: +197 shows
**Complexity**: Medium (debugging logic)
**Agent**: ny-merge-debugger

### 3. Fix NY Scraper Data Quality ⚠️ HIGH
**Issue**: Scraping non-comedy events, LA venues, stale 2023-2024 dates
**Impact**: Polluting database with bad data
**Solution**: Add validation filters to ny-scraper.py
**Estimated gain**: Cleaner data, prevent corruption
**Complexity**: Easy (add filters)
**Agent**: ny-scraper-fixer

## Priority 2: Easy Wins (High ROI, Low Effort)

### 4. Build The Stand Custom Scraper (NY)
**Issue**: Only 6 shows captured, website has 24+ shows
**Website**: thestandnyc.com - HTML/DOM-based, VERY EASY to scrape
**Estimated gain**: +18-40 shows
**Complexity**: Easy (similar to Union Hall scraper)
**Agent**: stand-scraper-builder

### 5. Build Comedy Store Custom Scraper (LA)
**Issue**: Only 9 shows captured, website has 40+ shows
**Website**: thecomedystore.com - Static HTML calendar
**Estimated gain**: +30 shows
**Complexity**: Easy (straightforward HTML parsing)
**Agent**: comedy-store-scraper-builder

### 6. Build Largo Custom Scraper (LA)
**Issue**: Only 2 shows captured, website has 40+ shows
**Website**: largo-la.com - Static HTML
**Estimated gain**: +38 shows
**Complexity**: Easy (similar to Comedy Store)
**Agent**: largo-scraper-builder

## Priority 3: Medium Effort (Good ROI)

### 7. Improve Union Hall Scraper (NY)
**Issue**: Only capturing 16 shows, website has 80+ shows
**Solution**: Review and improve parsing logic
**Estimated gain**: +64 shows
**Complexity**: Medium (debug existing scraper)
**Agent**: union-hall-improver

### 8. Build Gotham Comedy Club Scraper (NY)
**Issue**: Only 2 shows captured, DoNYC venue page has 26 events
**Approach**: Scrape DoNYC venue page OR reverse-engineer their API
**Estimated gain**: +24 shows
**Complexity**: Medium (JavaScript-heavy)
**Agent**: gotham-scraper-builder

### 9. Build Bell House Scraper (NY)
**Issue**: Only 1 show captured, DoNYC venue page has 30 events
**Approach**: Scrape DoNYC venue page
**Estimated gain**: +29 shows
**Complexity**: Medium (Next.js/React)
**Agent**: bell-house-scraper-builder

## Priority 4: System Improvements

### 10. Apply Chicago's Data Protection to All Scrapers
**Issue**: NY and LA scrapers can overwrite good data with partial scrapes
**Solution**: Add smart save logic from scraper-improved.py
**Impact**: Prevent future data loss
**Complexity**: Easy (copy/paste with adjustments)
**Agent**: data-protection-applier

### 11. Extend UCB Theatre Date Range (NY)
**Issue**: Only covers 26 days, could extend further
**Solution**: Add pagination/date navigation to scraper
**Estimated gain**: +50-100 shows
**Complexity**: Medium
**Status**: Lower priority - already has decent coverage

## Expected Results

| Improvement | Current | After Fix | Gain |
|-------------|---------|-----------|------|
| **Chicago** | 61 | 5,000+ | +4,900 |
| **NY** | 209 | 500+ | +300 |
| **LA** | 130 | 235+ | +105 |
| **TOTAL** | 400 | 5,735+ | +5,335 |

## Implementation Strategy

### Phase 1: Critical Fixes (Day 1)
1. Fix Chicago pagination (chicago-scraper-fixer)
2. Fix NY merge script (ny-merge-debugger)
3. Fix NY data quality (ny-scraper-fixer)

**Expected: +5,097 shows**

### Phase 2: Easy Wins (Day 1-2)
4. The Stand scraper (stand-scraper-builder)
5. Comedy Store scraper (comedy-store-scraper-builder)
6. Largo scraper (largo-scraper-builder)

**Expected: +86-108 shows**

### Phase 3: Medium Effort (Day 2-3)
7. Union Hall improvement (union-hall-improver)
8. Gotham scraper (gotham-scraper-builder)
9. Bell House scraper (bell-house-scraper-builder)

**Expected: +117 shows**

### Phase 4: System Improvements (Day 3)
10. Apply data protection to all scrapers (data-protection-applier)

**Result: Prevent future data loss**

## Parallel Execution Plan

**Group A - Critical Fixes** (Run first, sequentially):
- chicago-scraper-fixer
- ny-merge-debugger
- ny-scraper-fixer

**Group B - NY Scrapers** (Run in parallel after Group A):
- stand-scraper-builder
- gotham-scraper-builder
- bell-house-scraper-builder
- union-hall-improver

**Group C - LA Scrapers** (Run in parallel with Group B):
- comedy-store-scraper-builder
- largo-scraper-builder

**Group D - System** (Run after all scrapers complete):
- data-protection-applier

## Success Metrics

- Chicago: 5,000+ shows (from 61)
- NY: 500+ shows (from 209)
- LA: 235+ shows (from 130)
- All scrapers have data protection
- No data quality issues (no non-comedy events, no stale dates)
- All preferred venues have custom scrapers or good coverage

## Notes

- Chicago scraper fix is HIGHEST priority - 99% of shows are missing
- NY merge fix is free gain - shows already scraped, just not appearing
- All new scrapers should follow Comedy Cellar pattern (agent-browser + multi-date)
- Test each scraper individually before integrating into pipeline
