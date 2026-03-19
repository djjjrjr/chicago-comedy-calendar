#!/bin/bash
# Organize files into clean folder structure

echo "📁 Organizing files..."

# Move Chicago scrapers
mv scraper.py scrapers/chicago/scrape-category.py 2>/dev/null
mv scrape-do312-venues.py scrapers/chicago/
mv scrape-den-theatre.py scrapers/chicago/
mv merge-chicago-shows.py scrapers/chicago/

# Move NY scrapers
mv ny-scraper.py scrapers/ny/scrape-category.py 2>/dev/null
mv scrape-caveat.sh scrapers/ny/
mv scrape-union-hall.sh scrapers/ny/
mv scrape-comedy-cellar.sh scrapers/ny/
mv scrape-the-stand.sh scrapers/ny/
mv scrape-ucb-ny.py scrapers/ny/
mv scrape-bell-house.* scrapers/ny/
mv scrape-gotham.* scrapers/ny/
mv scrape-all-ny.sh scrapers/ny/
mv merge-ny-shows-v2.py scrapers/ny/merge-ny-shows.py

# Move LA scrapers
mv la-scraper.py scrapers/la/scrape-category.py 2>/dev/null
mv scrape-ucb-la.py scrapers/la/
mv scrape-largo.sh scrapers/la/
mv scrape-comedy-store.* scrapers/la/
mv scrape-dynasty-typewriter.* scrapers/la/
mv scrape-dola-venues.py scrapers/la/
mv scrape-all-la.sh scrapers/la/
mv merge-la-shows.py scrapers/la/

# Move data files
mv shows.json data/chicago/
mv do312-venues-shows.json data/chicago/
mv venue-info.json data/chicago/

mv ny-shows.json data/ny/
mv ny-shows-donyc.json data/ny/
mv caveat-shows.json data/ny/
mv union-hall-shows.json data/ny/
mv comedy-cellar-shows.json data/ny/
mv the-stand-shows.json data/ny/
mv ucb-ny-shows.json data/ny/
mv bell-house-shows.json data/ny/
mv gotham-shows.json data/ny/

mv la-shows.json data/la/
mv la-shows-dola.json data/la/
mv ucb-la-shows.json data/la/
mv largo-shows.json data/la/
mv comedy-store-shows.json data/la/
mv dola-venues-shows.json data/la/
mv dynasty-typewriter-shows.json data/la/

# Move web files
mv index.html public/chicago/
mv app.js public/chicago/
mv styles.css public/chicago/

mv ny.html public/ny/index.html
mv ny-app.js public/ny/app.js
mv ny-styles.css public/ny/styles.css

mv la.html public/la/index.html
mv la-app.js public/la/app.js
mv la-styles.css public/la/styles.css

# Move docs
mv *.md docs/ 2>/dev/null

# Move outdated/temp files to archive
mv scraper-old.py archive/ 2>/dev/null
mv scraper-improved.py archive/ 2>/dev/null
mv *-backup.json archive/ 2>/dev/null
mv *-page.html archive/ 2>/dev/null
mv *-raw.json archive/ 2>/dev/null
mv den-theatre-shows.json archive/ 2>/dev/null
mv scrape-union-hall-eventbrite.py archive/ 2>/dev/null
mv merge-ny-shows.sh archive/ 2>/dev/null

# Move utility scripts to root (keep accessible)
mv fix-venue-info.py ./ 2>/dev/null
mv venue-info-scraper.py ./ 2>/dev/null
mv test-all-scrapers.sh ./ 2>/dev/null

echo "✅ Files organized!"
