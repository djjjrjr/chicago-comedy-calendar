#!/usr/bin/env python3
"""
Chicago Comedy Calendar Scraper
Fetches show schedules from Do312.com for all Chicago comedy venues
"""

import json
import sys
from datetime import datetime
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Venue configurations with Do312 slugs
VENUES = {
    'second-city': {
        'name': 'Second City',
        'do312_slug': 'the-second-city'
    },
    'io-theater': {
        'name': 'iO Theater',
        'do312_slug': 'io-theater'
    },
    'annoyance': {
        'name': 'Annoyance Theatre',
        'do312_slug': 'annoyance-theatre'
    },
    'zanies': {
        'name': 'Zanies',
        'do312_slug': 'zanies'
    },
    'laugh-factory': {
        'name': 'Laugh Factory',
        'do312_slug': 'laugh-factory'
    },
    'lincoln-lodge': {
        'name': 'Lincoln Lodge',
        'do312_slug': 'the-lincoln-lodge'
    },
    'den-theatre': {
        'name': 'Den Theatre',
        'do312_slug': 'the-den-theatre'
    }
}


def scrape_do312_venue(page, venue_id: str, venue_config: Dict) -> List[Dict]:
    """
    Scrape a single venue's events from Do312

    Args:
        page: Playwright page object
        venue_id: Internal venue ID (e.g., 'second-city')
        venue_config: Venue configuration dictionary

    Returns:
        List of show dictionaries
    """
    shows = []
    slug = venue_config['do312_slug']
    url = f'https://do312.com/venues/{slug}'

    print(f"  Fetching {venue_config['name']} from {url}")

    try:
        # Navigate to venue page
        page.goto(url, wait_until='networkidle', timeout=30000)

        # Wait for events to load
        try:
            page.wait_for_selector('.event-item, [class*="event"]', timeout=5000)
        except PlaywrightTimeout:
            print(f"  No events found for {venue_config['name']}")
            return shows

        # Extract event data using JavaScript
        events_data = page.evaluate('''
            () => {
                const events = [];
                // Look for event containers - adjust selectors as needed
                const eventElements = document.querySelectorAll('.event-item, [class*="event-"]');

                eventElements.forEach(el => {
                    try {
                        // Extract title
                        const titleEl = el.querySelector('h3, h4, .event-title, [class*="title"]');
                        const title = titleEl ? titleEl.textContent.trim() : '';

                        if (!title) return; // Skip if no title

                        // Extract date/time
                        const dateEl = el.querySelector('time, .date, [class*="date"]');
                        let dateStr = '';
                        if (dateEl) {
                            dateStr = dateEl.getAttribute('datetime') || dateEl.textContent.trim();
                        }

                        // Extract time
                        const timeEl = el.querySelector('.time, [class*="time"]');
                        const time = timeEl ? timeEl.textContent.trim() : '';

                        // Extract link
                        const linkEl = el.querySelector('a');
                        const url = linkEl ? linkEl.href : '';

                        // Extract description if available
                        const descEl = el.querySelector('.description, [class*="desc"]');
                        const description = descEl ? descEl.textContent.trim().substring(0, 200) : '';

                        events.push({
                            title,
                            dateStr,
                            time,
                            url,
                            description
                        });
                    } catch (err) {
                        console.error('Error extracting event:', err);
                    }
                });

                return events;
            }
        ''')

        # Process and format the events
        for event in events_data:
            if not event.get('title'):
                continue

            # Parse date - Do312 typically uses dates like "Today Mar 6" or actual dates
            date_str = event.get('dateStr', '')
            time_str = event.get('time', '')

            # For now, use a placeholder date if we can't parse it
            # In production, you'd want proper date parsing
            date_iso = datetime.now().isoformat()

            show = {
                'venue': venue_id,
                'title': event['title'],
                'date': date_iso,
                'time': time_str,
                'description': event.get('description', ''),
                'url': event.get('url', '')
            }

            shows.append(show)

        print(f"  Found {len(shows)} shows for {venue_config['name']}")

    except Exception as e:
        print(f"  Error scraping {venue_config['name']}: {e}")

    return shows


def scrape_all_venues() -> List[Dict]:
    """
    Scrape all venues using Playwright

    Returns:
        List of all shows from all venues
    """
    all_shows = []

    print("Starting Chicago Comedy Calendar scraper...")
    print("Using Do312.com as data source\n")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Scrape each venue
        for venue_id, venue_config in VENUES.items():
            print(f"Scraping {venue_config['name']}...")
            try:
                shows = scrape_do312_venue(page, venue_id, venue_config)
                all_shows.extend(shows)
            except Exception as e:
                print(f"  Failed to scrape {venue_config['name']}: {e}")
                continue

            print()

        browser.close()

    return all_shows


def save_shows(shows: List[Dict]):
    """Save shows to JSON file"""
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'shows': shows
    }

    with open('shows.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Saved {len(shows)} shows to shows.json")


def main():
    try:
        shows = scrape_all_venues()

        if not shows:
            print("\n⚠️  Warning: No shows were scraped. Check if Do312.com structure has changed.")
            sys.exit(1)

        save_shows(shows)
        print("\n✓ Scraping complete!")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Scraping failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
