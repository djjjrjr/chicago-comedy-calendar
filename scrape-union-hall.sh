#!/bin/bash
# Scrape Union Hall events using agent-browser

echo "🎭 Starting Union Hall scraper..."
echo "📍 Navigating to Union Hall calendar..."

agent-browser open https://unionhallny.com/calendar
sleep 3

echo "📊 Extracting event data..."

agent-browser eval "
const events = [];
const pageText = document.body.innerText;
const lines = pageText.split('\\n').map(l => l.trim()).filter(l => l);

// Parse the calendar format:
// Mar
// 17
// WHAT'S THE CRAIC? Hosted by Keara Sullivan
// (performers list)
// BUY

for (let i = 0; i < lines.length - 2; i++) {
    const line = lines[i];

    // Check if this is a month abbreviation (Mar, Apr, etc.)
    if (line.match(/^[A-Z][a-z]{2}$/)) {
        const month = line;
        const day = lines[i+1];
        const title = lines[i+2];

        // Verify format: month, day (number), title (not BUY/REGISTER)
        if (day.match(/^\\d+$/) && title && title.length > 3 && !title.match(/^(BUY|REGISTER|CALENDAR|GROUP)$/)) {
            const currentYear = new Date().getFullYear();
            const dateStr = \`\${month} \${day}, \${currentYear}\`;
            const dateObj = new Date(dateStr);

            // If date is in the past, assume next year
            if (dateObj < new Date()) {
                dateObj.setFullYear(currentYear + 1);
            }

            // Get ticket link
            const ticketLinks = Array.from(document.querySelectorAll('a[href*=\"buy\"], a[href*=\"register\"]'));
            let url = 'https://unionhallny.com/calendar';

            // Try to find matching link near this event
            for (const link of ticketLinks) {
                const linkText = link.textContent.trim().toUpperCase();
                if (linkText === 'BUY' || linkText === 'REGISTER') {
                    url = link.href;
                    break;
                }
            }

            events.push({
                title: title,
                venue: 'Union Hall',
                date: dateObj.toISOString(),
                time: null,  // Union Hall doesn't show times on calendar
                description: null,
                url: url
            });
        }
    }
}

JSON.stringify({
    shows: events,
    lastUpdated: new Date().toISOString(),
    venue: 'Union Hall',
    totalShows: events.length
}, null, 2);
" > union-hall-shows.json

agent-browser close

echo "✅ Scraping complete!"
echo "📝 Results saved to union-hall-shows.json"
echo ""
echo "📋 Summary:"
python3 -c "
import json
with open('union-hall-shows.json', 'r') as f:
    data = json.load(f)
    print(f'Total shows: {data[\"totalShows\"]}')
    print(f'Last updated: {data[\"lastUpdated\"]}')
    print('\\nSample shows:')
    for show in data['shows'][:5]:
        print(f'  • {show[\"title\"][:60]}')
        print(f'    Date: {show[\"date\"][:10]}')
"
