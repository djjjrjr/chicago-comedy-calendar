#!/bin/bash
# Run all LA scrapers and merge results

echo "🚀 Starting LA comedy show scraper pipeline..."
echo ""

# Change to scrapers/la directory
cd scrapers/la || exit 1

echo "1️⃣ Scraping DoLA category..."
python3 scrape-category.py > /dev/null 2>&1
# Rename to la-shows-dola.json so it doesn't get overwritten by merger
if [ -f "la-shows.json" ]; then
    mv la-shows.json la-shows-dola.json
fi
echo "   ✓ DoLA complete"

echo "2️⃣ Scraping UCB Theatre LA..."
python3 scrape-ucb-la.py > /dev/null 2>&1
echo "   ✓ UCB LA complete"

echo "3️⃣ Scraping Largo at the Coronet..."
./scrape-largo.sh > /dev/null 2>&1
echo "   ✓ Largo complete"

echo "4️⃣ Scraping The Comedy Store..."
python3 scrape-comedy-store.py > /dev/null 2>&1
echo "   ✓ The Comedy Store complete"

echo ""
echo "🔄 Merging all LA shows..."
python3 merge-la-shows.py

# Move output to root
if [ -f "la-shows.json" ]; then
    mv la-shows.json ../../
    echo "📦 Moved la-shows.json to root"
fi

echo ""
echo "✅ LA scraper pipeline complete!"
