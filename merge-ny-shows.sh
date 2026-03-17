#!/bin/bash
# Merge all NY comedy show data sources into single ny-shows.json
# Combines: DoNYC + Caveat + Union Hall + Comedy Cellar

echo "🔄 Starting NY shows merger..."

# Check that all source files exist
MISSING_FILES=0

if [ ! -f "ny-shows-donyc.json" ]; then
    echo "⚠️  Warning: ny-shows-donyc.json not found (DoNYC data)"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ ! -f "caveat-shows.json" ]; then
    echo "⚠️  Warning: caveat-shows.json not found"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ ! -f "union-hall-shows.json" ]; then
    echo "⚠️  Warning: union-hall-shows.json not found"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ ! -f "comedy-cellar-shows.json" ]; then
    echo "⚠️  Warning: comedy-cellar-shows.json not found"
    MISSING_FILES=$((MISSING_FILES + 1))
fi

if [ $MISSING_FILES -eq 4 ]; then
    echo "❌ Error: No source files found. Please run scrapers first."
    exit 1
fi

echo "📊 Merging data sources..."

# Python script to merge all sources
python3 << 'EOF'
import json
from datetime import datetime
import os

def load_shows(filename):
    """Load shows from a JSON file, return empty list if file doesn't exist"""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            # Handle different JSON structures
            if isinstance(data, dict):
                return data.get('shows', [])
            elif isinstance(data, list):
                return data
            return []
    except Exception as e:
        print(f"Warning: Could not load {filename}: {e}")
        return []

def normalize_venue_name(venue):
    """Normalize venue names to match PREFERRED_VENUES"""
    # Comedy Cellar sub-venues should all map to "Comedy Cellar"
    if venue and 'Comedy Cellar' in venue:
        return 'Comedy Cellar'
    return venue

def deduplicate_shows(shows):
    """Remove duplicate shows based on venue + date + time"""
    seen = set()
    unique_shows = []

    for show in shows:
        # Create a key for deduplication
        venue = show.get('venue', '')
        date = show.get('date', '')[:10]  # Just the date part (YYYY-MM-DD)
        time = show.get('time', '') or ''
        title = show.get('title', '')[:50]  # First 50 chars of title

        key = f"{venue}|{date}|{time}|{title}"

        if key not in seen:
            seen.add(key)
            unique_shows.append(show)

    return unique_shows

def main():
    all_shows = []

    # Load from all sources
    sources = [
        ('DoNYC', 'ny-shows-donyc.json'),
        ('Caveat', 'caveat-shows.json'),
        ('Union Hall', 'union-hall-shows.json'),
        ('Comedy Cellar', 'comedy-cellar-shows.json')
    ]

    for source_name, filename in sources:
        shows = load_shows(filename)
        if shows:
            print(f"✓ Loaded {len(shows)} shows from {source_name}")
            all_shows.extend(shows)
        else:
            print(f"⚠ No shows from {source_name}")

    print(f"\n📈 Total shows before processing: {len(all_shows)}")

    # Normalize venue names
    for show in all_shows:
        show['venue'] = normalize_venue_name(show.get('venue', ''))

    # Deduplicate
    all_shows = deduplicate_shows(all_shows)
    print(f"📉 After deduplication: {len(all_shows)} shows")

    # Sort by date
    all_shows.sort(key=lambda x: (x.get('date', ''), x.get('time', '') or ''))

    # Create output
    output = {
        'shows': all_shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'sources': [s[0] for s in sources],
        'totalShows': len(all_shows)
    }

    # Save merged file
    with open('ny-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Success! Merged {len(all_shows)} unique shows")
    print(f"📝 Saved to ny-shows.json")

    # Show breakdown by venue
    print("\n📊 Shows by venue:")
    venue_counts = {}
    for show in all_shows:
        venue = show.get('venue', 'Unknown')
        venue_counts[venue] = venue_counts.get(venue, 0) + 1

    for venue, count in sorted(venue_counts.items(), key=lambda x: -x[1]):
        print(f"  • {venue}: {count} shows")

    # Show sample
    print("\n📋 Sample shows:")
    for show in all_shows[:5]:
        print(f"  • {show.get('title', 'N/A')[:50]}")
        print(f"    {show.get('venue', 'N/A')}, {show.get('date', 'N/A')[:10]}")

if __name__ == '__main__':
    main()
EOF

echo ""
echo "✅ Merger complete!"
