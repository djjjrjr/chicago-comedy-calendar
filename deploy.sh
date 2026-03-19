#!/bin/bash
# Deploy script - Run all scrapers and update data

echo "🚀 Starting full deployment..."
echo ""

# Chicago
echo "=== CHICAGO ==="
cd scrapers/chicago
./scrape-all.sh
cd ../..
echo ""

# New York
echo "=== NEW YORK ==="
cd scrapers/ny
./scrape-all-ny.sh
cd ../..
echo ""

# Los Angeles
echo "=== LOS ANGELES ==="
cd scrapers/la
./scrape-all-la.sh
cd ../..
echo ""

# Show final counts
echo "📊 Final Show Counts:"
python3 << 'PYEOF'
import json

try:
    chi = json.load(open('data/chicago/shows.json'))
    ny = json.load(open('data/ny/ny-shows.json'))
    la = json.load(open('data/la/la-shows.json'))

    chi_count = len(chi['shows'])
    ny_count = len(ny['shows'])
    la_count = len(la['shows'])

    print(f"  Chicago: {chi_count} shows")
    print(f"  New York: {ny_count} shows")
    print(f"  Los Angeles: {la_count} shows")
    print(f"  ───────────────────")
    print(f"  Total: {chi_count + ny_count + la_count} shows")
except Exception as e:
    print(f"  Error reading data: {e}")
PYEOF

echo ""
echo "✅ Deployment complete!"
echo "🌐 Open public/{city}/index.html to view sites"
