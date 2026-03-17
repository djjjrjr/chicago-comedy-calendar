#!/usr/bin/env python3
"""
Venue Information Scraper
Automatically collects venue details for all venues found in event data
Runs weekly to build/update a comprehensive venue database
"""

import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

def load_existing_venue_info():
    """Load existing venue info to avoid re-scraping"""
    try:
        with open('venue-info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'lastUpdated': None,
            'venues': {}
        }

def get_all_venue_names():
    """Extract unique venue names from all show data files"""
    venues = set()

    # Load from all city show files
    for filename in ['shows.json', 'ny-shows.json', 'la-shows.json']:
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for show in data.get('shows', []):
                    venue_name = show.get('venue', '').strip()
                    if venue_name:
                        venues.add(venue_name)
        except FileNotFoundError:
            print(f"⚠️  {filename} not found, skipping")

    return sorted(list(venues))

def scrape_venue_from_do_site(page, venue_name, base_url, site_name):
    """Scrape venue information from Do312/DoNYC/DoLA venue page"""

    # Create URL-friendly slug from venue name
    slug = venue_name.lower()
    slug = slug.replace('&', 'and')
    slug = slug.replace(' ', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    slug = '-'.join(filter(None, slug.split('-')))  # Remove duplicate hyphens

    venue_url = f"{base_url}/venues/{slug}"

    try:
        print(f"  Checking {venue_url}")
        response = page.goto(venue_url, wait_until='domcontentloaded', timeout=15000)

        if response.status == 404:
            print(f"  ❌ Venue page not found (404)")
            return None

        # Wait for content to load
        time.sleep(2)

        # Extract venue information
        venue_info = page.evaluate('''
            () => {
                const info = {
                    address: '',
                    phone: '',
                    website: '',
                    found: false
                };

                // Find address - link that contains a street address (with "Street", "Avenue", etc.)
                const addressLink = Array.from(document.querySelectorAll('a')).find(a => {
                    const text = a.textContent.trim();
                    return (text.includes('Street') || text.includes('Avenue') || text.includes('Boulevard') ||
                            text.includes('Road') || text.includes('Drive') || text.includes('Lane')) &&
                           /\d+/.test(text); // Contains a number
                });
                if (addressLink) {
                    info.address = addressLink.textContent.trim();
                    info.found = true;
                }

                // Find phone - link with tel: protocol
                const phoneLink = document.querySelector('a[href^="tel:"]');
                if (phoneLink) {
                    info.phone = phoneLink.textContent.trim();
                    info.found = true;
                }

                // Find website - link with text "Official Website"
                const websiteLink = Array.from(document.querySelectorAll('a')).find(a =>
                    a.textContent.includes('Official Website') || a.textContent.includes('Website')
                );
                if (websiteLink && websiteLink.href &&
                    !websiteLink.href.includes('do312') &&
                    !websiteLink.href.includes('donyc') &&
                    !websiteLink.href.includes('dolosangeles')) {
                    info.website = websiteLink.href;
                    info.found = true;
                }

                return info;
            }
        ''')

        if venue_info.get('found'):
            print(f"  ✓ Found venue info")
            return {
                'name': venue_name,
                'address': venue_info.get('address', ''),
                'phone': venue_info.get('phone', ''),
                'website': venue_info.get('website', ''),
                'lastUpdated': datetime.now().isoformat(),
                'source': site_name
            }
        else:
            print(f"  ⚠️  Page loaded but no venue info found")
            return None

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return None

def determine_city_for_venue(venue_name):
    """Determine which city a venue belongs to based on show data"""

    # Check each city's show file
    city_mapping = {
        'shows.json': ('chicago', 'https://do312.com', 'Do312'),
        'ny-shows.json': ('new-york', 'https://donyc.com', 'DoNYC'),
        'la-shows.json': ('los-angeles', 'https://dolosangeles.com', 'DoLA')
    }

    for filename, (city, base_url, site_name) in city_mapping.items():
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                venues_in_file = [show.get('venue', '') for show in data.get('shows', [])]
                if venue_name in venues_in_file:
                    return city, base_url, site_name
        except FileNotFoundError:
            continue

    return None, None, None

def main():
    print("🎭 Venue Information Scraper Starting...")
    print("=" * 60)

    # Load existing venue info
    venue_data = load_existing_venue_info()
    existing_venues = venue_data.get('venues', {})

    # Get all unique venue names from show data
    all_venues = get_all_venue_names()
    print(f"\n📊 Found {len(all_venues)} unique venues across all cities")
    print(f"📚 Already have info for {len(existing_venues)} venues")

    # Determine which venues need scraping
    venues_to_scrape = [v for v in all_venues if v not in existing_venues]
    print(f"🔍 Need to scrape {len(venues_to_scrape)} new venues")

    if not venues_to_scrape:
        print("\n✓ All venues already have information!")
        return

    print(f"\n🌐 Starting browser to scrape venue information...")

    scraped_count = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for venue_name in venues_to_scrape:
            print(f"\n📍 Scraping: {venue_name}")

            # Determine which city/site to scrape from
            city, base_url, site_name = determine_city_for_venue(venue_name)

            if not city:
                print(f"  ⚠️  Could not determine city for venue")
                continue

            print(f"  City: {city} ({site_name})")

            # Scrape venue info
            venue_info = scrape_venue_from_do_site(page, venue_name, base_url, site_name)

            if venue_info:
                existing_venues[venue_name] = venue_info
                scraped_count += 1

            # Rate limiting
            time.sleep(2)

        browser.close()

    print("\n" + "=" * 60)
    print(f"✓ Scraping complete!")
    print(f"  New venues scraped: {scraped_count}")
    print(f"  Total venues in database: {len(existing_venues)}")

    # Save updated venue info
    venue_data['venues'] = existing_venues
    venue_data['lastUpdated'] = datetime.now().isoformat()

    with open('venue-info.json', 'w') as f:
        json.dump(venue_data, f, indent=2)

    print(f"\n💾 Saved to venue-info.json")

if __name__ == '__main__':
    main()
