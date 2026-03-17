#!/bin/bash
# Comedy Cellar Scraper V2 - Simpler approach
# Scrape multiple dates by selecting from dropdown

echo "🎭 Starting Comedy Cellar scraper V2..."

# Array to store all shows
ALL_SHOWS="[]"

# How many dates to scrape (default 14)
MAX_DATES=${MAX_DATES:-14}

for date_index in $(seq 0 $((MAX_DATES - 1))); do
    echo "📆 Scraping date index $date_index..."

    # Open page
    agent-browser open https://www.comedycellar.com/new-york-line-up/
    sleep 2

    # Select date from dropdown
    agent-browser select @e11 "$date_index"
    sleep 2

    # Extract shows for this date
    SHOWS=$(agent-browser eval "
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

    # Merge with ALL_SHOWS
    ALL_SHOWS=$(python3 -c "
import json, sys
existing = json.loads('$ALL_SHOWS')
new = json.loads('''$SHOWS''')
existing.extend(new)
print(json.dumps(existing))
")

    SHOW_COUNT=$(echo "$SHOWS" | grep -o '"title"' | wc -l)
    echo "  ✓ Found $SHOW_COUNT shows"

    agent-browser close
done

# Create final JSON
python3 << EOF
import json
from datetime import datetime

shows = json.loads('''$ALL_SHOWS''')

output = {
    'shows': shows,
    'lastUpdated': datetime.now().isoformat() + 'Z',
    'venue': 'Comedy Cellar',
    'totalShows': len(shows)
}

with open('comedy-cellar-shows.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f'\\n✅ Total: {len(shows)} shows saved to comedy-cellar-shows.json')
print(f'\\nSample shows:')
for show in shows[:3]:
    print(f'  • {show["title"][:50]}')
    print(f'    {show["venue"]}, {show["time"]}')
EOF
