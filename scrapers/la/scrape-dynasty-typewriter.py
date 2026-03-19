#!/usr/bin/env python3
"""
Scrape Dynasty Typewriter events from their Squarespace calendar
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def parse_date(date_str, year=2026):
    """Convert date strings like 'THU, MAR 19' to ISO format"""
    try:
        # Remove day of week prefix
        date_str = re.sub(r'^[A-Z]{3},\s*', '', date_str.strip())

        # Try full month name first, then abbreviated
        for fmt in ["%B %d", "%b %d", "%B %d", "%b %d"]:
            try:
                date_obj = datetime.strptime(f"{date_str}, {year}", f"{fmt}, %Y")
                return date_obj.isoformat() + "Z"
            except ValueError:
                continue

        # Fallback
        return datetime.now().isoformat() + "Z"
    except Exception as e:
        print(f"  ⚠️ Error parsing date '{date_str}': {e}")
        return datetime.now().isoformat() + "Z"

def parse_time(time_str):
    """Normalize time format"""
    try:
        time_str = time_str.strip()
        # Handle formats like "7:00 PM" or "11:59 PM"
        match = re.search(r'(\d+):(\d+)\s*([AP]M)', time_str, re.IGNORECASE)
        if match:
            hour, minute, meridiem = match.groups()
            return f"{hour}:{minute} {meridiem.upper()}"
        return time_str
    except:
        return time_str

def scrape_dynasty_typewriter():
    """Scrape Dynasty Typewriter Squarespace calendar"""
    print("🎭 Starting Dynasty Typewriter scraper...")

    url = "https://www.dynastytypewriter.com/calendar-squad-up"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        print(f"📡 Fetching {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        print(f"✅ Got {len(response.text)} characters")

        soup = BeautifulSoup(response.text, 'html.parser')
        shows = []

        # Look for event items in Squarespace calendar
        # Events are typically in <article> or <div> with class containing "event"
        event_items = soup.find_all(['article', 'div', 'li'], class_=re.compile(r'event|calendar-event|eventlist-event', re.I))

        print(f"📦 Found {len(event_items)} potential event elements")

        for item in event_items:
            try:
                # Extract title
                title_el = item.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name', re.I))
                if not title_el:
                    title_el = item.find(['h1', 'h2', 'h3', 'h4'])

                if not title_el:
                    continue

                title = title_el.get_text(strip=True)

                # Extract date
                date_el = item.find(['time', 'span', 'div'], class_=re.compile(r'date', re.I))
                date_str = date_el.get_text(strip=True) if date_el else ''

                # Extract time
                time_el = item.find(['time', 'span', 'div'], class_=re.compile(r'time', re.I))
                time_str = ''
                if time_el:
                    time_str = time_el.get_text(strip=True)
                elif date_str:
                    # Sometimes time is in the date element
                    time_match = re.search(r'(\d+:\d+\s*[AP]M)', date_str, re.I)
                    if time_match:
                        time_str = time_match.group(1)

                # Extract URL
                link = item.find('a', href=True)
                url_str = link['href'] if link else ''
                if url_str and not url_str.startswith('http'):
                    url_str = 'https://www.dynastytypewriter.com' + url_str

                # Extract description/excerpt
                desc_el = item.find(['p', 'div'], class_=re.compile(r'excerpt|description|summary', re.I))
                description = desc_el.get_text(strip=True) if desc_el else ''

                # Only add if we have title and some date info
                if title and date_str:
                    iso_date = parse_date(date_str)
                    formatted_time = parse_time(time_str) if time_str else ''

                    shows.append({
                        'title': title,
                        'venue': 'Dynasty Typewriter',
                        'date': iso_date,
                        'time': formatted_time,
                        'description': description[:300] if description else '',
                        'url': url_str if url_str else url
                    })

            except Exception as e:
                print(f"  ⚠️  Error parsing event: {e}")
                continue

        # Deduplicate by title + date
        unique_shows = []
        seen = set()

        for show in shows:
            key = (show['title'], show['date'][:10])
            if key not in seen:
                seen.add(key)
                unique_shows.append(show)

        print(f"✅ Extracted {len(unique_shows)} unique shows")
        return unique_shows

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    shows = scrape_dynasty_typewriter()

    output = {
        'shows': shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'venue': 'Dynasty Typewriter',
        'totalShows': len(shows)
    }

    # Save to JSON
    output_file = 'dynasty-typewriter-shows.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"📝 Saved {len(shows)} shows to {output_file}")

    # Print sample
    if shows:
        print("\n📋 Sample shows:")
        for show in shows[:5]:
            print(f"  • {show['title']}")
            print(f"    {show['venue']}, {show.get('time', 'TBA')}")

if __name__ == '__main__':
    main()
