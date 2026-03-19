#!/usr/bin/env python3
"""
Scraper for Den Theatre (Chicago)
Extracts comedy shows from thedentheatre.com
"""

import json
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_den_theatre():
    """Scrape shows from Den Theatre website."""
    shows = []

    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Start with the performances page
    base_url = "https://thedentheatre.com"
    url = f"{base_url}/performances"

    print(f"Loading {url}...")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all show articles
        articles = soup.find_all('article')
        print(f"Found {len(articles)} articles")

        for article in articles:
            try:
                # Find the title - it's in BlogList-item-title class
                title_elem = article.find('a', class_='BlogList-item-title')
                if not title_elem:
                    continue

                title_text = title_elem.get_text().strip()
                show_url = title_elem.get('href', '')

                # Make URL absolute
                if show_url and not show_url.startswith('http'):
                    show_url = f"{base_url}{show_url}"

                # Find date - it's in BlogList-item-excerpt div
                excerpt_div = article.find('div', class_='BlogList-item-excerpt')
                date_text = ""
                if excerpt_div:
                    date_para = excerpt_div.find('p')
                    if date_para:
                        date_link = date_para.find('a')
                        if date_link:
                            date_text = date_link.get_text().strip()
                            # Remove "LIMITED TICKETS LEFT" if present
                            date_text = re.sub(r'\s*\|\s*LIMITED TICKETS LEFT', '', date_text, flags=re.IGNORECASE)
                            date_text = re.sub(r'\s*LIMITED TICKETS LEFT', '', date_text, flags=re.IGNORECASE)
                            date_text = date_text.strip()

                # Find stage/venue info from location span or link
                stage_elem = article.find('span', class_='BlogList-item-location')
                stage = stage_elem.get_text().strip() if stage_elem else ""

                # Also check article classes for stage info
                if not stage:
                    article_classes = article.get('class', [])
                    for cls in article_classes:
                        if 'heath-mainstage' in cls:
                            stage = "Heath Mainstage"
                            break
                        elif 'theatre-2a' in cls or '2a' in cls:
                            stage = "Theatre 2A"
                            break
                        elif 'crosby' in cls:
                            stage = "The Crosby"
                            break

                # Parse dates
                parsed_dates = parse_date_range(date_text)

                # Create show entry for each parsed date
                if parsed_dates:
                    for show_date in parsed_dates:
                        show = {
                            "title": title_text,
                            "venue": "Den Theatre",
                            "date": show_date,
                            "time": "",
                            "description": f"{title_text} at {stage}" if stage else title_text,
                            "url": show_url or ""
                        }
                        shows.append(show)
                else:
                    # If we can't parse dates, still add the show with raw date
                    show = {
                        "title": title_text,
                        "venue": "Den Theatre",
                        "date": date_text,
                        "time": "",
                        "description": f"{title_text} at {stage}" if stage else title_text,
                        "url": show_url or ""
                    }
                    shows.append(show)

            except Exception as e:
                print(f"Error extracting show: {e}")
                continue

        # Try to scrape additional pages
        # Look for pagination links
        page_num = 2
        max_pages = 5  # Limit pagination

        while page_num <= max_pages:
            # Check if there's an "Older" link or page numbers
            next_page_link = soup.find('a', string=re.compile(r'Older|Next', re.IGNORECASE))

            if next_page_link:
                next_url = next_page_link.get('href', '')
                if next_url and not next_url.startswith('http'):
                    next_url = f"{base_url}{next_url}"

                print(f"Loading page {page_num}: {next_url}")

                try:
                    response = requests.get(next_url, headers=headers, timeout=30)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')

                    articles = soup.find_all('article')
                    print(f"Found {len(articles)} articles on page {page_num}")

                    # Process articles same as before
                    for article in articles:
                        try:
                            title_elem = article.find('a', class_='BlogList-item-title')
                            if not title_elem:
                                continue

                            title_text = title_elem.get_text().strip()
                            show_url = title_elem.get('href', '')

                            if show_url and not show_url.startswith('http'):
                                show_url = f"{base_url}{show_url}"

                            excerpt_div = article.find('div', class_='BlogList-item-excerpt')
                            date_text = ""
                            if excerpt_div:
                                date_para = excerpt_div.find('p')
                                if date_para:
                                    date_link = date_para.find('a')
                                    if date_link:
                                        date_text = date_link.get_text().strip()
                                        date_text = re.sub(r'\s*\|\s*LIMITED TICKETS LEFT', '', date_text, flags=re.IGNORECASE)
                                        date_text = re.sub(r'\s*LIMITED TICKETS LEFT', '', date_text, flags=re.IGNORECASE)
                                        date_text = date_text.strip()

                            stage_elem = article.find('span', class_='BlogList-item-location')
                            stage = stage_elem.get_text().strip() if stage_elem else ""

                            if not stage:
                                article_classes = article.get('class', [])
                                for cls in article_classes:
                                    if 'heath-mainstage' in cls:
                                        stage = "Heath Mainstage"
                                        break
                                    elif 'theatre-2a' in cls or '2a' in cls:
                                        stage = "Theatre 2A"
                                        break
                                    elif 'crosby' in cls:
                                        stage = "The Crosby"
                                        break

                            parsed_dates = parse_date_range(date_text)

                            if parsed_dates:
                                for show_date in parsed_dates:
                                    show = {
                                        "title": title_text,
                                        "venue": "Den Theatre",
                                        "date": show_date,
                                        "time": "",
                                        "description": f"{title_text} at {stage}" if stage else title_text,
                                        "url": show_url or ""
                                    }
                                    shows.append(show)
                            else:
                                show = {
                                    "title": title_text,
                                    "venue": "Den Theatre",
                                    "date": date_text,
                                    "time": "",
                                    "description": f"{title_text} at {stage}" if stage else title_text,
                                    "url": show_url or ""
                                }
                                shows.append(show)

                        except Exception as e:
                            print(f"Error extracting show: {e}")
                            continue

                    page_num += 1

                except Exception as e:
                    print(f"Error loading page {page_num}: {e}")
                    break
            else:
                print("No more pagination links found")
                break

    except Exception as e:
        print(f"Error loading page: {e}")
        return shows

    return shows


