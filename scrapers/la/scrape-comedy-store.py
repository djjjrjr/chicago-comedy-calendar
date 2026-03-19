#!/usr/bin/env python3
"""
Scrape The Comedy Store (LA) events from their weekly calendar
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def parse_date(date_str, year=2026):
    """Convert 'March 18' or 'Mar 18' to ISO date"""
    try:
        # Clean up the date string
        date_str = date_str.strip()
        # Try full month name first, then abbreviated
        try:
            date_obj = datetime.strptime(f"{date_str}, {year}", "%B %d, %Y")
        except ValueError:
            date_obj = datetime.strptime(f"{date_str}, {year}", "%b %d, %Y")
        return date_obj.isoformat() + "Z"
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return datetime.now().isoformat() + "Z"

def parse_time(time_str):
    """Normalize time format"""
    try:
        time_str = time_str.strip()
        # Handle formats like "8:00 PM" or "11:59 PM"
        match = re.search(r'(\d+):(\d+)\s*([AP]M)', time_str, re.IGNORECASE)
        if match:
            hour, minute, meridiem = match.groups()
            return f"{hour}:{minute} {meridiem.upper()}"
        return time_str
    except:
        return time_str

def scrape_week(url, headers):
    """Scrape shows from a single week"""
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"  ❌ Error fetching {url}: {e}")
        return [], None

    soup = BeautifulSoup(response.content, 'html.parser')
    shows = []

    # Find all show containers
    # Looking for patterns in the HTML structure
    show_containers = soup.find_all('div', class_='row')

    for container in show_containers:
        try:
            # Look for show title
            title_elem = container.find('h2', class_='show-title')
            if not title_elem:
                continue

            title_link = title_elem.find('a')
            if not title_link:
                continue

            title = title_link.get_text(strip=True)
            show_url = title_link.get('href', '')
            if show_url and not show_url.startswith('http'):
                show_url = 'https://thecomedystore.com' + show_url

            # Look for date and time
            date_str = ''
            time_str = ''

            # Search for date/time spans
            spans = container.find_all('span')
            for span in spans:
                text = span.get_text(strip=True)
                # Date pattern: "March 18" or "Mar 18"
                if re.match(r'^[A-Z][a-z]{2,8}\s+\d+$', text):
                    date_str = text
                # Time pattern: "8:00 PM"
                elif re.search(r'\d+:\d+\s*[AP]M', text, re.IGNORECASE):
                    time_str = text

            # Look for room/venue
            room = ''
            room_elem = container.find('h3')
            if room_elem:
                room_text = room_elem.get_text(strip=True)
                if 'Main Room' in room_text:
                    room = 'Main Room'
                elif 'Original Room' in room_text:
                    room = 'Original Room'
                elif 'Belly Room' in room_text:
                    room = 'Belly Room'

            # Build venue name
            venue = 'The Comedy Store'
            if room:
                venue = f'The Comedy Store - {room}'

            # Get lineup
            description = 'Comedy showcase'
            lineup_links = container.find_all('a', href=re.compile(r'/comedians/'))
            if lineup_links:
                comedians = [link.get_text(strip=True) for link in lineup_links if link.get_text(strip=True)]
                if comedians:
                    description = 'Lineup: ' + ', '.join(comedians[:10])  # Limit to first 10

            # Check if sold out
            if 'SOLD OUT' in container.get_text().upper() or 'Sold Out' in container.get_text():
                description = 'SOLD OUT - ' + description

            # Parse date and time
            iso_date = parse_date(date_str) if date_str else datetime.now().isoformat() + "Z"
            formatted_time = parse_time(time_str) if time_str else ''

            # Only add if we have essential information
            if title and date_str:
                shows.append({
                    'title': title,
                    'venue': venue,
                    'date': iso_date,
                    'time': formatted_time,
                    'description': description,
                    'url': show_url if show_url else 'https://thecomedystore.com/calendar/'
                })

        except Exception as e:
            print(f"  ⚠️  Error parsing show: {e}")
            continue

    # Look for next week link
    next_link = None
    next_btn = soup.find('a', href=re.compile(r'/calendar/by-week/\d{4}-\d{2}-\d{2}'))
    if next_btn and 'Next Week' in next_btn.get_text():
        next_href = next_btn.get('href')
        if next_href:
            next_link = 'https://thecomedystore.com' + next_href if next_href.startswith('/') else next_href

    return shows, next_link

def scrape_comedy_store():
    """Scrape The Comedy Store weekly calendar (multiple weeks)"""
    print("🎭 Starting The Comedy Store scraper...")

    base_url = "https://thecomedystore.com/calendar/by-week/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    all_shows = []
    url = base_url
    weeks_scraped = 0
    max_weeks = 4  # Scrape up to 4 weeks

    print("📊 Scraping weekly calendars...")

    while url and weeks_scraped < max_weeks:
        weeks_scraped += 1
        print(f"  📅 Week {weeks_scraped}: {url}")

        week_shows, next_url = scrape_week(url, headers)
        all_shows.extend(week_shows)

        print(f"     Found {len(week_shows)} shows")

        url = next_url

    # Deduplicate shows
    unique_shows = []
    seen = set()

    for show in all_shows:
        key = (show['venue'], show['date'][:10], show['time'], show['title'])
        if key not in seen:
            seen.add(key)
            unique_shows.append(show)

    print(f"✅ Found {len(unique_shows)} unique shows across {weeks_scraped} weeks")

    return unique_shows

def main():
    shows = scrape_comedy_store()

    output = {
        'shows': shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'venue': 'The Comedy Store',
        'totalShows': len(shows)
    }

    # Save to JSON
    output_file = 'comedy-store-shows.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"📝 Saved {len(shows)} shows to {output_file}")

    # Print summary
    if shows:
        print("\n📊 Shows by room:")
        from collections import Counter
        rooms = Counter()
        for show in shows:
            venue = show['venue']
            if ' - ' in venue:
                room = venue.split(' - ')[1]
                rooms[room] += 1
            else:
                rooms['Unspecified'] += 1

        for room, count in rooms.most_common():
            print(f"  • {room}: {count}")

        print("\n📋 Sample shows:")
        for show in shows[:5]:
            print(f"  • {show['title']}")
            print(f"    {show['venue']}, {show.get('time', 'TBA')}")

if __name__ == '__main__':
    main()
