# Caveat NYC Scraper Analysis

## Summary

**✅ Caveat is HIGHLY scrapable** and has abundant comedy event data!

- **124 total events** scraped from https://caveat.nyc/events
- Events span from **March 2026 through December 2026**
- All events include: title, date, time, description, and ticket URL
- React-based website but loads all data client-side (no API calls needed)
- Simple scraping process using `agent-browser`

---

## Scraper Details

### Technology Stack
- **Website**: React.js (Material-UI components)
- **Scraping Method**: Browser automation with `agent-browser` (Playwright)
- **Data Structure**: MuiCard components with MuiTypography text elements

### Scraping Process
1. Navigate to https://caveat.nyc/events
2. Wait 3 seconds for React app to load
3. Click "SHOW ALL" button to load all events (not just the initial 20)
4. Extract data from `.MuiCard-root` elements
5. Parse date strings (e.g., "TUE, MAR 17") and add current year
6. Output to JSON file

### Script Location
- **Bash script**: `scrape-caveat.sh` (uses agent-browser)
- **Output file**: `caveat-shows.json`

---

## Sample Events

Here are some representative shows from Caveat:

1. **RISK! LIVE SHOW AND STORY SLAM** - Mar 17, 7:00 PM
   - True stories people never thought they'd share in public

2. **PITCH ROAST LIVE** - Mar 18, 7:00 PM
   - Comedy, startups, and venture capital together

3. **FACTS MACHINE: SCIENCE, COMEDY & TRIVIA!** - Mar 19, 7:00 PM
   - Science comedy show + trivia showdown

4. **NERD NITE** - Mar 28, 7:00 PM
   - Three fun-yet-informative presentations

5. **CHRIS REDD** - Apr 1, 9:30 PM
   - SNL alum, multifaceted stand-up talent

---

## Venue Characteristics

**Venue Focus**: "Smart, joyfully-nerdy comedy"

**Show Types**:
- Storytelling shows (RISK!, Story Collider)
- Science comedy (Facts Machine, Nerd Nite)
- Game shows (Facebook Marketplace Live, Three-Day Champion)
- PowerPoint comedy (Next Slide Please, Major Fix)
- Political/social commentary (Anti-Fascist Cabaret, Immigrant Jam)
- Improv (Raaaatscraps)
- Stand-up showcases
- Musical comedy
- Trivia nights

**Unique Selling Point**: Intellectual, themed comedy shows that blend entertainment with education/social commentary

---

## Data Quality

**Excellent!** Every event includes:
- ✅ Clear title
- ✅ Specific date (day of week + date)
- ✅ Exact time (e.g., "7:00 PM")
- ✅ Description (1-2 sentences)
- ✅ Direct ticket purchase URL

**Potential Issues**:
- Date parsing assumes current/next year (some dates might need adjustment)
- No price information included
- No performer names in structured format (embedded in titles/descriptions)

---

## Comparison to DoNYC

| Metric | DoNYC | Caveat Direct |
|--------|-------|---------------|
| **Events Found** | 0 | 124 |
| **Data Quality** | N/A | Excellent |
| **Update Frequency** | Daily scrape | Real-time |
| **Scraping Complexity** | Medium | Easy (browser automation) |
| **Maintenance Risk** | Low (aggregator) | Medium (venue-specific) |

**Caveat is NOT listed on DoNYC**, which is why we found 0 shows earlier.

---

## Recommendation

**✅ STRONGLY RECOMMEND adding Caveat to preferred venues**

### Reasons:
1. **Abundant data**: 124 shows (more than most other venues)
2. **Easy to scrape**: Simple process, works reliably
3. **Unique content**: Intellectual/nerdy comedy fills a niche
4. **Lower East Side location**: Good geographic diversity (Brooklyn boundary)
5. **Quality programming**: Mix of established names (Chris Redd) and innovative formats
6. **High activity**: Multiple shows per week

### Updated NY Preferred Venues Recommendation:
1. Comedy Cellar (custom scraper)
2. Gotham Comedy Club (DoNYC)
3. The Stand (DoNYC)
4. The Bell House (DoNYC)
5. Union Hall (custom scraper)
6. **Caveat** (custom scraper - **124 shows!**)
7. UCB Theatre (custom scraper with stealth)

**Replace**: Comic Strip Live NYC (2 shows) or Eastville (6 shows)
**With**: Caveat (124 shows + unique content)

---

## Integration Plan

To add Caveat to the calendar:

1. ✅ Scraper already created: `scrape-caveat.sh`
2. Add Caveat to `PREFERRED_VENUES` in `ny-app.js`
3. Add Caveat venue info (address, phone, website, map) to `venues` object
4. Add filter button for Caveat in `ny.html`
5. Update GitHub Actions workflow to run Caveat scraper
6. Merge Caveat data with DoNYC data in `ny-shows.json`

---

## Next Steps

Should we:
1. Add Caveat to the NY preferred venues list?
2. Keep Comic Strip Live NYC (historic prestige, 2 shows) or replace with Caveat (124 shows)?
3. Build the other custom scrapers (Comedy Cellar, Union Hall, UCB)?
