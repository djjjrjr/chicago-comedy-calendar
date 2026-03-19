#!/usr/bin/env python3
"""
Scrape Union Hall events from their Eventbrite organizer page.
This captures all available events instead of just the 16 shown on their website.
"""

import subprocess
import json
import re
from datetime import datetime

# Union Hall's Eventbrite organizer ID
ORGANIZER_URL = "https://www.eventbrite.com/o/union-hall-17899496497"

def scrape_eventbrite_organizer():
    """Use agent-browser to scrape all events from Union Hall's Eventbrite organizer page."""

    print("🎭 Starting Union Hall Eventbrite scraper...")
    print(f"📍 Opening organizer page: {ORGANIZER_URL}")

    # Open the organizer page
    subprocess.run(["agent-browser", "open", ORGANIZER_URL], check=True)
    subprocess.run(["sleep", "4"], check=True)

    print("📊 Scrolling to load all events...")

    # First scroll to load all events
    for i in range(15):
        subprocess.run(["agent-browser", "eval", "window.scrollTo(0, document.body.scrollHeight); 'scrolled'"],
                      capture_output=True, check=False)
        subprocess.run(["sleep", "2"], check=True)

    print("📊 Extracting all event data...")

    # JavaScript to extract all events from the page
    js_code = '''
const events = [];
const eventCards = document.querySelectorAll('[data-testid="organizer-profile__event-card"], article, div[class*="event-card"], a[href*="/e/"]');

console.log('Found potential event cards:', eventCards.length);

// Get unique event links
const eventLinks = new Set();
document.querySelectorAll('a[href*="/e/"]').forEach(link => {
  const href = link.href;
  if (href.includes('/e/') && href.includes('tickets')) {
    eventLinks.add(href.split('?')[0]); // Remove query params
  }
});

console.log('Found unique event links:', eventLinks.size);

// Extract event details from the page
const eventElements = document.querySelectorAll('[class*="event"], article');
const pageText = document.body.innerText;

// Try to parse visible event cards
const eventSections = document.querySelectorAll('div[class*="Card"], div[class*="card"], li[class*="event"]');

for (const section of eventSections) {
  const text = section.innerText || section.textContent;
  if (!text || text.length < 10) continue;

  // Look for event title and date patterns
  const lines = text.split('\\n').filter(l => l.trim());

  // Find links within this section
  const link = section.querySelector('a[href*="/e/"]');
  if (!link) continue;

  const url = link.href.split('?')[0];

  // Try to find title - usually the first substantial text or link text
  const title = link.textContent.trim() || lines.find(l => l.length > 5 && !l.match(/^(Mon|Tue|Wed|Thu|Fri|Sat|Sun|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\\d{1,2}|PM|AM|•)/i))?.trim();

  if (!title || title.length < 3) continue;

  // Try to find date - look for patterns like "Mar 21", "March 21, 2026", etc.
  const dateMatch = text.match(/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\\d{1,2}),? (\\d{4})?/i);
  const timeMatch = text.match(/(\\d{1,2}:\\d{2} [AP]M)/i);

  let date = null;
  if (dateMatch) {
    const month = dateMatch[1];
    const day = dateMatch[2];
    const year = dateMatch[3] || new Date().getFullYear();
    const time = timeMatch ? timeMatch[1] : '7:00 PM';

    const dateStr = `${month} ${day}, ${year} ${time}`;
    try {
      date = new Date(dateStr).toISOString();
    } catch (e) {
      console.log('Date parse error:', dateStr);
    }
  }

  // Check for duplicates
  if (events.some(e => e.url === url)) continue;

  events.push({
    title: title,
    venue: 'Union Hall',
    date: date,
    time: timeMatch ? timeMatch[1] : null,
    description: null,
    url: url
  });
}

// Fallback: if we didn't get many events, try a simpler extraction
if (events.length < 20) {
  console.log('Using fallback extraction method...');

  const allLinks = document.querySelectorAll('a[href*="/e/"][href*="tickets"]');
  for (const link of allLinks) {
    const url = link.href.split('?')[0];
    if (events.some(e => e.url === url)) continue;

    // Get parent container for context
    const container = link.closest('div[class*="Card"], div[class*="card"], li, article') || link.parentElement;
    const text = container?.innerText || link.innerText;

    const title = link.getAttribute('aria-label') || link.textContent.trim() || text.split('\\n')[0];

    if (title && title.length > 3 && !title.match(/^(View|See|More|Event)/i)) {
      events.push({
        title: title.trim(),
        venue: 'Union Hall',
        date: null,
        time: null,
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
'''

    # Execute the JavaScript and capture output
    result = subprocess.run(
        ["agent-browser", "eval", js_code],
        capture_output=True,
        text=True
    )

    # Close browser
    subprocess.run(["agent-browser", "close"], check=True)

    if result.returncode != 0:
        print(f"❌ Error extracting events: {result.stderr}")
        return None

    # Parse the JSON output
    try:
        # The output might have some extra text, so find the JSON
        output = result.stdout
        # Look for JSON starting with {
        json_start = output.find('{')
        if json_start >= 0:
            json_str = output[json_start:]
            data = json.loads(json_str)
            return data
        else:
            print(f"❌ No JSON found in output")
            return None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        print(f"Output was: {result.stdout[:500]}")
        return None

def main():
    data = scrape_eventbrite_organizer()

    if not data:
        print("❌ Failed to scrape events")
        return 1

    # Save to file
    output_file = "union-hall-shows.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print("✅ Scraping complete!")
    print(f"📝 Results saved to {output_file}")
    print(f"\n📋 Summary:")
    print(f"Total shows: {data['totalShows']}")
    print(f"Last updated: {data['lastUpdated']}")

    if data['shows']:
        print("\nSample shows:")
        for show in data['shows'][:5]:
            title = show['title'][:60]
            date = show['date'][:10] if show['date'] else 'TBD'
            print(f"  • {title}")
            print(f"    Date: {date}")

    return 0

if __name__ == "__main__":
    exit(main())
