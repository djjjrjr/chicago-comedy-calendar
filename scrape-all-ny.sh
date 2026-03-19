#!/bin/bash
# Run all NY scrapers and merge results

echo "🚀 Starting NY comedy show scraper pipeline..."
echo ""

# 1. Caveat (agent-browser)
echo "1️⃣ Scraping Caveat..."
./scrape-caveat.sh > /dev/null 2>&1
echo "   ✓ Caveat complete"

# 2. Union Hall (agent-browser)
echo "2️⃣ Scraping Union Hall..."
./scrape-union-hall.sh > /dev/null 2>&1
echo "   ✓ Union Hall complete"

# 3. Comedy Cellar (agent-browser)
echo "3️⃣ Scraping Comedy Cellar..."
./scrape-comedy-cellar.sh > /dev/null 2>&1
echo "   ✓ Comedy Cellar complete"

# 4. The Stand (agent-browser)
echo "4️⃣ Scraping The Stand..."
./scrape-the-stand.sh > /dev/null 2>&1
echo "   ✓ The Stand complete"

# 5. UCB NY (cloudscraper)
echo "5️⃣ Scraping UCB Theatre NY..."
python3 scrape-ucb-ny.py > /dev/null 2>&1
echo "   ✓ UCB NY complete"

# 6. The Bell House (agent-browser via DoNYC)
echo "6️⃣ Scraping The Bell House..."
./scrape-bell-house.sh > /dev/null 2>&1
echo "   ✓ The Bell House complete"

# 7. Merge all sources
echo ""
echo "🔄 Merging all NY shows..."
python3 merge-ny-shows.py

echo ""
echo "✅ NY scraper pipeline complete!"
echo "📊 Final data: ny-shows.json"
