#!/usr/bin/env python3
"""
NY Shows Merger - Combines all data sources
"""

import json
import os
from datetime import datetime

def load_shows(filename):
    """Load shows, handling JSON-as-string issue"""
    if not os.path.exists(filename):
        print(f"  ⚠️  {filename} not found")
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
    """Normalize venue names"""
    if not venue:
        return venue
    # Comedy Cellar sub-venues → Comedy Cellar
    if 'Comedy Cellar' in venue:
        return 'Comedy Cellar'
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
        'ucb-ny-shows.json'
    ]

    all_shows = []

    for source in sources:
        shows = load_shows(source)
        all_shows.extend(shows)

    print(f"\n📈 Total before processing: {len(all_shows)}")

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
        'sources': ['DoNYC', 'Caveat', 'Union Hall', 'Comedy Cellar', 'UCB Theatre'],
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
