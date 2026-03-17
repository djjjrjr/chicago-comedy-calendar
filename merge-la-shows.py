#!/usr/bin/env python3
"""
Merge LA comedy shows from multiple sources into a single file
"""

import json
from datetime import datetime

def load_shows(filename):
    """Load shows from JSON file, handling JSON-as-string encoding"""
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()

        # Handle JSON wrapped in quotes (from agent-browser eval)
        if content.startswith('"') and content.endswith('"'):
            content = json.loads(content)  # Unescape the string

        data = json.loads(content)
        shows = data.get('shows', []) if isinstance(data, dict) else data
        return shows
    except FileNotFoundError:
        print(f"  ⚠️  {filename} not found, skipping")
        return []
    except Exception as e:
        print(f"  ❌ Error loading {filename}: {e}")
        return []

def normalize_venue(venue):
    """Normalize venue names for consistency"""
    # Add normalization rules here if needed
    return venue

def deduplicate(shows):
    """Remove duplicate shows based on venue, date, time, and title"""
    seen = set()
    unique = []

    for show in shows:
        # Create a unique key for each show
        key = (
            show.get('venue', ''),
            show.get('date', '')[:10],  # Just the date part
            show.get('time', '') or '',
            show.get('title', '')[:50]  # First 50 chars of title
        )

        if key not in seen:
            seen.add(key)
            unique.append(show)

    return unique

def main():
    print("🔄 Merging LA comedy shows...")
    print()

    all_shows = []

    # Try DoLA shows first
    dola_shows = load_shows('la-shows-dola.json')
    if not dola_shows:
        # Fallback: check if la-shows.json exists and has different data than what we're about to create
        try:
            with open('la-shows.json', 'r') as f:
                temp_data = json.load(f)
                # Only use if it doesn't have 'sources' key (meaning it's old DoLA data, not merged data)
                if 'sources' not in temp_data:
                    dola_shows = temp_data.get('shows', [])
                    print(f"  ✓ Loaded {len(dola_shows)} shows from la-shows.json (DoLA)")
        except:
            pass

    if dola_shows:
        all_shows.extend(dola_shows)
    else:
        print("  ⚠️  No DoLA data found")

    # Add UCB LA shows
    ucb_shows = load_shows('ucb-la-shows.json')
    if ucb_shows:
        print(f"  ✓ Loaded {len(ucb_shows)} shows from ucb-la-shows.json")
        all_shows.extend(ucb_shows)

    print()
    print(f"📈 Total before processing: {len(all_shows)}")

    # Normalize venue names
    for show in all_shows:
        show['venue'] = normalize_venue(show.get('venue', ''))

    # Deduplicate
    unique_shows = deduplicate(all_shows)
    print(f"📉 After deduplication: {len(unique_shows)}")

    # Sort by date
    unique_shows.sort(key=lambda x: (x.get('date', ''), x.get('time', '') or ''))

    # Create output
    output = {
        'shows': unique_shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'totalShows': len(unique_shows),
        'sources': ['DoLA', 'UCB FRANKLIN']
    }

    # Save merged data
    with open('la-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print(f"✅ Merged {len(unique_shows)} shows → la-shows.json")

    # Show breakdown by venue
    venue_counts = {}
    for show in unique_shows:
        venue = show.get('venue', 'Unknown')
        venue_counts[venue] = venue_counts.get(venue, 0) + 1

    print()
    print("📊 Shows by venue:")
    for venue, count in sorted(venue_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  • {venue}: {count}")

if __name__ == '__main__':
    main()
