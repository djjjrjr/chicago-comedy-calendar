#!/usr/bin/env python3
"""
UCB Theatre LA Scraper - Bypasses Cloudflare with cloudscraper
"""

import cloudscraper
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

def scrape_ucb_la():
    print("🎭 Starting UCB Theatre LA scraper...")

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'desktop': True
        }
    )

    url = 'https://ucbcomedy.com/shows/los-angeles/'
    print(f"📡 Fetching {url}")

    try:
        # Retry up to 3 times (server sometimes returns 520 error)
        import time
        response = None
        for attempt in range(3):
            try:
                response = scraper.get(url, timeout=30)
                if response.status_code == 200:
                    break
                elif response.status_code == 520:
                    print(f"⚠️  Server error 520, retrying ({attempt+1}/3)...")
                    time.sleep(5)
            except Exception as e:
                if attempt < 2:
                    print(f"⚠️  Request failed, retrying ({attempt+1}/3)...")
                    time.sleep(5)
                else:
                    raise

        if response.status_code != 200:
            print(f"❌ Error: Status {response.status_code}")
            return []

        if "Just a moment" in response.text or "Performing security" in response.text:
            print("❌ Cloudflare blocked the request")
            return []

        print(f"✅ Got {len(response.text)} characters")
        print("🔍 Parsing HTML...")

        soup = BeautifulSoup(response.text, 'html.parser')

        shows = []

        # Find all show cards/events
        event_cards = soup.find_all(['div', 'article'], class_=re.compile(r'event|show|card', re.I))

        print(f"📦 Found {len(event_cards)} potential event elements")

        for card in event_cards:
            try:
                # Extract title
                title_el = card.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name|event', re.I))
                if not title_el:
                    title_el = card.find(['h1', 'h2', 'h3', 'h4'])

                title = title_el.get_text(strip=True) if title_el else None

                # Extract date/time
                date_el = card.find(['time', 'span', 'div'], class_=re.compile(r'date|time|when', re.I))
                date_str = date_el.get_text(strip=True) if date_el else None
                datetime_attr = date_el.get('datetime') if date_el and hasattr(date_el, 'get') else None

                # Extract URL
                link = card.find('a')
                url_str = link.get('href') if link else None
                if url_str and url_str.startswith('/'):
                    url_str = f'https://ucbcomedy.com{url_str}'

                # Extract description
                desc_el = card.find(['p', 'div'], class_=re.compile(r'desc|excerpt|content', re.I))
                description = desc_el.get_text(strip=True) if desc_el else None

                if title and (date_str or datetime_attr):
                    # Try to parse datetime
                    iso_date = None
                    time = None

                    if datetime_attr:
                        iso_date = datetime_attr
                    elif date_str:
                        # Try to extract date and time from string
                        date_match = re.search(r'(\w+)\s+(\d+),?\s+(\d{4})', date_str)
                        if date_match:
                            try:
                                dt = datetime.strptime(f"{date_match.group(1)} {date_match.group(2)}, {date_match.group(3)}", "%B %d, %Y")
                                iso_date = dt.isoformat() + 'Z'
                            except:
                                pass

                        # Look for time like "7:30 PM" or "7:30pm"
                        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)', date_str, re.I)
                        if time_match:
                            time = time_match.group(0)

                    if not iso_date:
                        iso_date = datetime.now().isoformat() + 'Z'

                    shows.append({
                        'title': title,
                        'venue': 'UCB FRANKLIN',
                        'date': iso_date,
                        'time': time,
                        'description': description,
                        'url': url_str or 'https://ucbcomedy.com/shows/los-angeles/'
                    })

            except Exception as e:
                print(f"⚠️  Error parsing card: {e}")
                continue

        # Deduplicate by URL
        seen_urls = set()
        unique_shows = []
        for show in shows:
            url_key = show.get('url', '')
            if url_key and url_key not in seen_urls:
                seen_urls.add(url_key)
                unique_shows.append(show)
            elif not url_key:
                unique_shows.append(show)

        shows = unique_shows
        print(f"✅ Extracted {len(shows)} shows (after deduplication)")

        # If no shows found, try alternative parsing method
        if len(shows) == 0:
            print("🔄 Trying alternative parsing method...")

            all_links = soup.find_all('a', href=re.compile(r'/shows?/', re.I))
            print(f"   Found {len(all_links)} show links")

            seen_urls = set()
            for link in all_links[:50]:
                href = link.get('href', '')
                text = link.get_text(strip=True)

                if text and len(text) > 3 and not text.lower() in ['shows', 'events', 'calendar', 'tickets']:
                    if href not in seen_urls:
                        seen_urls.add(href)
                        shows.append({
                            'title': text,
                            'venue': 'UCB FRANKLIN',
                            'date': datetime.now().isoformat() + 'Z',
                            'time': None,
                            'description': None,
                            'url': f'https://ucbcomedy.com{href}' if href.startswith('/') else href
                        })

            print(f"✅ Extracted {len(shows)} shows via alternative method")

        return shows

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    shows = scrape_ucb_la()

    output = {
        'shows': shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'venue': 'UCB FRANKLIN',
        'totalShows': len(shows)
    }

    with open('ucb-la-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(shows)} UCB LA shows to ucb-la-shows.json")

    if len(shows) > 0:
        print("\n📋 Sample shows:")
        for show in shows[:5]:
            print(f"  • {show['title']}")
            print(f"    {show['venue']}, {show.get('date', 'N/A')[:10]}")
