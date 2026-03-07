#!/usr/bin/env python3
"""
Chicago Comedy Calendar Scraper
Fetches show schedules from Do312.com for all Chicago comedy venues
"""

import json
import sys
import time
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
        # Navigate to venue page with extended timeout
        print(f"  Navigating to {url}")
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        print(f"  Initial page load complete")

        # Wait for network to be idle (page fully loaded)
        print(f"  Waiting for network idle...")
        page.wait_for_load_state('networkidle', timeout=30000)
        print(f"  Network idle - page fully loaded")

        # Extra buffer for JavaScript execution
        time.sleep(2)
        print(f"  Buffer wait complete")

        # Wait for events to load - Do312 uses .ds-listing.event-card
        print(f"  Waiting for event cards selector '.ds-listing.event-card'...")
        try:
            page.wait_for_selector('.ds-listing.event-card', timeout=15000)
            card_count = len(page.query_selector_all('.ds-listing.event-card'))
            print(f"  ✓ Found {card_count} event cards on page")
        except PlaywrightTimeout:
            print(f"  ⚠️  Timeout waiting for event cards after 15 seconds")
            print(f"  Debugging page state...")
            page_content = page.content()
            print(f"  - Page length: {len(page_content)} chars")
            print(f"  - Contains 'event-card': {'event-card' in page_content}")
            print(f"  - Page title: {page.title()}")

            # Take screenshot for debugging
            screenshot_path = f"debug_{venue_id}.png"
            page.screenshot(path=screenshot_path)
            print(f"  - Screenshot saved to {screenshot_path}")
            return shows

        # Extract event data using JavaScript with Do312-specific selectors
        events_data = page.evaluate('''
            () => {
                const events = [];
                // Do312 uses .ds-listing.event-card for event containers
                const eventElements = document.querySelectorAll('.ds-listing.event-card');

                console.log(`Found ${eventElements.length} event cards`);

                eventElements.forEach((el, index) => {
                    try {
                        // Do312 structure: .ds-listing-event-title-text for title
                        const titleEl = el.querySelector('.ds-listing-event-title-text');
                        const title = titleEl ? titleEl.textContent.trim() : '';

                        if (!title) {
                            console.log(`Event ${index}: No title found, skipping`);
                            return;
                        }

                        // Extract date from URL path (e.g., /events/2026/3/7/...)
                        const linkEl = el.querySelector('a[href*="/events/"]');
                        let dateStr = '';
                        if (linkEl) {
                            const match = linkEl.href.match(/\/events\/(\d{4})\/(\d{1,2})\/(\d{1,2})\//);
                            if (match) {
                                dateStr = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
                            }
                        }

                        // Extract time from .ds-event-time
                        const timeEl = el.querySelector('.ds-event-time');
                        const time = timeEl ? timeEl.textContent.trim() : '';

                        // Extract link from main <a> tag or data-permalink
                        let url = '';
                        const linkEl = el.querySelector('a[href*="/events/"]');
                        if (linkEl) {
                            url = linkEl.href;
                        } else if (el.hasAttribute('data-permalink')) {
                            url = 'https://do312.com' + el.getAttribute('data-permalink');
                        }

                        // Log what we found
                        console.log(`Event ${index}: "${title}" at ${time} on day ${dateStr}`);

                        events.push({
                            title,
                            dateStr,
                            time,
                            url,
                            description: ''
                        });
                    } catch (err) {
                        console.error(`Error extracting event ${index}:`, err);
                    }
                });

                return events;
            }
        ''')

        # Process and format the events
        print(f"  Processing {len(events_data)} events from page...")
        for i, event in enumerate(events_data):
            if not event.get('title'):
                print(f"    Event {i}: Skipped (no title)")
                continue

            # Parse date from URL format (YYYY-MM-DD)
            date_str = event.get('dateStr', '')
            time_str = event.get('time', '')

            # Convert to ISO format with time
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    date_iso = date_obj.isoformat() + 'Z'
                except ValueError:
                    date_iso = datetime.now().isoformat() + 'Z'
            else:
                date_iso = datetime.now().isoformat() + 'Z'

            show = {
                'venue': venue_id,
                'title': event['title'],
                'date': date_iso,
                'time': time_str,
                'description': event.get('description', ''),
                'url': event.get('url', '')
            }

            shows.append(show)
            print(f"    ✓ Added: {event['title']}")

        print(f"  ✓ Found {len(shows)} shows for {venue_config['name']}")

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
        # Launch browser with extra args for stability
        print("Launching Chromium browser...")
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        page = browser.new_page()
        print("✓ Browser launched successfully\n")

        # Scrape each venue with retry logic
        for venue_id, venue_config in VENUES.items():
            print(f"{'='*60}")
            print(f"Scraping {venue_config['name']}...")
            print(f"{'='*60}")

            max_retries = 2
            shows = []

            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        print(f"  Retry attempt {attempt + 1}/{max_retries}")
                        time.sleep(3)  # Wait before retry

                    shows = scrape_do312_venue(page, venue_id, venue_config)

                    if shows:
                        print(f"  ✓ Successfully scraped {len(shows)} shows")
                        break
                    elif attempt < max_retries - 1:
                        print(f"  No shows found, retrying...")
                    else:
                        print(f"  ⚠️  No shows found after {max_retries} attempts")

                except Exception as e:
                    print(f"  ✗ Error on attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        print(f"  Retrying in 3 seconds...")
                    else:
                        print(f"  ✗ Failed after {max_retries} attempts")
                        import traceback
                        traceback.print_exc()

            all_shows.extend(shows)
            print()

        print("Closing browser...")
        browser.close()
        print("✓ Browser closed\n")

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
    start_time = time.time()
    print(f"{'='*60}")
    print(f"Chicago Comedy Calendar Scraper")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        shows = scrape_all_venues()

        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total shows scraped: {len(shows)}")
        print(f"Time elapsed: {elapsed:.1f} seconds")

        if shows:
            # Group by venue for summary
            venues = {}
            for show in shows:
                venue = show['venue']
                venues[venue] = venues.get(venue, 0) + 1

            print("\nShows per venue:")
            for venue, count in venues.items():
                print(f"  - {venue}: {count}")

        if not shows:
            print("\n⚠️  Warning: No shows were scraped. Check if Do312.com structure has changed.")
            print("Exiting with code 1 to indicate failure.")
            sys.exit(1)

        save_shows(shows)
        print("\n✓ Scraping complete!")
        sys.exit(0)

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"SCRAPING FAILED")
        print(f"{'='*60}")
        print(f"Error: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
