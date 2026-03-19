#!/bin/bash
# Improved Union Hall scraper with scrolling support
# Captures 80+ shows by loading all lazy-loaded events

echo "🎭 Starting Union Hall scraper (improved)..."
echo "📍 Navigating to Union Hall calendar..."

agent-browser open https://unionhallny.com/calendar
sleep 3

echo "📜 Scrolling to load all events..."

# Scroll multiple times to load all lazy-loaded content
agent-browser eval "
(async () => {
    // Scroll to bottom multiple times to trigger lazy loading
    for (let i = 0; i < 5; i++) {
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    return 'Scrolling complete';
})();
"

sleep 2

echo "📊 Extracting event data..."

agent-browser eval "
const events = [];
const pageText = document.body.innerText;
const lines = pageText.split('\\n').map(l => l.trim()).filter(l => l);

// Parse the calendar format:
// Mar
// 19
// The Book of Red Flags Live!
// (performers list)
// BUY

let i = 0;
while (i < lines.length - 2) {
    const line = lines[i];

    // Check if this is a month abbreviation (Mar, Apr, etc.)
    if (line.match(/^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$/)) {
        const month = line;
        const day = lines[i+1];
        const title = lines[i+2];

        // Verify format: month, day (number), title (not BUY/REGISTER/CALENDAR)
        if (day.match(/^\\d{1,2}$/) && title && title.length > 3 &&
            !title.match(/^(BUY|REGISTER|CALENDAR|GROUP|FOOD|DRINK|GALLERY|INFO|RESERVATIONS)$/i)) {

            const currentYear = new Date().getFullYear();
            const currentMonth = new Date().getMonth();

            // Parse month
            const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            const monthIndex = monthNames.indexOf(month);

            if (monthIndex !== -1) {
                let year = currentYear;

                // If the event month is before current month, it's next year
                if (monthIndex < currentMonth) {
                    year = currentYear + 1;
                }

                const dateObj = new Date(year, monthIndex, parseInt(day));

                // Get performers/description if available
                let description = '';
                if (i + 3 < lines.length && !lines[i+3].match(/^(BUY|REGISTER|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\\d{1,2})$/)) {
                    description = lines[i+3];
                }

                events.push({
                    title: title,
                    venue: 'Union Hall',
                    date: dateObj.toISOString(),
                    time: null,
                    description: description || null,
                    url: 'https://unionhallny.com/calendar'
                });
            }
        }
    }
    i++;
}

// Deduplicate by title + date
const unique = [];
const seen = new Set();

events.forEach(event => {
    const key = event.title + '|' + event.date.substring(0, 10);
    if (!seen.has(key)) {
        seen.add(key);
        unique.push(event);
    }
});

JSON.stringify({
    shows: unique,
    lastUpdated: new Date().toISOString(),
    venue: 'Union Hall',
    totalShows: unique.length
}, null, 2);
" > union-hall-shows.json

agent-browser close

echo "✅ Scraping complete!"
echo "📝 Results saved to union-hall-shows.json"
echo ""
echo "📋 Summary:"
python3 -c "
import json
try:
    with open('union-hall-shows.json', 'r') as f:
        content = f.read().strip()
        # Handle JSON-as-string from agent-browser
        if content.startswith('\"') and content.endswith('\"'):
            content = json.loads(content)
        data = json.loads(content)
        print(f'Total shows: {data.get(\"totalShows\", 0)}')
        print(f'Last updated: {data.get(\"lastUpdated\", \"N/A\")}')

        # Count by month
        from collections import Counter
        dates = Counter()
        for show in data.get('shows', []):
            date = show.get('date', '')[:7]  # YYYY-MM
            if date:
                dates[date] += 1

        print(f'\\nShows across {len(dates)} months')
        print('\\nSample shows:')
        for show in data.get('shows', [])[:5]:
            print(f'  • {show[\"title\"][:60]}')
            print(f'    Date: {show[\"date\"][:10]}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
