#!/usr/bin/env python3
"""
Los Angeles Comedy Calendar Scraper
Fetches ALL comedy show schedules from DoLosAngeles.com
"""

import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Set, Tuple
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def scrape_dolosangeles_comedy_events(page) -> List[Dict]:
    """
    Scrape all comedy events from DoLosAngeles's comedy category page

    Args:
        page: Playwright page object

    Returns:
        List of show dictionaries with venue information from DoLosAngeles
    """
    all_events = []
    seen_events: Set[Tuple[str, str, str]] = set()  # For deduplication (title, date, venue)
    page_num = 1

    base_url = 'https://dolosangeles.com/events/comedy'

    print(f"Fetching comedy events from DoLosAngeles...")
    print(f"Starting URL: {base_url}\n")

    while True:
        # Construct URL for current page
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page_num}"

        print(f"{'='*60}")
        print(f"Page {page_num}: {url}")
        print(f"{'='*60}")

        try:
            # Navigate to page
            print(f"  Navigating to page...")
            page.goto(url, wait_until='domcontentloaded', timeout=60000)

            # Wait for network idle
            print(f"  Waiting for network idle...")
            page.wait_for_load_state('networkidle', timeout=60000)

            # Extra buffer for JavaScript
            time.sleep(2)

            # Check if we have event cards
            print(f"  Checking for event cards...")
            try:
                page.wait_for_selector('.ds-listing.event-card', timeout=10000)
            except PlaywrightTimeout:
                print(f"  No event cards found on page {page_num}")
                print(f"  Reached end of event listings")
                break

            # Extract events from current page
            events_data = page.evaluate('''
                () => {
                    const events = [];
                    const eventElements = document.querySelectorAll('.ds-listing.event-card');

                    console.log(`Found ${eventElements.length} event cards on page`);

                    eventElements.forEach((el, index) => {
                        try {
                            // Extract title
                            const titleEl = el.querySelector('.ds-listing-event-title-text');
                            const title = titleEl ? titleEl.textContent.trim() : '';

                            if (!title) {
                                return;
                            }

                            // Extract venue name from the venue link
                            const venueEl = el.querySelector('a[href*="/venues/"]');
                            const venue = venueEl ? venueEl.textContent.trim() : 'Unknown Venue';

                            // Extract link for date and URL
                            const linkEl = el.querySelector('a[href*="/events/"]');

                            // Extract date from URL path (e.g., /events/2026/3/15/...)
                            let dateStr = '';
                            if (linkEl) {
                                const match = linkEl.href.match(/\/events\/(\d{4})\/(\d{1,2})\/(\d{1,2})\//);
                                if (match) {
                                    dateStr = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
                                }
                            }

                            // Extract time
                            const timeEl = el.querySelector('.ds-event-time');
                            const time = timeEl ? timeEl.textContent.trim() : '';

                            // Extract URL
                            let url = '';
                            if (linkEl) {
                                url = linkEl.href;
                            } else if (el.hasAttribute('data-permalink')) {
                                url = 'https://dolosangeles.com' + el.getAttribute('data-permalink');
                            }

                            events.push({
                                title,
                                venue,
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

            # Process events from this page
            print(f"  Found {len(events_data)} events on page {page_num}")
            new_events_count = 0

            for event in events_data:
                if not event.get('title') or not event.get('venue'):
                    continue

                # Create deduplication key
                dedup_key = (
                    event['title'].lower().strip(),
                    event.get('dateStr', ''),
                    event['venue'].lower().strip()
                )

                # Skip if we've seen this exact event
                if dedup_key in seen_events:
                    continue

                seen_events.add(dedup_key)

                # Parse date
                date_str = event.get('dateStr', '')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        date_iso = date_obj.isoformat() + 'Z'
                    except ValueError:
                        date_iso = datetime.now().isoformat() + 'Z'
                else:
                    date_iso = datetime.now().isoformat() + 'Z'

                show = {
                    'venue': event['venue'],  # Venue name from DoLosAngeles
                    'title': event['title'],
                    'date': date_iso,
                    'time': event.get('time', ''),
                    'description': event.get('description', ''),
                    'url': event.get('url', '')
                }

                all_events.append(show)
                new_events_count += 1

            print(f"  Added {new_events_count} new events (after deduplication)")
            print(f"  Total events so far: {len(all_events)}\n")

            # Check if there's a next page
            has_next = page.evaluate('''
                () => {
                    // Try aria-label selectors first
                    let nextButton = document.querySelector('button[aria-label*="next" i], a[aria-label*="next" i]');

                    // If not found, search for buttons/links with "Next" text
                    if (!nextButton) {
                        const buttons = Array.from(document.querySelectorAll('button, a'));
                        nextButton = buttons.find(btn =>
                            btn.textContent.trim().toLowerCase().includes('next') ||
                            btn.getAttribute('aria-label')?.toLowerCase().includes('next')
                        );
                    }

                    return nextButton !== null && !nextButton.disabled && !nextButton.classList.contains('disabled');
                }
            ''')

            if not has_next:
                print(f"  No 'Next' button found - reached end of pagination")
                break

            # Move to next page
            page_num += 1

            # Add delay to avoid rate limiting
            time.sleep(2)

        except Exception as e:
            print(f"  Error on page {page_num}: {e}")
            print(f"  Stopping pagination")
            break

    return all_events


def scrape_all_events() -> List[Dict]:
    """
    Scrape all comedy events using Playwright

    Returns:
        List of all comedy shows from DoLosAngeles
    """
    all_shows = []

    print("Starting Los Angeles Comedy Calendar scraper...")
    print("Scraping ALL comedy events from DoLosAngeles.com\n")

    with sync_playwright() as p:
        # Launch browser
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

        # Create page
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )

        page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        })

        print("✓ Browser launched successfully\n")

        try:
            all_shows = scrape_dolosangeles_comedy_events(page)
            print(f"\n✓ Successfully scraped {len(all_shows)} total comedy events")
        except Exception as e:
            print(f"\n✗ Error during scraping: {e}")
            import traceback
            traceback.print_exc()

        print("\nClosing browser...")
        browser.close()
        print("✓ Browser closed\n")

    return all_shows


def save_shows(shows: List[Dict]):
    """Save shows to JSON file"""
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'shows': shows
    }

    with open('la-shows.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Saved {len(shows)} shows to la-shows.json")


def main():
    start_time = time.time()
    print(f"{'='*60}")
    print(f"Los Angeles Comedy Calendar Scraper")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        shows = scrape_all_events()

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

            print(f"\nShows per venue ({len(venues)} total venues):")
            # Show top 10 venues
            sorted_venues = sorted(venues.items(), key=lambda x: x[1], reverse=True)
            for venue, count in sorted_venues[:10]:
                print(f"  - {venue}: {count}")
            if len(sorted_venues) > 10:
                print(f"  ... and {len(sorted_venues) - 10} more venues")

        if not shows:
            print("\n⚠️  Warning: No shows were scraped. Check if DoLosAngeles.com structure has changed.")
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
