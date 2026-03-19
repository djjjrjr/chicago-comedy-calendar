#!/bin/bash
# Scrape The Stand NYC events using agent-browser
# Extracts all shows from their calendar page

echo "🎭 Starting The Stand scraper..."
echo "📍 Navigating to The Stand shows page..."

agent-browser open https://thestandnyc.com/shows
sleep 4

echo "📊 Extracting show data..."

agent-browser eval "
(async () => {
    // First scroll to bottom to ensure all content is loaded
    console.log('Scrolling to load all shows...');
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(resolve => setTimeout(resolve, 2000));

    const allShows = [];

    // Find all show containers - they are structured as heading pairs
    const showTitles = document.querySelectorAll('h2');

    console.log(\`Found \${showTitles.length} h2 elements\`);

    showTitles.forEach(titleElem => {
        const title = titleElem.textContent.trim();

        // Skip non-show headings
        if (!title || title.includes('Join our') || title.includes('Choose a Show')) {
            return;
        }

        // Find the next h3 sibling which contains date/time/room
        let dateElem = titleElem.nextElementSibling;
        while (dateElem && dateElem.tagName !== 'H3') {
            dateElem = dateElem.nextElementSibling;
        }

        if (!dateElem) return;

        const dateTimeText = dateElem.textContent.trim();

        // Parse date/time/room - Format: \"March 18 | 7:00 PM UPSTAIRS\"
        const match = dateTimeText.match(/([A-Za-z]+)\s+(\d+)\s*\|\s*(\d{1,2}:\d{2}\s*[AP]M)\s*(.+)?/i);

        if (match) {
            const [_, month, day, time, roomRaw] = match;

            // Clean up room (remove non-breaking spaces)
            const room = roomRaw ? roomRaw.replace(/\u00a0/g, ' ').trim() : '';

            // Construct date (assuming current/next year)
            const currentYear = new Date().getFullYear();
            const dateStr = \`\${month} \${day}, \${currentYear}\`;
            const dateObj = new Date(dateStr);

            // If date is in the past (more than 1 day), assume it's next year
            const daysDiff = (dateObj - new Date()) / (1000 * 60 * 60 * 24);
            if (daysDiff < -1) {
                dateObj.setFullYear(currentYear + 1);
            }

            const isoDate = dateObj.toISOString();

            // Build venue name with room if available
            let venueName = 'The Stand';
            if (room) {
                venueName = \`The Stand - \${room}\`;
            }

            // Try to find the URL for this show
            const titleLink = titleElem.querySelector('a');
            const url = titleLink ? titleLink.href : 'https://thestandnyc.com/shows';

            // Build description from title (comedian names are usually in the title)
            let description = title;

            allShows.push({
                title: title,
                venue: venueName,
                date: isoDate,
                time: time,
                description: description,
                url: url
            });
        }
    });

    // Deduplicate shows (same venue, date, time)
    const uniqueShows = [];
    const seen = new Set();

    allShows.forEach(show => {
        const key = \`\${show.venue}|\${show.date}|\${show.time}\`;
        if (!seen.has(key)) {
            seen.add(key);
            uniqueShows.push(show);
        }
    });

    console.log(\`Total shows found: \${allShows.length}\`);
    console.log(\`Unique shows after deduplication: \${uniqueShows.length}\`);

    return JSON.stringify({
        shows: uniqueShows,
        lastUpdated: new Date().toISOString(),
        venue: 'The Stand',
        totalShows: uniqueShows.length
    }, null, 2);
})();
" > the-stand-shows.json

agent-browser close

echo "✅ Scraping complete!"
echo "📝 Results saved to the-stand-shows.json"
echo ""
echo "📋 Summary:"
python3 -c "
import json
try:
    with open('the-stand-shows.json', 'r') as f:
        content = f.read().strip()
        # Handle JSON-as-string from agent-browser
        if content.startswith('\"') and content.endswith('\"'):
            content = json.loads(content)
        data = json.loads(content)
        print(f'Total shows: {data.get(\"totalShows\", 0)}')
        print(f'Last updated: {data.get(\"lastUpdated\", \"N/A\")}')

        # Count by date
        from collections import Counter
        dates = Counter()
        rooms = Counter()
        for show in data.get('shows', []):
            date = show.get('date', '')[:10]
            if date:
                dates[date] += 1
            venue = show.get('venue', '')
            if venue:
                rooms[venue] += 1

        print(f'\\nShows across {len(dates)} unique dates')
        print(f'\\nShows by room:')
        for room, count in sorted(rooms.items(), key=lambda x: -x[1]):
            print(f'  • {room}: {count}')

        print('\\nSample shows:')
        for show in data.get('shows', [])[:5]:
            print(f'  • {show[\"title\"][:60]}')
            print(f'    {show[\"venue\"]}, {show[\"time\"]}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
