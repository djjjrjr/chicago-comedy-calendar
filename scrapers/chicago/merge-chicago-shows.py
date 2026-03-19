#!/usr/bin/env python3
"""
Merge Chicago shows from comedy category + venue pages
"""

import json
from datetime import datetime

def load_shows(filename):
    """Load shows from JSON file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get('shows', [])
    except FileNotFoundError:
        print(f"  ⚠️  {filename} not found")
        return []
    except Exception as e:
        print(f"  ❌ Error loading {filename}: {e}")
        return []

def deduplicate(shows):
    """Remove duplicate shows"""
    seen = set()
    unique = []

    for show in shows:
        key = (
            show.get('venue', ''),
            show.get('date', '')[:10],
            show.get('time', '') or '',
            show.get('title', '')[:50]
        )

        if key not in seen:
            seen.add(key)
            unique.append(show)

    return unique

def main():
    print("🔄 Merging Chicago comedy shows...\n")

    # Load from both sources
    comedy_shows = load_shows('shows.json')  # From comedy category
    venue_shows = load_shows('do312-venues-shows.json')  # From venue pages

    print(f"  ✓ Comedy category: {len(comedy_shows)} shows")
    print(f"  ✓ Venue pages: {len(venue_shows)} shows")

    # Combine
    all_shows = comedy_shows + venue_shows
    print(f"\n📈 Total before dedup: {len(all_shows)}")

    # Deduplicate
    unique_shows = deduplicate(all_shows)
    overlap = len(all_shows) - len(unique_shows)
    print(f"📉 Duplicates removed: {overlap}")
    print(f"✅ Final unique shows: {len(unique_shows)}")

    # Sort by date
    unique_shows.sort(key=lambda x: (x.get('date', ''), x.get('time', '') or ''))

    # Create output
    output = {
        'shows': unique_shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'totalShows': len(unique_shows),
        'sources': ['Do312 Comedy Category', 'Do312 Venue Pages']
    }

    # Save
    with open('shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Merged → shows.json")

    # Show breakdown by venue
    venue_counts = {}
    for show in unique_shows:
        venue = show.get('venue', 'Unknown')
        venue_counts[venue] = venue_counts.get(venue, 0) + 1

    print(f"\n📊 Top venues:")
    for venue, count in sorted(venue_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  • {venue}: {count}")

if __name__ == '__main__':
    main()
