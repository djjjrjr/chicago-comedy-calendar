#!/bin/bash
# Run all LA scrapers and merge results

echo "🚀 Starting LA comedy show scraper pipeline..."
echo ""

# 1. DoLA scraper (if available)
if [ -f "la-scraper.py" ]; then
    echo "1️⃣ Scraping DoLA..."
    python3 la-scraper.py > /dev/null 2>&1 && echo "   ✓ DoLA complete" || echo "   ⚠️  DoLA failed (may need Playwright)"
else
    echo "1️⃣ DoLA scraper not found, skipping..."
fi

# 2. UCB LA (cloudscraper)
echo "2️⃣ Scraping UCB Theatre LA..."
python3 scrape-ucb-la.py > /dev/null 2>&1
echo "   ✓ UCB LA complete"

# 3. Merge (if merger exists)
if [ -f "merge-la-shows.py" ]; then
    echo ""
    echo "🔄 Merging all LA shows..."
    python3 merge-la-shows.py
else
    echo ""
    echo "⚠️  LA merger script not created yet"
    echo "   UCB LA data saved to: ucb-la-shows.json"
fi

echo ""
echo "✅ LA scraper pipeline complete!"
