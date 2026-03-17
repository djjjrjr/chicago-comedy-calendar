# Remaining Work Plan - Extended Comedy Cellar + UCB Scraper

## Goals

1. **Extend Comedy Cellar scraper** to scrape all 28 days (~280 shows)
2. **Build UCB Theatre scraper** with Cloudflare bypass (~50-100 shows)

---

## Task 1: Extend Comedy Cellar Scraper

### Current State
- ✅ Working prototype scrapes 1 day = 10 shows
- ❌ Multi-date iteration not working yet

### Challenge
The date dropdown requires proper selection and page reload logic.

### New Approach: Visit Each Date URL Directly
Instead of using dropdown, construct URLs for each date and visit them directly.

**Investigation needed:**
1. Check if Comedy Cellar uses date in URL parameters
2. If yes: construct URLs for each date
3. If no: use a simpler approach - reload page and scrape multiple times with delays

### Implementation Plan

**Option A: URL-based (if URLs change by date)**
```bash
# Example: https://www.comedycellar.com/new-york-line-up/?date=2026-03-17
for date in {0..27}; do
    url="https://www.comedycellar.com/new-york-line-up/?date_index=$date"
    agent-browser open $url
    # scrape
done
```

**Option B: Dropdown-based (simple iteration)**
```bash
# Open once, scrape multiple dates by selecting dropdown
agent-browser open https://www.comedycellar.com/new-york-line-up/
for i in {0..27}; do
    agent-browser eval "
        const select = document.querySelector('select');
        select.selectedIndex = $i;
        const event = new Event('change', { bubbles: true });
        select.dispatchEvent(event);
    "
    sleep 3  # Wait for page update
    # Extract and save shows
done
agent-browser close
```

**Option C: Hybrid - Open/close for each date (slower but reliable)**
```bash
for i in {0..13}; do  # First 14 days
    agent-browser open https://www.comedycellar.com/new-york-line-up/
    agent-browser select "select" "$i"
    sleep 2
    # Extract shows
    agent-browser close
done
```

### Estimated Time: 45-60 minutes

---

## Task 2: Build UCB Theatre Scraper with Cloudflare Bypass

### Challenge
UCB has Cloudflare "Performing security verification" that blocks automated browsers.

### Solution Options

#### Option 1: Python + Playwright Stealth (RECOMMENDED)
Use Python with `playwright-stealth` to bypass Cloudflare.

**Requirements:**
```bash
# Check if python3-playwright is available
python3 -m pip install playwright playwright-stealth
playwright install chromium
```

**Implementation:**
```python
#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def scrape_ucb():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Start visible
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...'
        )
        page = context.new_page()
        stealth_sync(page)  # Apply stealth

        page.goto('https://ucbcomedy.com/shows/new-york/', wait_until='networkidle')
        page.wait_for_timeout(10000)  # Wait for Cloudflare

        # Extract shows
        shows = page.evaluate('''() => {
            const events = [];
            // Extract show data
            return events;
        }''')

        browser.close()
        return shows
```

#### Option 2: Use undetected-chromedriver (Python alternative)
```python
import undetected_chromedriver as uc

driver = uc.Chrome()
driver.get('https://ucbcomedy.com/shows/new-york/')
# Wait and scrape
```

#### Option 3: Try agent-browser with extended delays
Sometimes Cloudflare will pass after extended waiting:
```bash
agent-browser open https://ucbcomedy.com/shows/new-york/
sleep 30  # Wait longer
agent-browser eval "document.title"  # Check if passed
```

#### Option 4: Investigate UCB's API (if exists)
Check network tab for JSON API endpoints that bypass Cloudflare.

### Recommended Approach: Try Option 3 First, Fall Back to Option 1

**Step 1:** Try extended wait with agent-browser
**Step 2:** If fails, build Python + playwright-stealth scraper
**Step 3:** If that fails, document and skip UCB for now

### Estimated Time:
- Option 3: 15 minutes
- Option 1: 60-90 minutes (if pip/playwright available)

---

## Execution Plan

### Part 1: Extend Comedy Cellar (45-60 min)
1. ✅ Test if Comedy Cellar uses URL parameters
2. ✅ Implement Option C (open/close per date) as reliable approach
3. ✅ Test with 7 dates first
4. ✅ Extend to all 28 dates
5. ✅ Verify output quality

### Part 2: Build UCB Scraper (30-90 min)
1. ✅ Try extended wait approach (Option 3)
2. ✅ If fails, check if Python + playwright available
3. ✅ Implement Python stealth scraper (Option 1)
4. ✅ Test and verify
5. ✅ Or document inability to bypass if all fail

---

## Success Metrics

### Comedy Cellar
- ✅ Successfully scrapes 28 dates
- ✅ ~280 shows (10 per day × 28 days)
- ✅ All venues captured (MacDougal, Underground, FBPC)
- ✅ Runs in < 5 minutes

### UCB Theatre
- ✅ Bypasses Cloudflare
- ✅ Extracts 50-100 shows
- ✅ Includes titles, dates, times, URLs
- ✅ Runs reliably

---

## Final Expected Output

| Scraper | Shows |
|---------|-------|
| DoNYC | 50 |
| Caveat | 124 |
| Comedy Cellar | 280 |
| Union Hall | 16 |
| UCB Theatre | 75 |
| **TOTAL** | **~545 shows** |

This would be a **7.4x increase** from the original 74 shows!

---

## Let's Start! 🚀

Beginning with Comedy Cellar extension...
