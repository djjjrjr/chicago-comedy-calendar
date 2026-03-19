#!/usr/bin/env python3
"""
Do312 Venue Page Scraper
Scrapes individual venue pages for Chicago preferred venues
"""

import json
import subprocess
import sys
from datetime import datetime

# Chicago preferred venues with their Do312 slugs
VENUES = {
    'The Second City': 'the-second-city',
    'iO Theater': 'io-theater',
    'Annoyance Theatre': 'annoyance-theatre',
    'Zanies Comedy Club': 'zanies-comedy-club-chicago',
    'Laugh Factory': 'laugh-factory-chicago',
    'The Lincoln Lodge': 'the-lincoln-lodge',
    'Den Theatre': 'the-den-theatre'
}

def scrape_venue(venue_name, venue_slug):
    """Scrape a single venue page from Do312"""
    url = f'https://do312.com/venues/{venue_slug}'

    print(f"  📍 {venue_name}...")

    try:
        # Open venue page
        subprocess.run(['agent-browser', 'open', url],
                      check=True, capture_output=True, timeout=30)

        # Wait for page load
        subprocess.run(['sleep', '2'], check=True)

        # Extract events
        js_code = """
            const shows = [];
            const eventCards = document.querySelectorAll('.ds-listing.event-card');

            eventCards.forEach(card => {
                const titleEl = card.querySelector('.ds-listing-event-title-text');
                const title = titleEl ? titleEl.textContent.trim() : '';

                if (!title) return;

                const venueEl = card.querySelector('a[href*="/venues/"]');
                const venue = venueEl ? venueEl.textContent.trim() : '';

                const linkEl = card.querySelector('a[href*="/events/"]');
                let dateStr = '';
                if (linkEl) {
                    const match = linkEl.href.match(/\\/events\\/(\\d{4})\\/(\\d{1,2})\\/(\\d{1,2})\\//);
                    if (match) {
                        dateStr = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
                    }
                }

                const timeEl = card.querySelector('.ds-listing-event-date-time');
                const time = timeEl ? timeEl.textContent.trim() : '';

                const descEl = card.querySelector('.ds-listing-event-detail-text');
                const description = descEl ? descEl.textContent.trim() : '';

                const url = linkEl ? linkEl.href : '';

                shows.push({
                    title: title,
                    venue: venue,
                    date: dateStr,
                    time: time,
                    description: description,
                    url: url
                });
            });

            JSON.stringify(shows);
        """

        result = subprocess.run(
            ['agent-browser', 'eval', js_code],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        # Parse output
        output = result.stdout.strip()
        if output.startswith('"') and output.endswith('"'):
            output = json.loads(output)

        shows = json.loads(output)

        # Convert dates to ISO format
        for show in shows:
            if show['date']:
                try:
                    date_obj = datetime.strptime(show['date'], '%Y-%m-%d')
                    show['date'] = date_obj.isoformat() + 'Z'
                except:
                    pass

        print(f"     ✓ {len(shows)} events")
        return shows

    except subprocess.TimeoutExpired:
        print(f"     ⚠️  Timeout")
        return []
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return []

def main():
    print("🎭 Starting Do312 Venue Page Scraper...")
    print(f"📋 Scraping {len(VENUES)} preferred venues\n")

    all_shows = []
    venue_counts = {}

    for venue_name, venue_slug in VENUES.items():
        shows = scrape_venue(venue_name, venue_slug)
        all_shows.extend(shows)
        venue_counts[venue_name] = len(shows)

    # Close browser
    try:
        subprocess.run(['agent-browser', 'close'],
                      check=True, capture_output=True, timeout=10)
    except:
        pass

    # Deduplicate
    seen = set()
    unique_shows = []
    for show in all_shows:
        key = (show['title'], show['date'][:10] if show['date'] else '', show['venue'])
        if key not in seen:
            seen.add(key)
            unique_shows.append(show)

    # Save
    output = {
        'shows': unique_shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'totalShows': len(unique_shows),
        'source': 'Do312 Venue Pages'
    }

    with open('do312-venues-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scraping complete!")
    print(f"📊 Total: {len(all_shows)} events → {len(unique_shows)} unique")
    print(f"📝 Saved to do312-venues-shows.json\n")

    print("📋 Breakdown by venue:")
    for venue, count in sorted(venue_counts.items(), key=lambda x: -x[1]):
        print(f"  • {venue}: {count} events")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
        subprocess.run(['agent-browser', 'close'], capture_output=True)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        subprocess.run(['agent-browser', 'close'], capture_output=True)
        sys.exit(1)
