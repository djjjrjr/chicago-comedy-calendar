#!/usr/bin/env python3
"""
Chicago Comedy Calendar Scraper - DATE-BASED VERSION

CRITICAL FIX: Do312.com's pagination is broken. Pages 4+ just repeat page 3.
The site organizes events by date-specific URLs:
  - /events/comedy/2026/03/19
  - /events/comedy/2026/03/20
  - etc.

This scraper iterates through dates instead of relying on broken pagination.
"""

import json
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def load_existing_shows() -> List[Dict]:
    """Load existing shows from shows.json"""
    try:
        with open('shows.json', 'r') as f:
            data = json.load(f)
            return data.get('shows', [])
    except FileNotFoundError:
        return []


def scrape_date_page(page, date_str: str, seen_events: Set[Tuple[str, str, str]]) -> List[Dict]:
    """
    Scrape all events for a specific date.

    Args:
        page: Playwright page object
        date_str: Date in YYYY/MM/DD format (e.g., "2026/03/19")
        seen_events: Set of already seen event keys for deduplication

    Returns:
        List of events for this date
    """
    events_for_date = []
    page_num = 1
    MAX_PAGES_PER_DATE = 5  # Each date shouldn't have more than ~5 pages

    # Convert date_str to display format
    try:
        date_obj = datetime.strptime(date_str, '%Y/%m/%d')
        display_date = date_obj.strftime('%m/%d')
    except:
        display_date = date_str

    while page_num <= MAX_PAGES_PER_DATE:
        # Construct URL for this date and page
        if page_num == 1:
            url = f'https://do312.com/events/comedy/{date_str}'
        else:
            # Do312 uses hash anchors for pagination within a date
            url = f'https://do312.com/events/comedy/{date_str}#{page_num}'

        try:
            # Navigate to page
            page.goto(url, wait_until='domcontentloaded', timeout=60000)

            # Wait for network idle (shorter timeout since we're doing many dates)
            try:
                page.wait_for_load_state('networkidle', timeout=30000)
            except PlaywrightTimeout:
                pass  # Continue anyway

            # Brief wait for JS
            time.sleep(2)

            # Check if we have event cards
            try:
                page.wait_for_selector('.ds-listing.event-card', timeout=10000)
            except PlaywrightTimeout:
                # No events on this page - might be end of this date's events
                if page_num == 1:
                    # No events for this date at all
                    return events_for_date
                else:
                    # Reached end of pagination for this date
                    break

            # Extract events from current page
            events_data = page.evaluate('''
                () => {
                    const events = [];
                    const eventElements = document.querySelectorAll('.ds-listing.event-card');

                    eventElements.forEach((el) => {
                        try {
                            const titleEl = el.querySelector('.ds-listing-event-title-text');
                            const title = titleEl ? titleEl.textContent.trim() : '';

                            if (!title) return;

                            const venueEl = el.querySelector('a[href*="/venues/"]');
                            const venue = venueEl ? venueEl.textContent.trim() : 'Unknown Venue';

                            const linkEl = el.querySelector('a[href*="/events/"]');

                            let dateStr = '';
                            if (linkEl) {
                                const match = linkEl.href.match(/\/events\/(\d{4})\/(\d{1,2})\/(\d{1,2})\//);
                                if (match) {
                                    dateStr = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
                                }
                            }

                            const timeEl = el.querySelector('.ds-listing-event-date-time');
                            const time = timeEl ? timeEl.textContent.trim() : '';

                            const descEl = el.querySelector('.ds-listing-event-detail-text');
                            const description = descEl ? descEl.textContent.trim() : '';

                            const url = linkEl ? linkEl.href : '';

                            events.push({
                                title: title,
                                venue: venue,
                                dateStr: dateStr,
                                time: time,
                                description: description,
                                url: url
                            });

                        } catch (err) {
                            console.error('Error extracting event:', err);
                        }
                    });

                    return events;
                }
            ''')

            if len(events_data) == 0:
                # No events found, probably end of pagination
                break

            # Process and deduplicate
            new_events_count = 0
            for event in events_data:
                event_key = (event['title'], event['dateStr'], event['venue'])

                if event_key in seen_events:
                    continue

                seen_events.add(event_key)

                # Parse date
                date_str_parsed = event.get('dateStr', '')
                if date_str_parsed:
                    try:
                        date_obj = datetime.strptime(date_str_parsed, '%Y-%m-%d')
                        date_iso = date_obj.isoformat() + 'Z'
                    except ValueError:
                        date_iso = datetime.now().isoformat() + 'Z'
                else:
                    date_iso = datetime.now().isoformat() + 'Z'

                show = {
                    'venue': event['venue'],
                    'title': event['title'],
                    'date': date_iso,
                    'time': event.get('time', ''),
                    'description': event.get('description', ''),
                    'url': event.get('url', '')
                }

                events_for_date.append(show)
                new_events_count += 1

            if new_events_count == 0:
                # All events on this page were duplicates, probably end of unique content
                break

            # Check if there's a next page for this date
            has_next = page.evaluate('''
                () => {
                    let nextButton = document.querySelector('button[aria-label*="next" i], a[aria-label*="next" i]');

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
                break

            page_num += 1
            time.sleep(1.5)  # Brief delay between pages

        except Exception as e:
            print(f"    ⚠️  Error on page {page_num} for {display_date}: {e}")
            break

    return events_for_date


def scrape_do312_by_date(page, days_ahead: int = 60) -> List[Dict]:
    """
    Scrape Do312 comedy events by iterating through dates.

    This fixes the broken pagination issue where pages 4+ just repeat page 3.
    Instead, we iterate through date-specific URLs.

    Args:
        page: Playwright page object
        days_ahead: Number of days into the future to scrape

    Returns:
        List of all events found
    """
    all_events = []
    seen_events: Set[Tuple[str, str, str]] = set()

    # Start from today
    current_date = datetime.now()

    print(f"Scraping Do312 comedy events by date")
    print(f"Date range: {current_date.strftime('%m/%d/%Y')} to {(current_date + timedelta(days=days_ahead)).strftime('%m/%d/%Y')}")
    print(f"Total dates to check: {days_ahead + 1}\n")

    for day_offset in range(days_ahead + 1):
        date = current_date + timedelta(days=day_offset)
        date_str = date.strftime('%Y/%m/%d')  # Format: 2026/03/19
        display_date = date.strftime('%m/%d')  # Format: 03/19

        print(f"[{day_offset + 1}/{days_ahead + 1}] Scraping {display_date}...", end=' ')

        try:
            events_for_date = scrape_date_page(page, date_str, seen_events)

            if events_for_date:
                all_events.extend(events_for_date)
                print(f"✓ Found {len(events_for_date)} events (total: {len(all_events)})")
            else:
                print(f"- No events")

        except Exception as e:
            print(f"✗ Error: {e}")
            continue

        # Small delay between dates to be respectful
        time.sleep(1)

    return all_events


def scrape_all_events() -> List[Dict]:
    """Scrape all comedy events using Playwright"""
    all_shows = []

    print("Starting Chicago Comedy Calendar scraper...")
    print("Using DATE-BASED scraping (fixes broken pagination)\n")

    with sync_playwright() as p:
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

        page = browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )

        page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        })

        print("✓ Browser launched successfully\n")

        # Scrape comedy events by date (60 days ahead)
        all_shows = scrape_do312_by_date(page, days_ahead=60)

        print("\nClosing browser...")
        browser.close()
        print("✓ Browser closed\n")

    return all_shows


def save_shows(shows: List[Dict], existing_shows: List[Dict]):
    """
    Save shows to JSON file, but only if we got enough data

    Args:
        shows: Newly scraped shows
        existing_shows: Previously saved shows
    """
    # Determine if new scrape is good enough to save
    MIN_SHOWS_THRESHOLD = 50  # Expect at least 50 shows with date-based scraping

    if len(shows) < MIN_SHOWS_THRESHOLD:
        if len(existing_shows) > 0:
            print(f"\n⚠️  WARNING: Only scraped {len(shows)} shows (below threshold of {MIN_SHOWS_THRESHOLD})")
            print(f"   Keeping existing {len(existing_shows)} shows to avoid data loss")
            print(f"   NOT overwriting shows.json")
            return False
        else:
            print(f"\n⚠️  WARNING: Only scraped {len(shows)} shows and no existing data")
            print(f"   Saving anyway (better than nothing)")

    # If new scrape is significantly worse than existing, warn but don't save
    if len(existing_shows) > 0:
        loss_threshold = 0.5  # Don't save if we lose more than 50% of shows
        if len(shows) < len(existing_shows) * loss_threshold:
            print(f"\n⚠️  WARNING: New scrape has {len(shows)} shows vs {len(existing_shows)} existing (>{100-loss_threshold*100}% loss)")
            print(f"   Keeping existing shows to avoid data loss")
            print(f"   NOT overwriting shows.json")
            return False

    # Save the new data
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'shows': shows
    }

    with open('shows.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Saved {len(shows)} shows to shows.json")
    return True


def main():
    start_time = time.time()
    print(f"{'='*60}")
    print(f"Chicago Comedy Calendar Scraper - DATE-BASED")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Load existing shows first
        existing_shows = load_existing_shows()
        if existing_shows:
            print(f"📚 Found {len(existing_shows)} existing shows in shows.json\n")

        # Scrape new data
        shows = scrape_all_events()

        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total shows scraped: {len(shows)}")
        print(f"Existing shows: {len(existing_shows)}")
        print(f"Time elapsed: {elapsed:.1f} seconds")

        if shows:
            venues = {}
            for show in shows:
                venue = show['venue']
                venues[venue] = venues.get(venue, 0) + 1

            print(f"\nShows per venue ({len(venues)} total venues):")
            sorted_venues = sorted(venues.items(), key=lambda x: x[1], reverse=True)
            for venue, count in sorted_venues[:10]:
                print(f"  - {venue}: {count}")
            if len(sorted_venues) > 10:
                print(f"  ... and {len(sorted_venues) - 10} more venues")

        # Try to save, but protect against bad scrapes
        saved = save_shows(shows, existing_shows)

        if saved:
            print("\n✓ Scraping complete!")
            sys.exit(0)
        else:
            print("\n⚠️  Scrape completed but data not saved (kept existing)")
            sys.exit(0)  # Still exit 0 so workflow doesn't fail

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"SCRAPING FAILED")
        print(f"{'='*60}")
        print(f"Error: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

        # Check if we have existing data to fall back on
        try:
            existing = load_existing_shows()
            if existing:
                print(f"\n✓ Keeping existing {len(existing)} shows (data preserved)")
                sys.exit(0)  # Don't fail the workflow if we have existing data
        except:
            pass

        sys.exit(1)


if __name__ == '__main__':
    main()
