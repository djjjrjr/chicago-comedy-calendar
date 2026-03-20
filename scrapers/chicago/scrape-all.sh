#!/bin/bash
# Master script to scrape all Chicago comedy shows

cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

echo "🎭 Starting Chicago comedy scraper..."
echo ""

# Scrape comedy category (now uses date-based scraping to fix broken pagination)
echo "📋 Scraping Do312 comedy by date..."
python3 scrape-category.py
if [ $? -eq 0 ]; then
    echo "✅ Date-based scraping complete"
else
    echo "⚠️  Date-based scraping failed"
fi
echo ""

# Scrape venue pages for all preferred venues
echo "📍 Scraping Do312 venue pages..."
python3 scrape-do312-venues.py
if [ $? -eq 0 ]; then
    echo "✅ Venue page scraping complete"
else
    echo "⚠️  Venue page scraping failed"
fi
echo ""

# Merge all sources
echo "🔄 Merging all sources..."
python3 merge-chicago-shows.py
if [ $? -eq 0 ]; then
    echo "✅ Merge complete"
else
    echo "⚠️  Merge failed"
fi
echo ""

# Move final output to root (where GitHub Pages serves from)
if [ -f "shows.json" ]; then
    mv shows.json ../../
    echo "📦 Moved shows.json to root"
fi

if [ -f "do312-venues-shows.json" ]; then
    mv do312-venues-shows.json ../../
fi

echo ""
echo "✅ Chicago scraping complete!"
echo "📊 Final data: ../../shows.json"
