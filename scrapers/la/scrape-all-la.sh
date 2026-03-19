#!/bin/bash
# Run all LA scrapers and merge results

echo "🚀 Starting LA comedy show scraper pipeline..."
echo ""

# 1. DoLA category scraper
echo "1️⃣ Scraping DoLA category..."
python3 scrape-category.py > /dev/null 2>&1
# Rename to la-shows-dola.json so it doesn't get overwritten by merger
if [ -f "la-shows.json" ]; then
    mv la-shows.json la-shows-dola.json
fi
echo "   ✓ DoLA complete"

# 2. UCB LA (cloudscraper)
echo "2️⃣ Scraping UCB Theatre LA..."
python3 scrape-ucb-la.py > /dev/null 2>&1
echo "   ✓ UCB LA complete"

# 3. Largo at the Coronet
echo "3️⃣ Scraping Largo at the Coronet..."
./scrape-largo.sh > /dev/null 2>&1
echo "   ✓ Largo complete"

# 4. The Comedy Store
echo "4️⃣ Scraping The Comedy Store..."
python3 scrape-comedy-store.py > /dev/null 2>&1
echo "   ✓ The Comedy Store complete"

# 5. Merge all LA sources
echo ""
echo "🔄 Merging all LA shows..."
python3 merge-la-shows.py

# 6. Move output to data directory
DATA_DIR="../../data/la"
if [ -f "la-shows.json" ]; then
    mv la-shows.json "$DATA_DIR/"
    echo "📦 Moved la-shows.json to $DATA_DIR"
fi

# Move individual venue files too
for file in *-shows.json; do
    if [ -f "$file" ] && [ "$file" != "la-shows.json" ]; then
        mv "$file" "$DATA_DIR/"
    fi
done

echo ""
echo "✅ LA scraper pipeline complete!"
echo "📊 Final data: $DATA_DIR/la-shows.json"
