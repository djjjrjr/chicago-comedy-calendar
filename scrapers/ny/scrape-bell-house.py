#!/usr/bin/env python3
"""
Bell House scraper - Scrapes from DoNYC venue page
"""

import cloudscraper
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_bell_house():
    print("🎭 Starting Bell House scraper...")

    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'darwin', 'desktop': True}
    )

    url = 'https://donyc.com/venues/the-bell-house'
    print(f"📡 Fetching {url}")

    try:
        response = scraper.get(url, timeout=30)

        if response.status_code != 200:
            print(f"❌ Error: Status {response.status_code}")
            return []

        print(f"✅ Got {len(response.text)} characters")
        soup = BeautifulSoup(response.text, 'html.parser')

        shows = []
        seen_urls = set()
        event_links = soup.find_all('a', href=re.compile(r'/events/'))

        print(f"📦 Found {len(event_links)} potential event links")

        current_date = None

        for link in event_links:
            try:
                href = link.get('href')
                if not href or '/venues/' in href:
                    continue

                if href.startswith('/'):
                    href = f"https://donyc.com{href}"

                if href in seen_urls:
                    continue

                text = link.get_text(strip=True)

                if text.upper() == 'THE BELL HOUSE' or text in ['BUY', 'GET TICKETS', '']:
                    continue

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
                        print(f"⚠️  Error parsing date '{current_date}': {e}")

                if not iso_date:
                    iso_date = datetime.now().isoformat() + 'Z'

                seen_urls.add(href)

                shows.append({
                    'title': title,
                    'venue': 'The Bell House',
                    'date': iso_date,
                    'time': time_str,
                    'description': None,
                    'url': href
                })

            except Exception as e:
                print(f"⚠️  Error parsing event: {e}")
                continue

        output = {
            'shows': shows,
            'lastUpdated': datetime.now().isoformat() + 'Z',
            'venue': 'The Bell House',
            'totalShows': len(shows)
        }

        with open('bell-house-shows.json', 'w') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Scraping complete!")
        print(f"📝 Results saved to bell-house-shows.json")
        print(f"📋 Total shows: {len(shows)}")

        return shows

    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    scrape_bell_house()
