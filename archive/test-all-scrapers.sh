#!/bin/bash
# Comprehensive scraper test - runs all scrapers and generates report

echo "🎬 COMPREHENSIVE SCRAPER TEST"
echo "=============================="
echo ""

# Chicago
echo "📍 CHICAGO SCRAPERS"
echo "-------------------"
echo "Running Chicago scraper..."
python3 scraper-improved.py > /dev/null 2>&1
if [ -f "shows.json" ]; then
    CHICAGO_COUNT=$(python3 -c "import json; print(len(json.load(open('shows.json'))['shows']))")
    echo "✅ Chicago: $CHICAGO_COUNT shows"
else
    echo "❌ Chicago: Failed"
fi
echo ""

# New York
echo "📍 NEW YORK SCRAPERS"
echo "--------------------"

echo "Running Comedy Cellar..."
./scrape-comedy-cellar.sh > /dev/null 2>&1
if [ -f "comedy-cellar-shows.json" ]; then
    CC_COUNT=$(python3 -c "import json; d=json.load(open('comedy-cellar-shows.json')); print(d['totalShows'] if 'totalShows' in d else len(d.get('shows', [])))")
    echo "✅ Comedy Cellar: $CC_COUNT shows"
fi

echo "Running The Stand..."
if [ -f "scrape-stand.py" ]; then
    python3 scrape-stand.py > /dev/null 2>&1
    if [ -f "stand-shows.json" ]; then
        STAND_COUNT=$(python3 -c "import json; d=json.load(open('stand-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
        echo "✅ The Stand: $STAND_COUNT shows"
    fi
fi

echo "Running Gotham Comedy Club..."
python3 scrape-gotham.py > /dev/null 2>&1
if [ -f "gotham-shows.json" ]; then
    GOTHAM_COUNT=$(python3 -c "import json; d=json.load(open('gotham-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
    echo "✅ Gotham: $GOTHAM_COUNT shows"
fi

echo "Running Bell House..."
python3 scrape-bell-house.py > /dev/null 2>&1
if [ -f "bell-house-shows.json" ]; then
    BELL_COUNT=$(python3 -c "import json; d=json.load(open('bell-house-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
    echo "✅ Bell House: $BELL_COUNT shows"
fi

echo "Running Union Hall..."
./scrape-union-hall.sh > /dev/null 2>&1
if [ -f "union-hall-shows.json" ]; then
    UH_COUNT=$(python3 -c "import json; content=open('union-hall-shows.json').read().strip(); content=json.loads(content) if not content.startswith('\"') else json.loads(json.loads(content)); print(content.get('totalShows', len(content.get('shows', []))))")
    echo "✅ Union Hall: $UH_COUNT shows"
fi

echo "Running Caveat..."
./scrape-caveat.sh > /dev/null 2>&1
if [ -f "caveat-shows.json" ]; then
    CAVEAT_COUNT=$(python3 -c "import json; content=open('caveat-shows.json').read().strip(); content=json.loads(content) if not content.startswith('\"') else json.loads(json.loads(content)); print(content.get('totalShows', len(content.get('shows', []))))")
    echo "✅ Caveat: $CAVEAT_COUNT shows"
fi

echo "Running UCB Theatre NY..."
python3 scrape-ucb-ny.py > /dev/null 2>&1
if [ -f "ucb-ny-shows.json" ]; then
    UCB_NY_COUNT=$(python3 -c "import json; d=json.load(open('ucb-ny-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
    echo "✅ UCB NY: $UCB_NY_COUNT shows"
fi

echo ""

# Los Angeles
echo "📍 LOS ANGELES SCRAPERS"
echo "-----------------------"

echo "Running Comedy Store..."
python3 scrape-comedy-store.py > /dev/null 2>&1
if [ -f "comedy-store-shows.json" ]; then
    CS_COUNT=$(python3 -c "import json; d=json.load(open('comedy-store-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
    echo "✅ Comedy Store: $CS_COUNT shows"
fi

echo "Running Largo..."
if [ -f "scrape-largo.py" ]; then
    python3 scrape-largo.py > /dev/null 2>&1
    if [ -f "largo-shows.json" ]; then
        LARGO_COUNT=$(python3 -c "import json; d=json.load(open('largo-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
        echo "✅ Largo: $LARGO_COUNT shows"
    fi
fi

echo "Running UCB LA..."
python3 scrape-ucb-la.py > /dev/null 2>&1
if [ -f "ucb-la-shows.json" ]; then
    UCB_LA_COUNT=$(python3 -c "import json; d=json.load(open('ucb-la-shows.json')); print(d.get('totalShows', len(d.get('shows', []))))")
    echo "✅ UCB LA: $UCB_LA_COUNT shows"
fi

echo ""
echo "=============================="
echo "🎉 ALL SCRAPERS COMPLETE!"
echo "=============================="
