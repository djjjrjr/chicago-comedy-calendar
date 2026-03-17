# UCB Cloudflare Bypass Solutions

## Current Situation

**Both UCB sites are Cloudflare protected:**
- https://ucbcomedy.com/shows/new-york/
- https://ucbcomedy.com/shows/new-york/ny-month-view/ ← **Also blocked**
- https://ucbcomedy.com/shows/los-angeles/
- https://ucbcomedy.com/shows/los-angeles/la-month-view/ ← **Also blocked**

**Issue**: Cloudflare's "Performing security verification" detects automated browsers and blocks them.

---

## Solution Options (Ranked by Viability)

### ⭐ Option 1: Playwright Stealth (RECOMMENDED)

**What it is**: A Python library that makes Playwright browsers undetectable by anti-bot systems like Cloudflare.

#### How Playwright Stealth Works

**Normal browser automation leaves fingerprints:**
```javascript
// Cloudflare can detect these:
navigator.webdriver === true  // ❌ Exposed!
window.chrome === undefined   // ❌ Suspicious!
navigator.plugins.length === 0 // ❌ No plugins!
```

**Playwright Stealth removes these fingerprints:**
```python
from playwright_stealth import stealth_sync

# Stealth modifies the browser to:
# ✅ Set navigator.webdriver = undefined
# ✅ Add realistic chrome/plugin properties
# ✅ Spoof WebGL vendor/renderer
# ✅ Mask automation-related properties
# ✅ Add realistic permissions/languages
```

#### Implementation

**Requirements:**
```bash
# Check if pip is available
which pip3

# Install packages
pip3 install playwright playwright-stealth
playwright install chromium
```

**Scraper Code:**
```python
#!/usr/bin/env python3
"""
UCB Theatre Scraper with Cloudflare Bypass
"""

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import json
from datetime import datetime

def scrape_ucb_ny():
    shows = []

    with sync_playwright() as p:
        # Launch browser (headless=False for debugging)
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )

        # Create context with realistic settings
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York'
        )

        page = context.new_page()

        # Apply stealth mode - THIS IS THE KEY!
        stealth_sync(page)

        print("🌐 Navigating to UCB NY...")
        page.goto('https://ucbcomedy.com/shows/new-york/ny-month-view/', wait_until='domcontentloaded')

        # Wait for Cloudflare check (usually 5-10 seconds)
        print("⏳ Waiting for Cloudflare...")
        page.wait_for_timeout(10000)

        # Check if we bypassed Cloudflare
        title = page.title()
        if "Just a moment" in title:
            print("❌ Cloudflare still blocking")
            browser.close()
            return []

        print("✅ Bypassed Cloudflare!")

        # Wait for calendar to load
        page.wait_for_selector('.calendar-event', timeout=10000)

        # Extract shows
        shows = page.evaluate('''() => {
            const events = [];
            document.querySelectorAll('.calendar-event, .event-item, [class*="show"]').forEach(el => {
                const title = el.querySelector('.title, .event-title, h3, h4')?.textContent?.trim();
                const dateEl = el.querySelector('.date, time, [datetime]');
                const date = dateEl?.getAttribute('datetime') || dateEl?.textContent;
                const link = el.querySelector('a')?.href;

                if (title && date) {
                    events.push({
                        title: title,
                        venue: 'UCB Theatre',
                        date: date,
                        time: null,
                        description: null,
                        url: link || 'https://ucbcomedy.com/shows/new-york/'
                    });
                }
            });
            return events;
        }''')

        browser.close()

    return shows

if __name__ == '__main__':
    shows = scrape_ucb_ny()

    output = {
        'shows': shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'venue': 'UCB Theatre',
        'totalShows': len(shows)
    }

    with open('ucb-ny-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(shows)} UCB NY shows")
```

#### Success Rate
- **~80-90%** success rate with Playwright Stealth
- Cloudflare updates defenses periodically, may need tweaks
- Works well for moderate Cloudflare protection (like UCB)

---

### ⭐ Option 2: Undetected ChromeDriver (Alternative Python)

**What it is**: A modified ChromeDriver that's harder for Cloudflare to detect.

```python
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def scrape_ucb_selenium():
    # Automatically handles anti-detection
    driver = uc.Chrome()

    try:
        print("🌐 Opening UCB NY...")
        driver.get('https://ucbcomedy.com/shows/new-york/ny-month-view/')

        # Wait for Cloudflare
        import time
        time.sleep(10)

        # Check if passed Cloudflare
        if "Just a moment" not in driver.title:
            print("✅ Bypassed Cloudflare!")

            # Wait for events
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "calendar-event"))
            )

            # Extract shows using JavaScript
            shows = driver.execute_script('''
                return Array.from(document.querySelectorAll('.event-item')).map(el => ({
                    title: el.querySelector('.title')?.textContent?.trim(),
                    date: el.querySelector('.date')?.textContent?.trim(),
                    url: el.querySelector('a')?.href
                }));
            ''')

            return shows
        else:
            print("❌ Still blocked")
            return []

    finally:
        driver.quit()
```

