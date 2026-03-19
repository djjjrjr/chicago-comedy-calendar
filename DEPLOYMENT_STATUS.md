# Deployment Status - March 19, 2026

## ✅ Repository Organized & Cleaned

The repository has been reorganized into a clean, maintainable structure with clear separation of concerns.

### 📁 New Structure

```
comedy-calendar/
├── scrapers/      # All scraping scripts by city
├── data/          # JSON outputs by city
├── public/        # Static websites by city (ready to deploy)
├── docs/          # Documentation (GUIDE.md)
├── archive/       # Deprecated files
└── design-options/# Alternative CSS themes
```

### 🎯 Current Data (All Fresh - No Stale Shows)

- **Chicago**: 159 shows
- **New York**: 316 shows
- **Los Angeles**: 321 shows
- **Total**: 796 comedy shows

All shows dated from **March 19, 2026** onwards (stale data filtered out).

---

## 🚀 Deployment Options

### Option 1: Quick Local Test
```bash
# Run all scrapers
./deploy.sh

# Open in browser
open public/chicago/index.html
open public/ny/index.html
open public/la/index.html
```

### Option 2: Static Hosting (Netlify, Vercel, GitHub Pages)

**Deploy the `public/` folder:**
```bash
cd public
# Each city subfolder is a standalone site
```

**For GitHub Pages:**
```bash
git add public/
git commit -m "Deploy comedy calendars"
git push origin main

# Set up 3 repos or 3 branches:
# - chicago-comedy → public/chicago/*
# - ny-comedy → public/ny/*
# - la-comedy → public/la/*
```

### Option 3: Server with Cron (Automated Updates)

1. **Clone to server:**
```bash
git clone [repo-url] /var/www/comedy-calendar
cd /var/www/comedy-calendar
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
npm install -g agent-browser
```

3. **Set up daily scraping:**
```bash
crontab -e
# Add: 0 6 * * * cd /var/www/comedy-calendar && ./deploy.sh >> logs/scrape.log 2>&1
```

4. **Serve public folder:**
```bash
# Apache/Nginx config to serve public/*
```

---

## 🔄 Dual Scraping Approach (Implemented)

All three cities now use the **dual approach** for comprehensive coverage:

### Chicago
✅ **Category scraper** (Do312 /events/comedy) → 52 shows
✅ **Venue page scrapers** (7 preferred venues) → 134 shows
✅ **Merge + dedupe** → 159 unique shows

### New York
✅ **Category scraper** (DoNYC /events/comedy) → 74 shows
✅ **Custom venue scrapers** (8 venues with unique challenges) → 410 shows
✅ **Stale filter + dedupe** → 316 current shows

### Los Angeles
✅ **Category scraper** (DoLA /events/comedy) → 181 shows
✅ **Venue page scrapers** (Dynasty, Improv, Laugh Factory) → 110 shows
✅ **Custom scrapers** (UCB, Comedy Store, Largo) → 161 shows
✅ **Stale filter + dedupe** → 321 current shows

---

## 🛠️ Key Improvements Made

### 1. Stale Data Filtering ✅
- Added `filter_stale_shows()` to NY and LA merge scripts
- Removes any shows before today's date
- NY: Filtered 168 stale shows (2023-2025)
- LA: Filtered 33 stale shows

### 2. Repository Organization ✅
- Created logical folder structure
- Moved 100+ files to appropriate locations
- Archived deprecated files (old docs, backups, test files)
- Created symlinks for data access from public folders

### 3. Documentation ✅
- **README.md**: Quick overview and getting started
- **GUIDE.md**: Complete 300+ line guide with troubleshooting
- **STRUCTURE.txt**: Visual tree of project layout
- Archived 16 old documentation files

### 4. Deployment Scripts ✅
- **deploy.sh**: Master script for all cities
- **scrapers/{city}/scrape-all.sh**: City-specific runners
- All scripts tested and working

### 5. Data Integrity ✅
- Symlinks connect public sites to data folders
- All 3 sites verified functional (159, 316, 321 shows accessible)
- Deduplication working correctly
- No broken references

---

## 📋 Quick Commands

```bash
# Update all data
./deploy.sh

# Update one city
./scrapers/chicago/scrape-all.sh
./scrapers/ny/scrape-all-ny.sh
./scrapers/la/scrape-all-la.sh

# View local sites
open public/chicago/index.html
open public/ny/index.html
open public/la/index.html

# Check data
python3 -c "import json; print([len(json.load(open(f'data/{c}/{"ny-shows" if c=="ny" else "la-shows" if c=="la" else "shows"}.json'))['shows']) for c in ['chicago','ny','la']])"
```

---

## 📊 File Count Summary

**Before Cleanup**: 100+ files in root directory
**After Cleanup**:
- Root: 5 essential files (README, deploy.sh, requirements.txt, 2 utilities)
- Scrapers: 28 organized scraper files
- Data: 20 JSON files in organized structure
- Public: 3 complete websites with symlinks
- Archive: 20+ deprecated files safely stored

---

## ✅ Ready to Deploy

The project is **production-ready**:
- ✅ All scrapers functional
- ✅ Data fresh and filtered
- ✅ Websites working locally
- ✅ Documentation complete
- ✅ Repository organized
- ✅ Deployment scripts tested

**Next Steps:**
1. Choose deployment option (static hosting recommended)
2. Deploy `public/` folders to hosting service
3. Set up automated scraping (cron or GitHub Actions)
4. Monitor for scraper failures

---

## 📚 Documentation

- **Quick Start**: See README.md
- **Complete Guide**: See docs/GUIDE.md
- **Structure**: See STRUCTURE.txt
- **Historical Notes**: See archive/old-docs/

---

## 🎉 Summary

The comedy calendar project is now:
- **Organized**: Clean folder structure
- **Documented**: Comprehensive guides
- **Tested**: All systems verified working
- **Fresh**: Current data only (no stale shows)
- **Scalable**: Easy to add new venues/cities
- **Deployable**: Multiple deployment options ready

**Total Coverage**: 796 comedy shows across Chicago, New York, and Los Angeles.
