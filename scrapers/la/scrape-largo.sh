#!/bin/bash
# Scrape Largo at the Coronet events using curl and parsing
# The venue lists events on their main page at largo-la.com

echo "🎭 Starting Largo at the Coronet scraper..."
echo "📍 Fetching events from largo-la.com..."

# Create a Python script to scrape and parse the HTML
python3 << 'PYTHON_SCRIPT'
import json
import re
from datetime import datetime
import subprocess
import html as html_lib

# Use curl to fetch the page
try:
    result = subprocess.run(
        ['curl', '-sL', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'https://largo-la.com'],
        capture_output=True,
        text=True,
        timeout=30
    )
    html = result.stdout
except Exception as e:
    print(f"Error fetching page: {e}")
    exit(1)

shows = []

# Parse event blocks - each event has:
# 1. <h2> with title and link
# 2. <p> with date like "Thu Mar 19"
# 3. <div class="price"> with price

# Find all event blocks by looking for the event-details div structure
event_blocks = re.finditer(
    r'<div class="event-details">.*?<h2>\s*<a[^>]*title="([^"]*)"[^>]*>([^<]+)</a>\s*</h2>.*?<p>\s*([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{1,2})',
    html,
    re.DOTALL
)

for match in event_blocks:
    title = html_lib.unescape(match.group(2).strip())
    date_str = match.group(3).strip()

    # Parse date (format: "Thu Mar 19")
    date_parts = date_str.split()
    if len(date_parts) >= 3:
        dow, month, day = date_parts[0], date_parts[1], date_parts[2]
    else:
        continue

    # Determine year (assume current or next year)
    year = 2026

    try:
        date_str_full = f"{month} {day}, {year}"
        date_obj = datetime.strptime(date_str_full, "%b %d, %Y")
        iso_date = date_obj.isoformat()
    except Exception as e:
        print(f"Error parsing date '{date_str_full}': {e}")
        continue

    # Determine time based on day of week
    if dow == 'Sun':
        show_time = "7:30 PM"
    else:
        show_time = "8:00 PM"

    # Check if there's a late show mentioned in title
    if 'late' in title.lower() or '10:00' in title or '10pm' in title.lower():
        show_time = "10:00 PM"

    # Try to find price in nearby HTML
    # Look for <div class="price"> near this event
    event_html = match.group(0)
    price_match = re.search(r'<div class="price"\s*>\$(\d+(?:\.\d+)?)', html[max(0, match.start()-500):match.end()+500])
    price = price_match.group(1) if price_match else "40.00"

    # Try to extract event URL
    url_match = re.search(r'href="(https://wl\.seetickets\.us/event/[^"]+)"', event_html)
    event_url = url_match.group(1) if url_match else "https://wl.seetickets.us/LargoAtTheCoronet"

    show = {
        "title": title,
        "venue": "Largo at the Coronet",
        "date": iso_date,
        "time": show_time,
        "description": f"${price}",
        "url": event_url
    }

    shows.append(show)

# Deduplicate shows
unique_shows = []
seen = set()

for show in shows:
    key = f"{show['venue']}|{show['date']}|{show['time']}|{show['title']}"
    if key not in seen:
        seen.add(key)
        unique_shows.append(show)

# Create output JSON
output = {
    "shows": unique_shows,
    "lastUpdated": datetime.now().isoformat(),
    "venue": "Largo at the Coronet",
    "totalShows": len(unique_shows)
}

# Write to file
with open('largo-shows.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"✅ Scraped {len(unique_shows)} shows from Largo at the Coronet")

PYTHON_SCRIPT

echo ""
echo "✅ Scraping complete!"
echo "📝 Results saved to largo-shows.json"
echo ""
echo "📋 Summary:"
python3 << 'SUMMARY_SCRIPT'
import json

try:
    with open('largo-shows.json', 'r') as f:
        data = json.load(f)

    print(f"Total shows: {data.get('totalShows', 0)}")
    print(f"Last updated: {data.get('lastUpdated', 'N/A')}")

    # Count by month
    from collections import Counter
    months = Counter()
    for show in data.get('shows', []):
        date = show.get('date', '')[:7]  # YYYY-MM
        if date:
            months[date] += 1

    print(f"\nShows by month:")
    for month in sorted(months.keys()):
        print(f"  {month}: {months[month]} shows")

    print("\nSample shows:")
    for show in data.get('shows', [])[:5]:
        print(f"  • {show['title']}")
        print(f"    {show['date'][:10]} at {show['time']}")

except Exception as e:
    print(f"Error reading results: {e}")

SUMMARY_SCRIPT