**Installation:**
```bash
pip3 install undetected-chromedriver selenium
```

**Pros:**
- Often works where regular Selenium fails
- Simpler than Playwright Stealth
- Auto-updates ChromeDriver

**Cons:**
- Requires Chrome/Chromium installed
- Slightly less effective than Playwright Stealth

---

### Option 3: Paid Scraping Services (EASIEST but costs money)

#### ScraperAPI
```python
import requests

API_KEY = 'your_api_key'
url = 'https://ucbcomedy.com/shows/new-york/ny-month-view/'

response = requests.get(
    'https://api.scraperapi.com',
    params={
        'api_key': API_KEY,
        'url': url,
        'render': 'true'  # Render JavaScript
    }
)

html = response.text
# Parse HTML to extract shows
```

**Pricing:**
- $49/month for 100K requests
- $99/month for 300K requests
- Free tier: 5K requests

**Other Services:**
- **Bright Data** (formerly Luminati) - $500+/month, enterprise
- **Oxylabs** - Similar pricing
- **Crawlera/Zyte** - $25-100/month

**Pros:**
- ✅ Handles Cloudflare automatically
- ✅ No code changes needed
- ✅ High success rate (95%+)

**Cons:**
- ❌ Costs money (recurring)
- ❌ Overkill for small scraping needs

---

### Option 4: Cloudscraper (Python Library)

**What it is**: Python library specifically for bypassing Cloudflare.

```python
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'darwin',
        'desktop': True
    }
)

html = scraper.get('https://ucbcomedy.com/shows/new-york/ny-month-view/').text
# Parse HTML
```

**Installation:**
```bash
pip3 install cloudscraper
```

**Success Rate:**
- Works for **older Cloudflare challenges**
- May not work for newer "Performing security verification" (like UCB)
- Worth trying as it's simple

---

### Option 5: Browser Automation with Human-Like Behavior

**Concept**: Make the bot behave more human-like.

```python
import time
import random

# Random delays
time.sleep(random.uniform(2, 5))

# Mouse movements
page.mouse.move(random.randint(100, 900), random.randint(100, 700))

# Scroll naturally
for i in range(5):
    page.mouse.wheel(0, random.randint(100, 300))
    time.sleep(random.uniform(0.5, 1.5))

# Click around
page.click('body')
```

**Effectiveness**: Low (~20-30%) without stealth mode

---

### Option 6: Investigate UCB API/Hidden Endpoints

**Check if UCB loads data via API:**

```bash
# Open browser dev tools (Network tab)
# Filter for XHR/Fetch requests
# Look for JSON endpoints like:
# https://ucbcomedy.com/api/shows?venue=newyork
```

**If API found:**
```python
import requests

response = requests.get('https://ucbcomedy.com/api/shows', params={'venue': 'newyork'})
shows = response.json()
```

**Likelihood**: Medium - many modern sites use APIs

---

## Recommendation: Implementation Order

### 1️⃣ First Try: Playwright Stealth (Best option)
**Time**: 60-90 minutes
**Success Rate**: 80-90%
**Cost**: Free (just needs pip packages)

### 2️⃣ Fallback: Undetected ChromeDriver
**Time**: 30 minutes
**Success Rate**: 70-80%
**Cost**: Free

### 3️⃣ Quick Check: Cloudscraper
**Time**: 15 minutes
**Success Rate**: 30-50% (older Cloudflare)
**Cost**: Free

### 4️⃣ Last Resort: Paid Service
**Time**: 10 minutes to setup
**Success Rate**: 95%+
**Cost**: $49+/month

---

## Current Environment Limitations

**Issue**: Your current environment may not have `pip` or ability to install Python packages.

**Check availability:**
```bash
# Check for pip
which pip3
python3 -m pip --version

# Try to install
python3 -m pip install --user playwright
```

**If pip is NOT available**, options are:
1. Request pip installation in environment
2. Use paid service (ScraperAPI with REST API)
3. Run scraper on different machine that has Python/pip
4. Skip UCB scraping for now

---

## Monthly Calendar View (Your Question)

**You asked about using monthly calendar views:**
- https://ucbcomedy.com/shows/new-york/ny-month-view/
- https://ucbcomedy.com/shows/los-angeles/la-month-view/

**Result**: ❌ **Still Cloudflare protected**

**However, these may be BETTER targets because:**
1. ✅ Show all month's events on one page (no pagination)
2. ✅ Likely simpler HTML structure (calendar grid)
3. ✅ Easier to parse once Cloudflare is bypassed
4. ✅ Less JavaScript-heavy than main show pages

**Recommendation**: If you implement Playwright Stealth, target the monthly views!

---

## Next Steps

**If you want to proceed with UCB scraping:**

1. **Check if pip is available**:
   ```bash
   python3 -m pip --version
   ```

2. **If yes, I can build the Playwright Stealth scraper**

3. **If no, we have options:**
   - Use paid service (ScraperAPI trial)
   - Skip UCB for now (calendar still great with 6/7 venues)
   - Request environment with pip access

Would you like me to check if pip is available and attempt the Playwright Stealth implementation?
