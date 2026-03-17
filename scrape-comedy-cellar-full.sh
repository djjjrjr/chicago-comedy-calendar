#!/bin/bash
# Scrape Comedy Cellar events - FULL VERSION (all 28 days)
# Iterates through date dropdown to get complete calendar

echo "🎭 Starting Comedy Cellar FULL scraper..."
echo "📍 Navigating to Comedy Cellar lineup page..."

agent-browser open https://www.comedycellar.com/new-york-line-up/
sleep 3

# Get total number of dates available
TOTAL_DATES=$(agent-browser eval "document.querySelector('select') ? document.querySelector('select').options.length : 0")
echo "📅 Found $TOTAL_DATES dates available"

# Decide how many dates to scrape (max 28, or use env variable)
DATES_TO_SCRAPE=${MAX_DATES:-14}
if [ "$DATES_TO_SCRAPE" -gt "$TOTAL_DATES" ]; then
    DATES_TO_SCRAPE=$TOTAL_DATES
fi

echo "🔄 Will scrape $DATES_TO_SCRAPE dates..."

# Initialize empty shows array
echo '{"shows":[],"lastUpdated":"","venue":"Comedy Cellar","totalShows":0}' > comedy-cellar-shows.json

# Scrape each date
for i in $(seq 0 $((DATES_TO_SCRAPE - 1))); do
    echo "📆 Scraping date $((i + 1)) of $DATES_TO_SCRAPE..."

    # Select the date by index
    agent-browser eval "
        const select = document.querySelector('select');
        if (select && select.options[$i]) {
            select.selectedIndex = $i;
            select.dispatchEvent(new Event('change', { bubbles: true }));
        }
    " > /dev/null

    # Wait for page to update
    sleep 2

    # Extract shows for this date
    agent-browser eval "
        const allShows = [];
        const dateSelect = document.querySelector('select');
        const currentDateText = dateSelect ? dateSelect.options[dateSelect.selectedIndex].text : '';

        // Parse current date
        const dateMatch = currentDateText.match(/(\\w+)\\s+(\\w+)\\s+(\\d+),\\s+(\\d{4})/);
        let isoDate = new Date().toISOString();
        if (dateMatch) {
            const [_, dayOfWeek, month, day, year] = dateMatch;
            const dateObj = new Date(\`\${month} \${day}, \${year}\`);
            isoDate = dateObj.toISOString();
        }

        // Get all show information from page text
        const pageText = document.body.innerText;

        // Match pattern: '6:45 pm show-MacDougal Street'
        const showMatches = [...pageText.matchAll(/(\\d+:\\d+)\\s*([ap]m)\\s+show-([^\\n\\+]+)/gi)];

        showMatches.forEach(match => {
            const time = match[1] + ' ' + match[2]; // e.g., '6:45 pm'
            const venueInfo = match[3].trim();

            // Determine venue and title
            let venueName = 'Comedy Cellar';
            let title = 'Comedy Showcase';
            let description = 'Lineup to be announced';

            if (venueInfo.includes('MacDougal')) {
                venueName = 'Comedy Cellar - MacDougal Street';
            } else if (venueInfo.includes('Village Underground')) {
                venueName = 'Comedy Cellar - Village Underground';
            } else if (venueInfo.includes('Fat Black') || venueInfo.includes('FBPC')) {
                if (venueInfo.includes('Bar')) {
                    venueName = 'Comedy Cellar - Fat Black Pussycat (Bar)';
                } else if (venueInfo.includes('Lounge')) {
                    venueName = 'Comedy Cellar - Fat Black Pussycat (Lounge)';
                } else {
                    venueName = 'Comedy Cellar - Fat Black Pussycat';
                }
            }

            // Check if this is a special show (has a title beyond venue)
            const specialShowMatch = venueInfo.match(/([^:]+):/);
            if (specialShowMatch) {
                title = specialShowMatch[1].trim();
                description = venueInfo;
            }

            allShows.push({
                title: title,
                venue: venueName,
                date: isoDate,
                time: time,
                description: description,
                url: 'https://www.comedycellar.com/reservations-newyork/'
            });
        });

        JSON.stringify(allShows);
    " > /tmp/comedy-cellar-date-$i.json

    SHOW_COUNT=$(cat /tmp/comedy-cellar-date-$i.json | grep -o '"title"' | wc -l)
    echo "  ✓ Found $SHOW_COUNT shows"
done

echo ""
echo "📊 Combining all dates..."

# Combine all JSON files
python3 << 'EOF'
import json
import glob
from datetime import datetime

all_shows = []

# Read all temporary JSON files
for filename in sorted(glob.glob('/tmp/comedy-cellar-date-*.json')):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            if content and content != '[]':
                shows = json.loads(content)
                all_shows.extend(shows)
    except Exception as e:
        print(f"Warning: Could not parse {filename}: {e}")

# Create final output
output = {
    'shows': all_shows,
    'lastUpdated': datetime.now().isoformat() + 'Z',
    'venue': 'Comedy Cellar',
    'totalShows': len(all_shows)
}

with open('comedy-cellar-shows.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f'✅ Combined {len(all_shows)} total shows')
EOF

# Cleanup temp files
rm -f /tmp/comedy-cellar-date-*.json

agent-browser close

echo ""
echo "✅ Scraping complete!"
echo "📝 Results saved to comedy-cellar-shows.json"
echo ""
echo "📋 Summary:"
python3 -c "
import json
with open('comedy-cellar-shows.json', 'r') as f:
    data = json.load(f)
    print(f'Total shows: {data[\"totalShows\"]}')
    print(f'Last updated: {data[\"lastUpdated\"]}')
    print(f'\\nSample shows:')
    for show in data['shows'][:5]:
        print(f'  • {show[\"title\"][:50]}')
        print(f'    {show[\"venue\"]}, {show[\"time\"]} on {show[\"date\"][:10]}')
"
