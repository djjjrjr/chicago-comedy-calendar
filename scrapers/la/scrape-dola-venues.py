#!/usr/bin/env python3
"""
DoLA Venue Page Scraper for remaining LA venues
"""

import cloudscraper
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

VENUES = {
    'Dynasty Typewriter': 'dynasty-typewriter',
    'Hollywood Improv': 'hollywood-improv',
    'The Laugh Factory': 'the-laugh-factory'
}

def scrape_venue(venue_name, venue_slug):
    """Scrape a single venue from DoLA"""
    url = f'https://dolosangeles.com/venues/{venue_slug}'
    print(f"  📍 {venue_name}...")

    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'darwin', 'desktop': True}
    )

    try:
        response = scraper.get(url, timeout=30)
        if response.status_code != 200:
            print(f"     ❌ Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        shows = []
        seen_urls = set()
        event_links = soup.find_all('a', href=re.compile(r'/events/'))

        current_date = None

        for link in event_links:
            try:
                href = link.get('href')
                if not href or '/venues/' in href:
                    continue

                if href.startswith('/'):
                    href = f"https://dolosangeles.com{href}"

                if href in seen_urls:
                    continue

                text = link.get_text(strip=True)
                if not text or text.upper() == venue_name.upper() or text in ['BUY', 'GET TICKETS', '']:
                    continue

                # Check if this is a date header
                date_match = re.search(r'(TODAY|TOMORROW|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)\s+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})', text, re.IGNORECASE)
                if date_match:
                    current_date = text
                    continue

                title = text

                # Look for time
                time_str = None
                parent = link.find_parent(['div', 'li', 'article'])
                if parent:
                    parent_text = parent.get_text()
                    time_match = re.search(r'\d{1,2}:\d{2}\s?[AP]M', parent_text, re.IGNORECASE)
                    if time_match:
                        time_str = time_match.group(0).upper()

                # Parse date
                iso_date = None
                if current_date:
                    try:
                        date_match = re.search(r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})', current_date, re.IGNORECASE)
                        if date_match:
                            month_day = date_match.group(0)
                            current_year = datetime.now().year
                            date_obj = datetime.strptime(f"{month_day} {current_year}", "%b %d %Y")

                            if date_obj < datetime.now():
                                date_obj = date_obj.replace(year=current_year + 1)

                            iso_date = date_obj.isoformat() + 'Z'
                    except Exception as e:
                        pass

                if not iso_date:
                    iso_date = datetime.now().isoformat() + 'Z'

                seen_urls.add(href)

                shows.append({
                    'title': title,
                    'venue': venue_name,
                    'date': iso_date,
                    'time': time_str,
                    'description': None,
                    'url': href
                })

            except Exception as e:
                continue

        print(f"     ✓ {len(shows)} events")
        return shows

    except Exception as e:
        print(f"     ❌ Error: {e}")
        return []

def main():
    print("🎭 Starting DoLA Venue Page Scraper...")
    print(f"📋 Scraping {len(VENUES)} LA venues\n")

    all_shows = []
    venue_counts = {}

    for venue_name, venue_slug in VENUES.items():
        shows = scrape_venue(venue_name, venue_slug)
        all_shows.extend(shows)
        venue_counts[venue_name] = len(shows)

    # Deduplicate
    seen = set()
    unique_shows = []
    for show in all_shows:
        key = (show['title'], show['date'][:10] if show['date'] else '', show['venue'])
        if key not in seen:
            seen.add(key)
            unique_shows.append(show)

    # Save
    output = {
        'shows': unique_shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'totalShows': len(unique_shows),
        'source': 'DoLA Venue Pages'
    }

    with open('dola-venues-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scraping complete!")
    print(f"📊 Total: {len(all_shows)} events → {len(unique_shows)} unique")
    print(f"📝 Saved to dola-venues-shows.json\n")

    print("📋 Breakdown by venue:")
    for venue, count in sorted(venue_counts.items(), key=lambda x: -x[1]):
        print(f"  • {venue}: {count} events")

if __name__ == '__main__':
    main()
