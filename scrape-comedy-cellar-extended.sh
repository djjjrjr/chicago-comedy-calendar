#!/bin/bash
# Comedy Cellar Extended Scraper - Scrapes 14 days of shows
# Uses reliable approach: iterate through dropdown options

echo "🎭 Starting Comedy Cellar EXTENDED scraper..."

# How many days to scrape (default 14, can override with MAX_DAYS env var)
MAX_DAYS=${MAX_DAYS:-14}
echo "📅 Will scrape $MAX_DAYS days of shows..."

# Initialize combined JSON file
echo '[]' > /tmp/comedy-cellar-all-shows.json

# Counter for successful scrapes
TOTAL_SHOWS=0

for day_index in $(seq 0 $((MAX_DAYS - 1))); do
    echo ""
    echo "📆 Scraping day $((day_index + 1)) of $MAX_DAYS..."

    # Open Comedy Cellar page
    agent-browser open https://www.comedycellar.com/new-york-line-up/ > /dev/null 2>&1
    sleep 2

    # Get the date value for this index
    DATE_VALUE=$(agent-browser eval "
        const select = document.querySelector('select');
        select.options[$day_index] ? select.options[$day_index].value : null;
    ")

    if [ "$DATE_VALUE" == "null" ] || [ -z "$DATE_VALUE" ]; then
        echo "  ⚠️  No more dates available, stopping at day $day_index"
        agent-browser close > /dev/null 2>&1
        break
    fi

    # Select the date
    agent-browser select "select" "$DATE_VALUE" > /dev/null 2>&1
    sleep 2

    # Extract shows for this date
    SHOWS_JSON=$(agent-browser eval "
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
        const showMatches = [...pageText.matchAll(/(\\d+:\\d+)\\s*([ap]m)\\s+show-([^\\n\\+]+)/gi)];

        showMatches.forEach(match => {
            const time = match[1] + ' ' + match[2];
            const venueInfo = match[3].trim();

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
    ")

    # Count shows for this day
    DAY_SHOW_COUNT=$(echo "$SHOWS_JSON" | grep -o '"title"' | wc -l)
    echo "  ✓ Found $DAY_SHOW_COUNT shows"
    TOTAL_SHOWS=$((TOTAL_SHOWS + DAY_SHOW_COUNT))

    # Append to combined file
    python3 << EOF
import json
try:
    with open('/tmp/comedy-cellar-all-shows.json', 'r') as f:
        all_shows = json.load(f)
    new_shows = json.loads('''$SHOWS_JSON''')
    all_shows.extend(new_shows)
    with open('/tmp/comedy-cellar-all-shows.json', 'w') as f:
        json.dump(all_shows, f)
except Exception as e:
    print(f"Error combining shows: {e}")
EOF

    # Close browser for this iteration
    agent-browser close > /dev/null 2>&1

    # Small delay between iterations
    sleep 1
done

echo ""
echo "📊 Creating final output file..."

# Create final JSON with metadata
python3 << 'EOF'
import json
from datetime import datetime

try:
    with open('/tmp/comedy-cellar-all-shows.json', 'r') as f:
        shows = json.load(f)

    output = {
        'shows': shows,
        'lastUpdated': datetime.now().isoformat() + 'Z',
        'venue': 'Comedy Cellar',
        'totalShows': len(shows)
    }

    with open('comedy-cellar-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'\n✅ Success! Scraped {len(shows)} total shows')
    print(f'📝 Saved to comedy-cellar-shows.json')
    print(f'\n📋 Sample shows:')
    for show in shows[:5]:
        print(f'  • {show["title"][:50]}')
        print(f'    {show["venue"]}, {show["time"]} on {show["date"][:10]}')

except Exception as e:
    print(f'Error creating final file: {e}')
EOF

# Cleanup
rm -f /tmp/comedy-cellar-all-shows.json

echo ""
echo "✅ Comedy Cellar scraping complete!"
