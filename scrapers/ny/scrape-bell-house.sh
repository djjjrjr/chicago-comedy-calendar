#!/bin/bash
# Scrape The Bell House events from DoNYC venue page
# DoNYC requires JavaScript to load events, so we use agent-browser

echo "🎭 Starting The Bell House scraper..."
echo "📍 Navigating to DoNYC venue page..."

# Open the DoNYC venue page
agent-browser open "https://donyc.com/venues/the-bell-house" > /dev/null 2>&1

# Wait for page and JavaScript to load
sleep 6

echo "📊 Extracting event data..."

# Extract events using JavaScript evaluation and save to temp file
agent-browser eval "
const events = [];
const bodyText = document.body.innerText;
const lines = bodyText.split('\n').map(l => l.trim()).filter(l => l);

// DoNYC format pattern:
// TODAY MAR 18 (or FRIDAY MAR 20, etc.)
// Event Title
// THE BELL HOUSE
// . 27 (rating indicator)
// BUY

let i = 0;
while (i < lines.length) {
    const line = lines[i];

    // Look for date header pattern: \"TODAY MAR 18\" or \"FRIDAY MAR 20\"
    const dateMatch = line.match(/^(TODAY|TOMORROW|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)\\s+([A-Z]{3})\\s+(\\d{1,2})$/i);

    if (dateMatch) {
        const dayOfWeek = dateMatch[1];
        const month = dateMatch[2];
        const day = dateMatch[3];

        // Next line should be the event title
        const title = lines[i + 1];

        // Verify the title is reasonable (not BUY, not venue name, not SOLD OUT, etc.)
        if (title &&
            title.length > 3 &&
            !title.match(/^(BUY|SOLD OUT|THE BELL HOUSE|GOOGLE MAPS|\\.|UPCOMING)/i) &&
            title !== month + ' ' + day) {

            // Parse the date
            const currentYear = new Date().getFullYear();
            const dateStr = month + ' ' + day + ', ' + currentYear;
            let dateObj = new Date(dateStr);

            // If date is in the past, assume next year
            const now = new Date();
            if (dateObj < now && (now - dateObj) > 86400000) { // more than 1 day in past
                dateObj = new Date(month + ' ' + day + ', ' + (currentYear + 1));
            }

            // Look for time in nearby lines
            let time = null;
            for (let j = i + 1; j < Math.min(i + 6, lines.length); j++) {
                const timeMatch = lines[j].match(/\\b(\\d{1,2}:\\d{2}\\s*[AP]M)\\b/i);
                if (timeMatch) {
                    time = timeMatch[1].toUpperCase();
                    break;
                }
            }

            // Try to find the event URL by looking for links with the title
            let url = 'https://donyc.com/venues/the-bell-house';
            const links = Array.from(document.querySelectorAll('a'));
            const titleLink = links.find(a => a.textContent.trim() === title);
            if (titleLink && titleLink.href.includes('/events/')) {
                url = titleLink.href;
            }

            events.push({
                title: title,
                venue: 'The Bell House',
                date: dateObj.toISOString(),
                time: time,
                description: null,
                url: url
            });
        }
    }

    i++;
}

// Output JSON
JSON.stringify({
    shows: events,
    lastUpdated: new Date().toISOString(),
    venue: 'The Bell House',
    totalShows: events.length
}, null, 2);
" > bell-house-shows-raw.txt

# Parse and clean the JSON output using Python
python3 << 'PARSE_SCRIPT'
import json

# Read the raw output from agent-browser
with open('bell-house-shows-raw.txt', 'r') as f:
    content = f.read().strip()

# The output might be double-encoded as a JSON string
try:
    # Try parsing as-is first
    data = json.loads(content)
except:
    # If that fails, try double-parsing
    data = json.loads(json.loads(content))

# Write the properly formatted JSON
with open('bell-house-shows.json', 'w') as f:
    json.dump(data, f, indent=2)

# Clean up temp file
import os
os.remove('bell-house-shows-raw.txt')

PARSE_SCRIPT

# Close browser
agent-browser close > /dev/null 2>&1

echo "✅ Scraping complete!"
echo "📝 Results saved to bell-house-shows.json"
echo ""
echo "📋 Summary:"

# Display summary using Python
python3 << 'SUMMARY_SCRIPT'
import json
import sys

try:
    with open('bell-house-shows.json', 'r') as f:
        content = f.read()

    # The output from agent-browser eval may be a JSON-encoded string
    # Try to parse it directly first, then try double-parsing if needed
    try:
        data = json.loads(content)
    except:
        # If that fails, it might be double-encoded
        data = json.loads(json.loads(content))

    # Also handle if it's already a dict
    if isinstance(data, str):
        data = json.loads(data)

    total = data.get('totalShows', 0)
    print(f"Total shows: {total}")
    print(f"Last updated: {data.get('lastUpdated', 'N/A')}")

    if total > 0:
        print("\nSample shows:")
        for show in data.get('shows', [])[:5]:
            print(f"  • {show['title'][:60]}")
            date_part = show.get('date', '')[:10] if show.get('date') else 'N/A'
            time_part = show.get('time') or 'TBD'
            print(f"    {date_part} at {time_part}")
    else:
        print("\n⚠️  Warning: No shows found!")
        sys.exit(1)

except FileNotFoundError:
    print("❌ Error: Output file not created")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"❌ Error: Invalid JSON in output file: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

SUMMARY_SCRIPT
