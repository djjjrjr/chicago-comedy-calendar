# The Stand NYC Scraper - Implementation Summary

## Overview
Successfully built and integrated a custom scraper for The Stand comedy club in NYC.

## Files Created/Modified

### New Files
- **scrape-the-stand.sh** - Executable scraper script using agent-browser
- **the-stand-shows.json** - Output file with scraped show data

### Modified Files
- **scrape-all-ny.sh** - Added The Stand to the scraping pipeline
- **merge-ny-shows-v2.py** - Added The Stand to the merger sources list
- **merge-ny-shows.sh** - Added The Stand to the embedded merger script

## Implementation Details

### Scraping Method
- **Tool**: agent-browser (same as Comedy Cellar, Caveat, Union Hall)
- **Source URL**: https://thestandnyc.com/shows
- **Structure**: DOM-based with h2/h3 heading pairs
  - h2: Show title (with link)
  - h3: Date, time, and room info

### Data Extraction Pattern
The scraper extracts:
- **Title**: From h2 heading text
- **Venue**: "The Stand" with room suffix (Upstairs/Main room)
- **Date**: Parsed from h3 heading (e.g., "March 18 | 7:00 PM UPSTAIRS")
- **Time**: Extracted from h3 heading
- **Description**: Show title (includes comedian names)
- **URL**: Link from h2 heading

### Show Count
- **Current Scrape**: 20 shows
- **Date Range**: 4 days (March 18-21, 2026)
- **Breakdown**: 
  - The Stand - Upstairs: 10 shows
  - The Stand - Main room: 10 shows

## Challenges Encountered

1. **Website Scope**: The Stand's website only displays ~4 days of shows at a time, not the full month like some other venues. This is why we got 20 shows instead of 24+.

2. **Duplicate h2 Elements**: The page structure includes some duplicate h2 elements in the DOM (42 total h2s but only 20 unique shows).

3. **Bot Detection**: The site has Cloudflare protection, but agent-browser handles it successfully.

4. **Date Parsing**: Had to handle year rollover logic to correctly assign dates to 2026 vs 2027.

## Integration Status

✅ Scraper built and tested
✅ Added to scrape-all-ny.sh pipeline
✅ Integrated into merge-ny-shows-v2.py
✅ Integrated into merge-ny-shows.sh
✅ Shows appear in final ny-shows.json output

## Final Merged Data
After integration, the NY shows database now includes:
- **Total Shows**: 426 (up from 406)
- **The Stand Shows**: 20 unique shows
- **Sources**: DoNYC, Caveat, Union Hall, Comedy Cellar, The Stand, UCB Theatre

## Testing
All tests pass:
- ✅ Scraper runs successfully
- ✅ JSON output is properly formatted
- ✅ Venue names are normalized correctly
- ✅ Shows merge without duplicates
- ✅ Pipeline integration works end-to-end
