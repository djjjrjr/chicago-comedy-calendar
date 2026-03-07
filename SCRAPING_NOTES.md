# Venue Scraping Research Notes

## Challenge

Most Chicago comedy venue websites use **heavy JavaScript rendering** and dynamic content loading. This means:
- Simple HTML scraping with BeautifulSoup won't work
- Content is loaded via JavaScript after page load
- Events may be fetched from APIs

## Approaches to Consider

### 1. **Browser Automation** (Recommended)
Use Playwright or Selenium to:
- Load pages with full JavaScript execution
- Wait for dynamic content to render
- Extract show data from rendered DOM

**Pros:**
- Works with any website
- Gets the exact data users see

**Cons:**
- Slower (2-5 seconds per page)
- More resources needed
- Needs headless browser in GitHub Actions

### 2. **Find Hidden APIs**
Many sites load data from JSON APIs. We could:
- Inspect network requests in browser dev tools
- Find the API endpoints they use
- Query APIs directly (much faster)

**Pros:**
- Very fast
- Clean JSON data
- No HTML parsing needed

**Cons:**
- APIs may be undocumented/private
- Could break if they change
- May need authentication or headers

### 3. **Third-Party Aggregators**
Use services that already aggregate comedy shows:
- Eventbrite API
- Bandsintown API
- Chicago event aggregators

**Pros:**
- Standardized data format
- Well-documented APIs
- Covers multiple venues

**Cons:**
- May not have all venues
- Data might be incomplete
- Rate limits

## Venue-Specific Notes

### Second City
- URL: https://www.secondcity.com/shows/chicago/
- Status: Heavy JavaScript, content not in initial HTML
- Likely uses API for show data

### iO Theater
- URL: https://ioimprov.com/chicago/schedule
- Status: Not yet tested
- Known for improv shows

### Annoyance Theatre
- URL: https://theannoyance.com/shows
- Status: Not yet tested
- Alternative theater, may have simpler site

### Zanies
- URL: https://chicago.zanies.com/events/
- Status: JavaScript-rendered, no events in initial HTML
- Uses ETIX ticketing system - may have API

### Laugh Factory
- URL: https://chicago.laughfactory.com/shows
- Status: Not yet tested
- Part of national chain

### Lincoln Lodge
- URL: https://www.lincolnlodge.com/calendar
- Status: Not yet tested
- Free shows, simpler site possible

### Den Theatre
- URL: https://thedentheatre.com/shows/
- Status: Not yet tested
- Multi-show venue

## Recommended Next Steps

1. **Use Playwright** in scraper.py instead of BeautifulSoup
2. **Inspect each venue** with browser dev tools to find:
   - API endpoints (Network tab)
   - DOM selectors for show data
   - Data structure
3. **Start with easiest venues** (Lincoln Lodge, Annoyance)
4. **Add Playwright to requirements.txt**
5. **Update GitHub Actions** to install Playwright browsers

## Alternative: Manual Updates

For MVP, we could:
- Manually update shows.json weekly
- Focus on building great UI/UX
- Add automation later when we have time to properly reverse-engineer each site

This is actually common for small comedy aggregators!
