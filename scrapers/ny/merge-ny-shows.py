#!/usr/bin/env python3
"""
NY Shows Merger - Combines all data sources
"""

import json
import os
from datetime import datetime, timezone

def filter_stale_shows(shows):
    """Remove shows older than today"""
    today = datetime.now(timezone.utc).date()
    fresh_shows = []

    for show in shows:
        try:
            # Parse the date field (could be ISO string or just date)
            date_str = show.get('date', '')
            if date_str:
                # Handle both ISO format and simple date format
                if 'T' in date_str:
                    show_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
                else:
                    show_date = datetime.strptime(date_str[:10], '%Y-%m-%d').date()

                if show_date >= today:
                    fresh_shows.append(show)
        except:
            # If we can't parse the date, keep the show
            fresh_shows.append(show)

    return fresh_shows

def load_shows(filename):
    """Load shows, handling JSON-as-string issue"""
    if not os.path.exists(filename):
        print(f"  ⚠️  {filename} not found, skipping")
        return []

    try:
        with open(filename, 'r') as f:
            content = f.read().strip()

        # Handle JSON wrapped in quotes (from agent-browser eval)
        if content.startswith('"') and content.endswith('"'):
            content = json.loads(content)  # Unescape

        data = json.loads(content)

        # Extract shows array
        if isinstance(data, dict):
            shows = data.get('shows', [])
        elif isinstance(data, list):
            shows = data
        else:
            shows = []

        print(f"  ✓ Loaded {len(shows)} shows from {filename}")
        return shows

    except Exception as e:
        print(f"  ⚠️  Error loading {filename}: {e}")
        return []

def normalize_venue(venue):
    """Normalize venue names (currently disabled to preserve sub-venues)"""
    # DISABLED: Venue normalization was collapsing important sub-venue information
    # Comedy Cellar has multiple distinct rooms (MacDougal, Village Underground,
    # Fat Black Pussycat Bar/Lounge) that host simultaneous shows.
    # Preserving the full venue name is important for users to know which room.
    return venue

def deduplicate(shows):
    """Remove duplicates based on venue+date+time+title"""
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
    print("🔄 Merging NY comedy shows...")
    print()

    sources = [
        'ny-shows-donyc.json',
        'caveat-shows.json',
        'union-hall-shows.json',
        'comedy-cellar-shows.json',
        'the-stand-shows.json',
        'ucb-ny-shows.json',
        'bell-house-shows.json',
        'gotham-shows.json'
    ]

    all_shows = []

    for source in sources:
        shows = load_shows(source)
        all_shows.extend(shows)

    print(f"\n📈 Total before processing: {len(all_shows)}")

    # Filter stale shows
    all_shows = filter_stale_shows(all_shows)
    print(f"🗓️  After filtering old shows: {len(all_shows)}")

    # Normalize venue names
    for show in all_shows:
        show['venue'] = normalize_venue(show.get('venue'))

    # Deduplicate
    all_shows = deduplicate(all_shows)
    print(f"📉 After deduplication: {len(all_shows)}")

    # Sort by date
    all_shows.sort(key=lambda x: (x.get('date', ''), x.get('time', '') or ''))

    # Save
    output = {
        'shows': all_shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'sources': ['DoNYC', 'Caveat', 'Union Hall', 'Comedy Cellar', 'The Stand', 'UCB Theatre', 'The Bell House'],
        'totalShows': len(all_shows)
    }

    with open('ny-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Merged {len(all_shows)} shows → ny-shows.json")

    # Stats
    print(f"\n📊 Shows by venue:")
    venue_counts = {}
    for show in all_shows:
        v = show.get('venue', 'Unknown')
        venue_counts[v] = venue_counts.get(v, 0) + 1

    for venue, count in sorted(venue_counts.items(), key=lambda x: -x[1]):
        print(f"  • {venue}: {count}")

    print(f"\n📋 Sample shows:")
    for show in all_shows[:5]:
        print(f"  • {show.get('title', '')[:50]}")
        print(f"    {show.get('venue')}, {show.get('date')[:10]}")

if __name__ == '__main__':
    main()
