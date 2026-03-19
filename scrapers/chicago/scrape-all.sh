#!/bin/bash
# Master script to scrape all Chicago comedy shows

cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"
DATA_DIR="../../data/chicago"

echo "🎭 Starting Chicago comedy scraper..."
echo ""

# Scrape comedy category
echo "📋 Scraping Do312 comedy category..."
python3 scrape-category.py
if [ $? -eq 0 ]; then
    echo "✅ Category scraping complete"
else
    echo "⚠️  Category scraping failed"
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

# Move final output to data directory
if [ -f "shows.json" ]; then
    mv shows.json "$DATA_DIR/"
    echo "📦 Moved shows.json to $DATA_DIR"
fi

if [ -f "do312-venues-shows.json" ]; then
    mv do312-venues-shows.json "$DATA_DIR/"
fi

echo ""
echo "✅ Chicago scraping complete!"
echo "📊 Final data: $DATA_DIR/shows.json"
