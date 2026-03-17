#!/bin/bash
# Scrape Comedy Cellar events using agent-browser
# Approach: Scrape current day's lineup to test, then can extend to multiple days

echo "🎭 Starting Comedy Cellar scraper..."
echo "📍 Navigating to Comedy Cellar lineup page..."

agent-browser open https://www.comedycellar.com/new-york-line-up/
sleep 3

echo "📊 Extracting show data..."

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

    // Get reservation URL
    const reservationLink = Array.from(document.querySelectorAll('a[href*=\"reservation\"]')).find(a =>
        a.textContent.includes(time) || a.textContent.includes('MAKE A RESERVATION')
    );
    const url = reservationLink ? reservationLink.href : 'https://www.comedycellar.com/new-york-line-up/';

    allShows.push({
        title: title,
        venue: venueName,
        date: isoDate,
        time: time,
        description: description,
        url: url
    });
});

JSON.stringify({
    shows: allShows,
    lastUpdated: new Date().toISOString(),
    venue: 'Comedy Cellar',
    scrapedDate: currentDateText,
    totalShows: allShows.length
}, null, 2);
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
        data = json.load(f)
        print(f'Total shows: {data.get(\"totalShows\", 0)}')
        print(f'Scraped date: {data.get(\"scrapedDate\", \"N/A\")}')
        print(f'Last updated: {data.get(\"lastUpdated\", \"N/A\")}')
        print('\\nSample shows:')
        for show in data.get('shows', [])[:5]:
            print(f'  • {show[\"title\"][:50]}')
            print(f'    Venue: {show[\"venue\"]}, Time: {show[\"time\"]}')
except Exception as e:
    print(f'Error: {e}')
"
