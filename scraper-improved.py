#!/usr/bin/env python3
"""
Chicago Comedy Calendar Scraper - IMPROVED VERSION
- Better timeout handling
- Prevents data loss on partial scrapes
- Only saves if scrape is successful enough
"""

import json
import sys
import time
from datetime import datetime
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


def scrape_do312_comedy_events(page) -> List[Dict]:
    """Scrape all comedy events from Do312's comedy category page"""
    all_events = []
    seen_events: Set[Tuple[str, str, str]] = set()
    page_num = 1
    consecutive_failures = 0
    MAX_FAILURES = 2  # Stop after 2 consecutive page failures

    base_url = 'https://do312.com/events/comedy'

    print(f"Fetching comedy events from Do312...")
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
            # Navigate with increased timeout (2 minutes)
            print(f"  Navigating to page...")
            page.goto(url, wait_until='domcontentloaded', timeout=120000)

            # Wait for network idle with increased timeout
            print(f"  Waiting for network idle...")
            try:
                page.wait_for_load_state('networkidle', timeout=90000)
            except PlaywrightTimeout:
                print(f"  ⚠️  Network idle timeout, but continuing...")

            # Extra buffer for JavaScript
            time.sleep(3)

            # Check if we have event cards
            print(f"  Checking for event cards...")
            try:
                page.wait_for_selector('.ds-listing.event-card', timeout=15000)
            except PlaywrightTimeout:
                print(f"  No event cards found on page {page_num}")
                if page_num == 1:
                    print(f"  ERROR: No events on first page - site may be down")
                    break
                else:
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
                            const titleEl = el.querySelector('.ds-listing-event-title-text');
                            const title = titleEl ? titleEl.textContent.trim() : '';

                            if (!title) {
                                return;
                            }

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

            print(f"  Found {len(events_data)} events on page {page_num}")

            # Process and deduplicate
            new_events_count = 0
            for event in events_data:
                event_key = (event['title'], event['dateStr'], event['venue'])

                if event_key in seen_events:
                    continue

                seen_events.add(event_key)

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
                    'venue': event['venue'],
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

            # Reset failure counter on success
            consecutive_failures = 0

            # Check if there's a next page
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
                print(f"  No 'Next' button found - reached end of pagination")
                break

            # Move to next page
            page_num += 1
            time.sleep(3)  # Increased delay

        except PlaywrightTimeout as e:
            print(f"  ⚠️  Timeout on page {page_num}: {e}")
            consecutive_failures += 1

            if consecutive_failures >= MAX_FAILURES:
                print(f"  Stopping after {MAX_FAILURES} consecutive failures")
                break

            if len(all_events) > 0:
                print(f"  Continuing with {len(all_events)} events scraped so far...")
                break
            else:
                print(f"  No events scraped yet, trying next page...")
                page_num += 1
                time.sleep(5)

        except Exception as e:
            print(f"  Error on page {page_num}: {e}")
            consecutive_failures += 1

            if consecutive_failures >= MAX_FAILURES or len(all_events) == 0:
                print(f"  Stopping pagination")
                break

            print(f"  Continuing with {len(all_events)} events scraped so far...")
            break

    return all_events


def scrape_all_events() -> List[Dict]:
    """Scrape all comedy events using Playwright"""
    all_shows = []

    print("Starting Chicago Comedy Calendar scraper...")
    print("Scraping ALL comedy events from Do312.com\n")

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

        # Scrape comedy events
        all_shows = scrape_do312_comedy_events(page)

        print("Closing browser...")
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
    MIN_SHOWS_THRESHOLD = 20  # Require at least 20 shows

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
    print(f"Chicago Comedy Calendar Scraper - IMPROVED")
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
