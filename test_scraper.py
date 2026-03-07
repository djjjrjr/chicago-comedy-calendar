#!/usr/bin/env python3
"""
Test script to debug Do312 scraping
"""

from playwright.sync_api import sync_playwright
import json

def test_scrape_second_city():
    """Test scraping Second City venue page"""

    print("Starting browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://do312.com/venues/the-second-city"
        print(f"\nNavigating to: {url}")
        page.goto(url)
        page.wait_for_load_state('networkidle')

        print("\nWaiting for event cards...")
        try:
            page.wait_for_selector('.ds-listing.event-card', timeout=5000)
            print("✓ Event cards found on page")
        except Exception as e:
            print(f"✗ Could not find event cards: {e}")
            browser.close()
            return

        print("\nExtracting event data...")
        events = page.evaluate('''
            () => {
                const events = [];
                const eventElements = document.querySelectorAll('.ds-listing.event-card');

                console.log(`Found ${eventElements.length} event cards`);

                eventElements.forEach((el, index) => {
                    try {
                        // Title
                        const titleEl = el.querySelector('.ds-listing-event-title-text');
                        const title = titleEl ? titleEl.textContent.trim() : '';

                        // Date from URL
                        const linkEl = el.querySelector('a[href*="/events/"]');
                        let dateStr = '';
                        if (linkEl) {
                            const match = linkEl.href.match(/\\/events\\/(\\d{4})\\/(\\d{1,2})\\/(\\d{1,2})\\//);
                            if (match) {
                                dateStr = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
                            }
                        }

                        // Time
                        const timeEl = el.querySelector('.ds-event-time');
                        const time = timeEl ? timeEl.textContent.trim() : '';

                        // URL
                        const url = linkEl ? linkEl.href : '';

                        events.push({
                            index,
                            title,
                            dateStr,
                            time,
                            url
                        });
                    } catch (err) {
                        console.error(`Error extracting event ${index}:`, err);
                    }
                });

                return events;
            }
        ''')

        browser.close()

        print(f"\n{'='*60}")
        print(f"RESULTS: Found {len(events)} events")
        print(f"{'='*60}\n")

        if events:
            for event in events[:5]:  # Show first 5
                print(f"Event #{event['index']}:")
                print(f"  Title: {event['title']}")
                print(f"  Date: {event['dateStr']}")
                print(f"  Time: {event['time']}")
                print(f"  URL: {event['url']}")
                print()

            if len(events) > 5:
                print(f"... and {len(events) - 5} more events")
        else:
            print("✗ No events extracted - check selectors!")

        return events

if __name__ == '__main__':
    test_scrape_second_city()
