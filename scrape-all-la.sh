#!/bin/bash
# Run all LA scrapers and merge results

echo "🚀 Starting LA comedy show scraper pipeline..."
echo ""

# 1. DoLA scraper (if available)
if [ -f "la-scraper.py" ]; then
    echo "1️⃣ Scraping DoLA..."
    python3 la-scraper.py > /dev/null 2>&1
    # Rename to la-shows-dola.json so it doesn't get overwritten by merger
    if [ -f "la-shows.json" ]; then
        mv la-shows.json la-shows-dola.json
    fi
    echo "   ✓ DoLA complete"
else
    echo "1️⃣ DoLA scraper not found, skipping..."
fi

# 2. UCB LA (cloudscraper)
echo "2️⃣ Scraping UCB Theatre LA..."
python3 scrape-ucb-la.py > /dev/null 2>&1
echo "   ✓ UCB LA complete"

# 3. Merge all LA sources
echo ""
echo "🔄 Merging all LA shows..."
python3 merge-la-shows.py

echo ""
echo "✅ LA scraper pipeline complete!"
