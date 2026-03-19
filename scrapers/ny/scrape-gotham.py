#!/usr/bin/env python3
"""
Gotham Comedy Club Scraper - Scrapes from DoNYC venue page
"""

import cloudscraper
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_gotham():
    print("🎭 Starting Gotham Comedy Club scraper...")

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'desktop': True
        }
    )

    url = 'https://donyc.com/venues/gotham-comedy-club'
    print(f"📡 Fetching {url}")

    try:
        response = scraper.get(url, timeout=30)

        if response.status_code != 200:
            print(f"❌ Error: Status {response.status_code}")
            return []

        print(f"✅ Got {len(response.text)} characters")
        print("🔍 Parsing HTML...")

        soup = BeautifulSoup(response.text, 'html.parser')

        shows = []
        seen_urls = set()

        # Find all event links (exclude venue links)
        event_links = soup.find_all('a', href=re.compile(r'/events/'))

        print(f"📦 Found {len(event_links)} potential event links")

        current_date = None

        for link in event_links:
            try:
                href = link.get('href')
                if not href or '/venues/' in href:
                    continue

                # Make absolute URL
                if href.startswith('/'):
                    href = f"https://donyc.com{href}"

                # Skip duplicates
                if href in seen_urls:
                    continue

                # Get text content
                text = link.get_text(strip=True)

                # Skip if it's just the venue name
                if text.upper() == 'GOTHAM COMEDY CLUB':
                    continue

                # Skip navigation/metadata links
                if text in ['BUY', 'GET TICKETS', '']:
                    continue

                # Check if this link contains date info
                date_match = re.search(r'(TODAY|TOMORROW|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)\s+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})', text, re.IGNORECASE)

                if date_match:
                    # This is a date header, save it for context
                    current_date = text
                    continue

                # This should be an event title
                title = text

                # Look for time in nearby elements
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
                        # Parse date like "FRIDAY MAR 20"
                        date_match = re.search(r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+(\d{1,2})', current_date, re.IGNORECASE)
                        if date_match:
                            month_day = date_match.group(0)
                            current_year = datetime.now().year
                            date_obj = datetime.strptime(f"{month_day} {current_year}", "%b %d %Y")

                            # If date is in past, assume next year
                            if date_obj < datetime.now():
                                date_obj = date_obj.replace(year=current_year + 1)

                            iso_date = date_obj.isoformat() + 'Z'
                    except Exception as e:
                        print(f"⚠️  Error parsing date '{current_date}': {e}")

                if not iso_date:
                    # Use current date as fallback
                    iso_date = datetime.now().isoformat() + 'Z'

                seen_urls.add(href)

                shows.append({
                    'title': title,
                    'venue': 'Gotham Comedy Club',
                    'date': iso_date,
                    'time': time_str,
                    'description': None,
                    'url': href
                })

            except Exception as e:
                print(f"⚠️  Error parsing event: {e}")
                continue

        # Output
        output = {
            'shows': shows,
            'lastUpdated': datetime.now().isoformat() + 'Z',
            'venue': 'Gotham Comedy Club',
            'totalShows': len(shows)
        }

        with open('gotham-shows.json', 'w') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Scraping complete!")
        print(f"📝 Results saved to gotham-shows.json")
        print(f"📋 Total shows: {len(shows)}")
        print(f"📅 Last updated: {output['lastUpdated']}")
        print(f"\n🎤 Sample shows:")
        for show in shows[:5]:
            print(f"  • {show['title']}")
            print(f"    {show['date'][:10]} at {show.get('time', 'N/A')}")

        return shows

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    scrape_gotham()