def parse_date_range(date_text):
    """
    Parse date strings like:
    - "March 20"
    - "March 20-28"
    - "April 3-6"
    - "March 26-28"
    - "March 20 - April 5"
    Returns list of dates in YYYY-MM-DD format
    """
    dates = []

    # Current year (2026)
    current_year = 2026

    # Month mapping
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    if not date_text:
        return dates

    date_text = date_text.lower().strip()

    # Clean up unicode spaces
    date_text = re.sub(r'\s+', ' ', date_text)

    # Pattern 1: "March 20" or "April 3" (single date)
    single_match = re.match(r'^(\w+)\s+(\d+)$', date_text)
    if single_match:
        month_name = single_match.group(1)
        day = int(single_match.group(2))
        month = months.get(month_name)
        if month:
            dates.append(f"{current_year}-{month:02d}-{day:02d}")
        return dates

    # Pattern 2: "March 20-28" or "April 3-6" (same month range)
    range_match = re.match(r'^(\w+)\s+(\d+)-(\d+)$', date_text)
    if range_match:
        month_name = range_match.group(1)
        start_day = int(range_match.group(2))
        end_day = int(range_match.group(3))
        month = months.get(month_name)

        if month:
            # Add all dates in range
            for day in range(start_day, end_day + 1):
                try:
                    dates.append(f"{current_year}-{month:02d}-{day:02d}")
                except ValueError:
                    continue
        return dates

    # Pattern 3: "March 20 - April 5" (cross-month range)
    cross_month_match = re.match(r'^(\w+)\s+(\d+)\s*-\s*(\w+)\s+(\d+)$', date_text)
    if cross_month_match:
        start_month_name = cross_month_match.group(1)
        start_day = int(cross_month_match.group(2))
        end_month_name = cross_month_match.group(3)
        end_day = int(cross_month_match.group(4))

        start_month = months.get(start_month_name)
        end_month = months.get(end_month_name)

        if start_month and end_month:
            # Generate all dates in range
            from datetime import date, timedelta

            start_date = date(current_year, start_month, start_day)
            end_date = date(current_year, end_month, end_day)

            current_date = start_date
            while current_date <= end_date:
                dates.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)

        return dates

    return dates


def main():
    print("Starting Den Theatre scraper...")
    print("=" * 60)

    shows = scrape_den_theatre()

    print("=" * 60)
    print(f"Total shows extracted: {len(shows)}")

    # Remove duplicates based on title and date
    unique_shows = []
    seen = set()
    for show in shows:
        key = (show['title'], show['date'])
        if key not in seen:
            seen.add(key)
            unique_shows.append(show)

    print(f"Unique shows after deduplication: {len(unique_shows)}")

    # Sort by date
    try:
        unique_shows.sort(key=lambda x: x['date'] if x['date'] and re.match(r'\d{4}-\d{2}-\d{2}', x['date']) else '9999-99-99')
    except:
        pass

    # Save to JSON
    output_file = "/workspace/group/chicago-comedy-calendar/den-theatre-shows.json"
    with open(output_file, 'w') as f:
        json.dump(unique_shows, f, indent=2)

    print(f"\nSaved to {output_file}")
    print("\nSample shows:")
    for show in unique_shows[:10]:
        print(f"  - {show['date']}: {show['title']}")

    return len(unique_shows)


if __name__ == "__main__":
    count = main()
    print(f"\n✓ Successfully scraped {count} shows from Den Theatre")
