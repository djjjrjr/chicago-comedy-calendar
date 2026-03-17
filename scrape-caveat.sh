#!/bin/bash
# Scrape Caveat events using agent-browser

echo "🎭 Starting Caveat scraper..."
echo "📍 Navigating to Caveat events page..."

agent-browser open https://caveat.nyc/events
sleep 3

echo "🔄 Loading all events..."
agent-browser click "button:has-text('SHOW ALL')"
sleep 2

echo "📊 Extracting event data..."
agent-browser eval "
const cards = Array.from(document.querySelectorAll('.MuiCard-root'));
const events = [];

cards.forEach(card => {
    const allText = Array.from(card.querySelectorAll('[class*=\"MuiTypography\"]')).map(t => t.textContent.trim());
    const url = card.querySelector('a')?.href || '';

    if (allText.length >= 3) {
        // Parse date (e.g., 'TUE, MAR 17')
        const dateStr = allText[0];
        const currentYear = new Date().getFullYear();
        const dateParts = dateStr.split(', ');
        let isoDate = new Date().toISOString();

        if (dateParts.length === 2) {
            try {
                const monthDay = dateParts[1];
                const dateObj = new Date(monthDay + ' ' + currentYear);
                // If date is in past, assume next year
                if (dateObj < new Date()) {
                    dateObj.setFullYear(currentYear + 1);
                }
                isoDate = dateObj.toISOString();
            } catch (e) {
                // Use current date if parsing fails
            }
        }

        events.push({
            title: allText[2],
            venue: 'Caveat',
            date: isoDate,
            time: allText[1] || null,
            description: allText[4] || null,
            url: url || null
        });
    }
});

JSON.stringify({
    shows: events,
    lastUpdated: new Date().toISOString(),
    venue: 'Caveat',
    totalShows: events.length
}, null, 2);
" > caveat-shows.json

agent-browser close

echo "✅ Scraping complete!"
echo "📝 Results saved to caveat-shows.json"
echo ""
echo "📋 Summary:"
jq -r '"Total shows: \(.totalShows)\nLast updated: \(.lastUpdated)\n\nSample shows:"' caveat-shows.json
jq -r '.shows[:3] | .[] | "  • \(.title)\n    Date: \(.date), Time: \(.time)"' caveat-shows.json
