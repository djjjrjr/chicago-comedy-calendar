#!/bin/bash
# Scrape Comedy Cellar events using agent-browser
# Loops through all available dates (28 days)

echo "🎭 Starting Comedy Cellar scraper..."
echo "📍 Navigating to Comedy Cellar lineup page..."

agent-browser open https://www.comedycellar.com/new-york-line-up/
sleep 3

echo "📊 Extracting show data from all available dates..."

agent-browser eval "
(async () => {
    const allShows = [];
    const dateSelect = document.querySelector('select');

    if (!dateSelect) {
        return JSON.stringify({
            shows: [],
            error: 'Date selector not found',
            lastUpdated: new Date().toISOString()
        });
    }

    const totalDates = dateSelect.options.length;
    console.log(\`Found \${totalDates} dates to scrape\`);

    // Function to scrape shows from current page
    function scrapeCurrentPage() {
        const shows = [];
        const currentDateText = dateSelect.options[dateSelect.selectedIndex].text;

        // Parse date
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
            const time = match[1] + ' ' + match[2];
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

            // Check if this is a special show
            const specialShowMatch = venueInfo.match(/([^:]+):/);
            if (specialShowMatch) {
                title = specialShowMatch[1].trim();
                description = venueInfo;
            }

            // Get reservation URL
            const reservationLink = Array.from(document.querySelectorAll('a[href*=\"reservation\"]')).find(a =>
                a.textContent.includes(time) || a.textContent.includes('MAKE A RESERVATION')
            );
            const url = reservationLink ? reservationLink.href : 'https://www.comedycellar.com/new-york-line-up/';

            shows.push({
                title: title,
                venue: venueName,
                date: isoDate,
                time: time,
                description: description,
                url: url
            });
        });

        return shows;
    }

    // Loop through all dates
    for (let i = 0; i < totalDates; i++) {
        console.log(\`Scraping date \${i + 1}/\${totalDates}...\`);

        // Select the date
        dateSelect.selectedIndex = i;

        // Trigger change event to load new data
        const changeEvent = new Event('change', { bubbles: true });
        dateSelect.dispatchEvent(changeEvent);

        // Wait for content to update (1 second)
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Scrape shows from this date
        const dateShows = scrapeCurrentPage();
        allShows.push(...dateShows);

        console.log(\`  Found \${dateShows.length} shows\`);
    }

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

    console.log(\`Total shows scraped: \${allShows.length}\`);
    console.log(\`Unique shows: \${uniqueShows.length}\`);

    return JSON.stringify({
        shows: uniqueShows,
        lastUpdated: new Date().toISOString(),
        venue: 'Comedy Cellar',
        totalShows: uniqueShows.length,
        datesScraped: totalDates
    }, null, 2);
})();
" > comedy-cellar-shows.json

agent-browser close

echo "✅ Scraping complete!"
echo "📝 Results saved to comedy-cellar-shows.json"
echo ""
echo "📋 Summary:"
python3 -c "
import json
try:
    with open('comedy-cellar-shows.json', 'r') as f:
        content = f.read().strip()
        # Handle JSON-as-string from agent-browser
        if content.startswith('\"') and content.endswith('\"'):
            content = json.loads(content)
        data = json.loads(content)
        print(f'Total shows: {data.get(\"totalShows\", 0)}')
        print(f'Dates scraped: {data.get(\"datesScraped\", \"N/A\")}')
        print(f'Last updated: {data.get(\"lastUpdated\", \"N/A\")}')

        # Count by date
        from collections import Counter
        dates = Counter()
        for show in data.get('shows', []):
            date = show.get('date', '')[:10]
            if date:
                dates[date] += 1

        print(f'\\nShows across {len(dates)} unique dates')
        print('\\nSample shows:')
        for show in data.get('shows', [])[:5]:
            print(f'  • {show[\"title\"][:50]}')
            print(f'    Venue: {show[\"venue\"]}, Time: {show[\"time\"]}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
