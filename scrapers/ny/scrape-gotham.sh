#!/bin/bash
# Scrape Gotham Comedy Club events using agent-browser

echo "🎭 Starting Gotham Comedy Club scraper..."
echo "📍 Navigating to Gotham Comedy Club homepage..."

agent-browser open https://gothamcomedyclub.com
sleep 5

echo "🔄 Scrolling to load all events..."
agent-browser scroll down 3
sleep 2
agent-browser scroll down 3
sleep 2

echo "📊 Extracting event data..."
agent-browser eval '
const shows = [];
const allLinks = Array.from(document.querySelectorAll("a"));

// Filter for event links
const eventLinks = allLinks.filter(a => a.href && a.href.includes("/event/"));

console.error("Found event links:", eventLinks.length);

eventLinks.forEach((link, index) => {
  try {
    const text = link.textContent.trim();
    const href = link.href;

    // Split by newlines and filter empty lines
    const parts = text.split("\n")
      .map(s => s.trim())
      .filter(s => s && s !== "GET TICKETS" && s !== "BUY");

    if (parts.length >= 3) {
      const dateStr = parts[0];
      const title = parts[1];
      const time = parts[2];

      // Parse date - format is like "19 March 2026"
      const dateObj = new Date(dateStr);

      if (!isNaN(dateObj.getTime())) {
        shows.push({
          title: title,
          venue: "Gotham Comedy Club",
          date: dateObj.toISOString(),
          time: time,
          description: null,
          url: href
        });
      }
    }
  } catch (e) {
    console.error("Error parsing event:", e.message);
  }
});

console.error("Extracted shows:", shows.length);

JSON.stringify({
  shows: shows,
  lastUpdated: new Date().toISOString(),
  venue: "Gotham Comedy Club",
  totalShows: shows.length
}, null, 2);
' > gotham-shows.json

agent-browser close

echo "✅ Scraping complete!"

# Parse the JSON (might be wrapped in quotes from agent-browser)
if [ -f gotham-shows.json ]; then
  # Check if the file starts with a quote (JSON-as-string)
  if head -c 1 gotham-shows.json | grep -q '"'; then
    echo "🔄 Unwrapping JSON string..."
    python3 << 'PYTHON'
import json
with open('gotham-shows.json', 'r') as f:
    content = f.read().strip()
    # Unescape the JSON string
    if content.startswith('"') and content.endswith('"'):
        content = json.loads(content)
    data = json.loads(content)

with open('gotham-shows.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"📝 Results saved to gotham-shows.json")
print(f"📋 Total shows: {data['totalShows']}")
print(f"📅 Last updated: {data['lastUpdated']}")
print(f"\n🎤 Sample shows:")
for show in data['shows'][:5]:
    print(f"  • {show['title']}")
    print(f"    {show['date'][:10]} at {show['time']}")
PYTHON
  else
    # Already valid JSON
    python3 << 'PYTHON'
import json
with open('gotham-shows.json', 'r') as f:
    data = json.load(f)

print(f"📝 Results saved to gotham-shows.json")
print(f"📋 Total shows: {data['totalShows']}")
print(f"📅 Last updated: {data['lastUpdated']}")
print(f"\n🎤 Sample shows:")
for show in data['shows'][:5]:
    print(f"  • {show['title']}")
    print(f"    {show['date'][:10]} at {show['time']}")
PYTHON
  fi
fi
