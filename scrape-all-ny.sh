#!/bin/bash
# Run all NY scrapers and merge results

echo "🚀 Starting NY comedy show scraper pipeline..."
echo ""

# Change to scrapers/ny directory
cd scrapers/ny || exit 1

# Run all scrapers
echo "1️⃣ Scraping Caveat..."
./scrape-caveat.sh > /dev/null 2>&1
echo "   ✓ Caveat complete"

echo "2️⃣ Scraping Union Hall..."
./scrape-union-hall.sh > /dev/null 2>&1
echo "   ✓ Union Hall complete"

echo "3️⃣ Scraping Comedy Cellar..."
./scrape-comedy-cellar.sh > /dev/null 2>&1
echo "   ✓ Comedy Cellar complete"

echo "4️⃣ Scraping The Stand..."
./scrape-the-stand.sh > /dev/null 2>&1
echo "   ✓ The Stand complete"

echo "5️⃣ Scraping UCB Theatre NY..."
python3 scrape-ucb-ny.py > /dev/null 2>&1
echo "   ✓ UCB NY complete"

echo "6️⃣ Scraping The Bell House..."
./scrape-bell-house.sh > /dev/null 2>&1
echo "   ✓ The Bell House complete"

echo ""
echo "🔄 Merging all NY shows..."
python3 merge-ny-shows.py

# Move output to root
if [ -f "ny-shows.json" ]; then
    mv ny-shows.json ../../
    echo "📦 Moved ny-shows.json to root"
fi

echo ""
echo "✅ NY scraper pipeline complete!"
