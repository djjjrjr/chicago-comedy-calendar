# Scraping Strategy Analysis: NY & LA

## Current Strategy Comparison

### ✅ CHICAGO (Complete - Best Practice)
**Dual Strategy:**
1. **Comedy Category Scraper** → 52 shows (broad coverage)
2. **Venue Page Scrapers** → 134 shows (7 preferred venues)
3. **Merger** → 159 unique shows (27 overlap removed)

**Why This Works:**
- Captures ALL comedy shows on Do312 (broad net)
- PLUS deep coverage of preferred venues (targeted net)
- Deduplication handles overlap
- **No venue is missed**

---

## NEW YORK (390 shows)

### Current Approach: **Custom Scrapers Only**

| Venue | Strategy | Source | Shows |
|-------|----------|--------|-------|
| Comedy Cellar | Custom scraper | comedycellar.com | 101 |
| Union Hall | Custom scraper | unionhallny.com | 91 |
| UCB Theatre | Custom scraper | ucbtheatre.com | 88 |
| Bell House | DoNYC venue page | donyc.com/venues | 49 |
| Gotham Comedy Club | DoNYC venue page | donyc.com/venues | 41 |
| Caveat | Custom scraper | caveat.nyc | 20 |
| The Stand | Custom scraper | thestandnyc.com | (included) |

**What We're NOT Doing:**
- ❌ Not scraping DoNYC comedy category at all
- ❌ Not systematically scraping ALL DoNYC venue pages

**Missing Coverage:**
- Other NY comedy venues not in our preferred list
- Shows at preferred venues that might be tagged differently
- Backup data if custom scrapers fail

### Would Chicago's Dual Approach Help NY?

**DoNYC Comedy Category Analysis:**
- Current scraper exists: `ny-scraper.py`
- Was capturing ~74 shows (but had data quality issues)
- We FIXED the data quality issues (removed non-comedy, LA venues, stale dates)
- **But we're not using it in the final merge!**

**Recommendation for NY:**
1. ✅ **USE the fixed DoNYC comedy category scraper** (currently being wasted)
2. ✅ **Keep all custom scrapers** (better coverage than DoNYC for preferred venues)
3. ✅ **Merge both sources** like Chicago does
4. ✅ **Optional**: Add systematic DoNYC venue page scraping for all 7 venues

**Estimated Impact:**
- DoNYC category: ~50-70 additional shows (non-preferred venues + backup)
- DoNYC venue pages: Minimal gain (custom scrapers already better)
- **Recommended**: Just add DoNYC category to merge → **~440-460 total shows**

---

## LOS ANGELES (354 shows)

### Current Approach: **Mixed Strategy**

| Venue | Strategy | Source | Shows |
|-------|----------|--------|-------|
| UCB FRANKLIN | Custom scraper | ucbtheatre.com | 99 |
| Dynasty Typewriter | DoLA venue page | dolosangeles.com/venues | 49 |
| Largo at the Coronet | Custom scraper | largo-la.com | 44 |
| Hollywood Improv | DoLA venue page | dolosangeles.com/venues | 42 |
| The Laugh Factory | DoLA venue page | dolosangeles.com/venues | 25 |
| The Comedy Store | Custom scraper | thecomedystore.com | 71 (all rooms) |
| Groundlings | DoLA category | dolosangeles.com/events | 1 |

**What We're NOT Doing:**
- ❌ Not scraping DoLA comedy category anymore
- ❌ Not using systematic DoLA venue page approach

**Current Sources Being Merged:**
1. UCB LA custom scraper ✅
2. Largo custom scraper ✅
3. Comedy Store custom scraper ✅
4. DoLA venue pages (3 venues) ✅
5. ~~DoLA comedy category~~ ❌ (was broken, not included in final merge)

### Would Chicago's Dual Approach Help LA?

**DoLA Comedy Category Analysis:**
- Scraper exists: `la-scraper.py`
- Was capturing ~40-50 shows
- **Status**: Not being used in current merge!

**Recommendation for LA:**
1. ✅ **FIX and RE-ENABLE DoLA comedy category scraper**
2. ✅ **Keep all custom scrapers and DoLA venue pages**
3. ✅ **Merge all sources** like Chicago does
4. ❌ **Don't add more venue page scrapers** (we have 3/7 covered, diminishing returns)

**Estimated Impact:**
- DoLA category: ~30-40 additional shows (other venues + backup)
- **Recommended**: Add DoLA category to merge → **~385-395 total shows**

---

## PACK THEATER QUESTION

**Status:** ❌ NOT included in any scraper
- DoLA has Pack Theater venue page with 1 event
- Not in preferred venues list
- Would need to be added to:
  - Preferred venues config
  - DoLA venue page scraper
  - OR just captured by DoLA category scraper if we re-enable it

---

## RECOMMENDATION SUMMARY

### **Priority 1: Re-Enable Category Scrapers** 🔴

#### NY - Add DoNYC Category Back
```bash
# Current merge only uses custom scrapers
# Should add: ny-scraper.py output to merge-ny-shows-v2.py
```
**Gain:** +50-70 shows → **~440-460 total**

#### LA - Add DoLA Category Back
```bash
# Current merge doesn't include la-scraper.py output
# Should add: la-shows-dola.json to merge-la-shows.py
```
**Gain:** +30-40 shows → **~385-395 total**

### **Priority 2: Consider Systematic Venue Page Scraping** 🟡

#### NY - Build DoNYC Venue Page Scraper (Like Chicago)
```python
# Similar to scrape-do312-venues.py
# Scrape all 7 NY preferred venues from DoNYC
```
**Pros:**
- Backup if custom scrapers fail
- Consistent with Chicago approach
- Easy to maintain

**Cons:**
- Custom scrapers already provide better coverage
- Minimal unique shows gained (~5-10 total)
- More complexity

**Recommendation:** 🤷 **Optional** - Only if you want consistency with Chicago

#### LA - Expand DoLA Venue Page Scraper
```python
# Add remaining 4 venues to scrape-dola-venues.py:
# - The Groundlings
# - Pack Theater (if desired)
# - etc.
```
**Recommendation:** 🤷 **Optional** - DoLA category would capture these

---

## FINAL COMPARISON

| City | Current Approach | Chicago-Style Dual Approach | Potential Gain |
|------|-----------------|----------------------------|----------------|
| **Chicago** | ✅ Dual (category + venues) | N/A - already doing it | N/A |
| **New York** | Custom scrapers only | + Add DoNYC category | +50-70 shows |
| **Los Angeles** | Custom + venue pages | + Add DoLA category | +30-40 shows |

### **Bottom Line:**

**YES, it would be beneficial to add category scrapers back to NY & LA!**

The dual approach (category + custom/venue scrapers) provides:
1. **Broad coverage** - Category scraper catches all venues
2. **Deep coverage** - Custom scrapers get more shows from preferred venues
3. **Redundancy** - If one fails, you still have data
4. **Best of both worlds** - Like Chicago's 159 shows vs 52 or 134 alone

**Estimated New Totals with Category Scrapers:**
- Chicago: 159 (already using dual approach)
- New York: **~440-460** (from 390)
- Los Angeles: **~385-395** (from 354)
- **Grand Total: ~985-1,015 shows** (vs current 903)

**Implementation:**
- NY: Add `ny-shows-donyc.json` to merge-ny-shows-v2.py
- LA: Add `la-shows-dola.json` to merge-la-shows.py (it's already in the code but file doesn't exist)
