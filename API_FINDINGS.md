# API Investigation Findings

## Key Discovery: Use Event Aggregators!

Instead of scraping each venue directly, we can use **event aggregator sites** that already collect this data.

### Do312.com

**Pros:**
- Has data for ALL Chicago venues
- Clean, structured HTML
- Updates regularly
- Easier to scrape than individual venue sites

**Example URL Structure:**
- `https://do312.com/venues/zanies` - Zanies events
- `https://do312.com/venues/second-city` - Second City events
- `https://do312.com/venues/io-theater` - iO Theater events

**Data Available:**
- Show title
- Date and time
- Venue
- Ticket links
- Sometimes performer names

**Scraping Approach:**
```python
from playwright.sync_api import sync_playwright

def scrape_do312_venue(venue_slug):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f'https://do312.com/venues/{venue_slug}')
        page.wait_for_selector('.event-item')  # or whatever class

        events = page.query_selector_all('.event-item')
        # Extract data...
```

## Alternative: Eventbrite API

Some venues use Eventbrite for ticketing. Eventbrite has an official API.

**API Example:**
```python
import requests

# Search for events by organizer or venue
response = requests.get(
    'https://www.eventbriteapi.com/v3/events/search/',
    headers={'Authorization': f'Bearer {token}'},
    params={
        'location.address': 'Chicago, IL',
        'q': 'comedy',
        'start_date.range_start': '2026-03-01T00:00:00',
        'start_date.range_end': '2026-03-31T23:59:59'
    }
)
```

**Venues that might use Eventbrite:**
- Need to check each venue's ticket links

## Recommended Strategy

### Phase 1: Use Do312 (Easiest)
1. Scrape Do312 for all 7 venues
2. One scraper, consistent format
3. All venues covered

### Phase 2: Direct APIs (If needed)
For venues not well-covered by Do312:
- Check if they use ETIX, Eventbrite, or other ticketing platforms
- Use those platforms' APIs

### Phase 3: Individual Scrapers (Last resort)
Only build these for venues that:
- Aren't on Do312
- Don't use standard ticketing platforms
- Have simple enough sites to scrape

## Venue Mapping for Do312

Need to find the correct slug for each venue:
- [ ] Second City: `/venues/second-city` (to verify)
- [ ] iO Theater: `/venues/io-theater` (to verify)
- [ ] Annoyance Theatre: `/venues/annoyance-theatre` (to verify)
- [x] Zanies: `/venues/zanies` ✓ confirmed
- [ ] Laugh Factory: `/venues/laugh-factory` (to verify)
- [ ] Lincoln Lodge: `/venues/lincoln-lodge` (to verify)
- [ ] Den Theatre: `/venues/den-theatre` (to verify)

## Next Steps

1. **Verify all venue slugs on Do312**
2. **Build single scraper for Do312**
3. **Test with all venues**
4. **Deploy to GitHub Actions**

This is MUCH simpler than building 7 different scrapers!
