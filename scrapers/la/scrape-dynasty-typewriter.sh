#!/bin/bash
# Scrape Dynasty Typewriter using agent-browser

echo "🎭 Starting Dynasty Typewriter scraper..."

cd "$(dirname "$0")"

# Open the calendar page
agent-browser open "https://www.dynastytypewriter.com/calendar-squad-up" > /dev/null 2>&1

# Wait for page to load
sleep 3

# Scroll to load more events
agent-browser eval "window.scrollTo(0, document.body.scrollHeight)" > /dev/null 2>&1
sleep 2

# Extract events using JavaScript
agent-browser eval 'JSON.stringify({
  shows: Array.from(document.querySelectorAll("[class*=\"eventlist-event\"], [data-item-id]")).map(item => {
    const titleEl = item.querySelector("[class*=\"eventlist-title\"], h1, h2, h3");
    if (!titleEl) return null;

    const dateEl = item.querySelector("[class*=\"eventlist-datetag\"], [class*=\"event-date\"]");
    const timeEl = item.querySelector("[class*=\"eventlist-time\"], [class*=\"event-time\"]");
    const linkEl = item.querySelector("a[href]");
    const excerptEl = item.querySelector("[class*=\"excerpt\"], [class*=\"description\"], p");

    const dateText = dateEl ? dateEl.textContent.trim() : "";
    const timeText = timeEl ? timeEl.textContent.trim() : "";

    // Parse date (e.g., "Mar 19")
    let isoDate = "";
    if (dateText) {
      const match = dateText.match(/([A-Za-z]{3})\s+(\d+)/);
      if (match) {
        const monthMap = {Jan:1,Feb:2,Mar:3,Apr:4,May:5,Jun:6,Jul:7,Aug:8,Sep:9,Oct:10,Nov:11,Dec:12};
        const month = monthMap[match[1]] || 3;
        const day = match[2];
        const year = 2026;
        isoDate = new Date(year, month-1, day).toISOString();
      }
    }

    return {
      title: titleEl.textContent.trim(),
      venue: "Dynasty Typewriter",
      date: isoDate || new Date().toISOString(),
      time: timeText,
      description: excerptEl ? excerptEl.textContent.trim().substring(0, 200) : "",
      url: linkEl && linkEl.href ? linkEl.href : "https://www.dynastytypewriter.com/calendar-squad-up"
    };
  }).filter(e => e !== null),
  lastUpdated: new Date().toISOString(),
  venue: "Dynasty Typewriter"
})' > dynasty-typewriter-shows-temp.json 2>/dev/null

# Close browser
agent-browser close > /dev/null 2>&1

# Check if we got data
if [ -f "dynasty-typewriter-shows-temp.json" ]; then
    # Parse and format the JSON (handle potential JSON-in-string encoding)
    python3 << 'EOF'
import json
import sys

try:
    with open('dynasty-typewriter-shows-temp.json', 'r') as f:
        content = f.read().strip()

    # Handle JSON wrapped in quotes (from agent-browser eval)
    if content.startswith('"') and content.endswith('"'):
        content = json.loads(content)  # Unescape

    data = json.loads(content)
    shows = data.get('shows', [])

    # Deduplicate
    seen = set()
    unique_shows = []
    for show in shows:
        key = (show.get('title', ''), show.get('date', '')[:10])
        if key not in seen and show.get('title'):
            seen.add(key)
            unique_shows.append(show)

    output = {
        'shows': unique_shows,
        'lastUpdated': data.get('lastUpdated', ''),
        'venue': 'Dynasty Typewriter',
        'totalShows': len(unique_shows)
    }

    with open('dynasty-typewriter-shows.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Extracted {len(unique_shows)} unique shows")
    print(f"📝 Saved to dynasty-typewriter-shows.json")

    if unique_shows:
        print("\n📋 Sample shows:")
        for show in unique_shows[:5]:
            print(f"  • {show['title']}")
            print(f"    {show.get('time', 'TBA')}")

except Exception as e:
    print(f"❌ Error processing data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

    # Clean up temp file
    rm -f dynasty-typewriter-shows-temp.json
else
    echo "❌ Failed to extract data"
    exit 1
fi
