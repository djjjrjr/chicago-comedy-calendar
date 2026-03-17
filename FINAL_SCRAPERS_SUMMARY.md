# Final NY Custom Scrapers Summary

## 🎯 Final Status: 3/4 Scrapers Working

### ✅ Successfully Implemented

| Scraper | Shows | Status | Script |
|---------|-------|--------|--------|
| **Caveat** | 124 | ✅ COMPLETE | `scrape-caveat.sh` |
| **Union Hall** | 16 | ✅ COMPLETE | `scrape-union-hall.sh` |
| **Comedy Cellar** | 10 | ✅ WORKING (single day) | `scrape-comedy-cellar.sh` |
| **TOTAL** | **150** | **3/4 working** | — |

### ❌ Blocked by Cloudflare

| Site | Status | Issue |
|------|--------|-------|
| **UCB Theatre NY** | ❌ BLOCKED | Cloudflare security verification |
| **UCB Theatre LA** | ❌ BLOCKED | Cloudflare security verification |

---

## 📊 Impact

### Current Data

| Source | Shows | Venues |
|--------|-------|--------|
| DoNYC | ~50 | Gotham Comedy Club, The Stand, The Bell House |
| Custom Scrapers | 150 | Caveat, Comedy Cellar, Union Hall |
| **TOTAL** | **~200** | **6 venues** |

**Improvement**: ~200 shows vs 74 original = **2.7x increase** ✨

---

## 🚧 Remaining Challenges

### 1. Comedy Cellar Multi-Day Scraping

**Issue**: Extending to 28 days takes too long (timeouts)
- Each date requires page reload (~3-5 seconds)
- 28 days × 5 seconds = 140+ seconds
- With browser operations, total time > 3 minutes

**Current Solution**: Use single-day scraper (10 shows)
- Reliable and fast (~10 seconds)
- Can be run daily to capture rotating lineup

**Potential Future Solution**:
- Investigate if Comedy Cellar has an API
- Run scraper at specific times when less busy
- Optimize sleep delays
- Or accept the longer runtime

### 2. UCB Theatre Cloudflare Protection

**Issue**: Both NY and LA UCB sites blocked by Cloudflare
- Message: "Performing security verification...This website uses a security service to protect against malicious bots"
- `agent-browser` cannot bypass (no stealth mode)
- Even with 30+ second waits, Cloudflare doesn't pass

**Attempted Solutions**:
- ✅ Extended wait times (15s, 30s) - FAILED
- ❌ Not attempted: Python + playwright-stealth (requires pip install)
- ❌ Not attempted: Paid proxy services

**Bypass Options** (not currently available in this environment):

**Option A: Python + Playwright Stealth**
```bash
pip install playwright playwright-stealth
playwright install chromium
```
```python
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def scrape_ucb():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        stealth_sync(page)  # Apply anti-detection

        page.goto('https://ucbcomedy.com/shows/new-york/')
        page.wait_for_timeout(10000)
        # Should bypass Cloudflare...
```

**Option B: Undetected ChromeDriver**
```python
import undetected_chromedriver as uc
driver = uc.Chrome()
driver.get('https://ucbcomedy.com/shows/new-york/')
```

**Option C: Paid Services**
- ScraperAPI
- Bright Data
- Oxylabs

**Recommendation**:
- **For NY**: Keep UCB in preferred list, note "Check UCB website for shows"
- **For LA**: Remove UCB FRANKLIN from preferred list (can't scrape)

---

## 📋 Final NY Preferred Venues Recommendation

### Scrapable Venues (6)

1. **Comedy Cellar** - Custom scraper (10 shows/day)
2. **Gotham Comedy Club** - DoNYC (~15 shows)
3. **The Stand** - DoNYC (~10 shows)
4. **The Bell House** - DoNYC (~15 shows)
5. **Union Hall** - Custom scraper (16 shows)
6. **Caveat** - Custom scraper (124 shows)

### Non-Scrapable (1)

7. **UCB Theatre** - ❌ Cloudflare blocked
   - Keep in list but add note
   - Link directly to ucbcomedy.com
   - Users can check UCB site manually

**Total**: 6 scrapable + 1 manual = 7 venues

---

## 🎨 LA Venues - UCB Issue

**Finding**: UCB LA (Franklin) is also Cloudflare protected

**Current LA Preferred Venues**:
1. The Comedy Store
2. The Laugh Factory
3. Hollywood Improv
4. **UCB FRANKLIN** ← ❌ Cannot scrape (Cloudflare)
5. Dynasty Typewriter
6. Largo at the Coronet
7. The Groundlings Theatre

**Recommendation for LA**:
- **Option A**: Remove UCB FRANKLIN, replace with scrape-able venue
- **Option B**: Keep UCB FRANKLIN with note "Check UCB website"
- **Option C**: Find alternative LA improv venue that's scrapable

---

## 🚀 Ready to Deploy

### Working Scrapers (Ready Now)

**New York:**
- ✅ `scrape-caveat.sh` → 124 shows
- ✅ `scrape-union-hall.sh` → 16 shows
- ✅ `scrape-comedy-cellar.sh` → 10 shows
- ✅ `ny-scraper.py` (DoNYC) → ~50 shows

**Total**: ~200 NY shows from 6 venues

**Los Angeles:**
- ✅ `la-scraper.py` (DoLA) → works for scrapable venues
- ❌ UCB LA cannot be scraped (Cloudflare)

---

## 📝 Next Steps

### Immediate (Phase 4)
1. Create merger script to combine NY data:
   - DoNYC output
   - Caveat output
   - Union Hall output
   - Comedy Cellar output
2. Normalize venue names (e.g., "Comedy Cellar - MacDougal" → "Comedy Cellar")
3. Remove duplicates
4. Test final ny-shows.json
5. Update GitHub Actions workflow

### Short-term
1. Decide on LA UCB FRANKLIN (keep or replace)
2. Add error handling to all scrapers
3. Add retry logic
4. Consider running Comedy Cellar scraper daily to get different dates

### Long-term (If Cloudflare Bypass Becomes Available)
1. Install Python + playwright-stealth
2. Build UCB NY scraper
3. Build UCB LA scraper
4. Add ~100-150 more shows

---

## 🎉 Success Metrics

**Achieved**:
- ✅ 3 custom scrapers working
- ✅ 150 shows from custom sources
- ✅ 200+ total shows (2.7x improvement)
- ✅ All major NY venues covered except UCB

**Excellent progress!** The calendar will be significantly more comprehensive even without UCB data.
