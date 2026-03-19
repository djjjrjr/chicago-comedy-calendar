# 🎭 Comedy Calendar - Chicago, NY & LA

Beautiful, aggregated schedule viewers for comedy venues in three cities - all in one place!

## 🌟 Features

- **3 Cities** - Chicago (7 venues), New York (7 venues), Los Angeles (7 venues)
- **Auto-Updated** - Dual scraping approach (category pages + venue scrapers)
- **Beautiful Design** - Modern, responsive interface with smooth animations
- **Smart Filtering** - Filter by venue, comedy type, and date
- **Direct Tickets** - Links to buy tickets on venue websites

## 🚀 Live Sites

- **Chicago**: [https://djjjrjr.github.io/chicago-comedy-calendar](https://djjjrjr.github.io/chicago-comedy-calendar)
- **New York**: [https://djjjrjr.github.io/chicago-comedy-calendar/ny.html](https://djjjrjr.github.io/chicago-comedy-calendar/ny.html)
- **Los Angeles**: [https://djjjrjr.github.io/chicago-comedy-calendar/la.html](https://djjjrjr.github.io/chicago-comedy-calendar/la.html)

## 📊 Current Coverage

- Chicago: 159 shows
- New York: 316 shows
- Los Angeles: 321 shows
- **Total: 796 comedy shows**

## 🛠️ How It Works

### Frontend
- Pure HTML/CSS/JavaScript (no frameworks!)
- Fetches data from JSON files
- Client-side filtering and sorting

### Dual Scraping Approach
Each city combines two strategies:
1. **Category scraping** - Broad coverage from Do312/DoNYC/DoLA
2. **Venue scrapers** - Deep coverage with custom scrapers for each venue

### Technologies
- Python + BeautifulSoup for static sites
- agent-browser for JavaScript-heavy sites
- cloudscraper for Cloudflare-protected sites

## 📁 Project Structure

```
.
├── index.html, ny.html, la.html    # Site pages
├── shows.json, ny-shows.json, la-shows.json  # Data
├── scrapers/                       # Scraping scripts by city
├── data/                           # Source of truth
└── deploy.sh                       # Run all scrapers
```

## 🔧 Running Locally

1. Clone the repository:
```bash
git clone https://github.com/djjjrjr/chicago-comedy-calendar.git
cd chicago-comedy-calendar
```

2. Open `index.html` (Chicago), `ny.html`, or `la.html` in your browser

## 🔄 Updating Data

```bash
# Install dependencies
pip install -r requirements.txt

# Run all scrapers and deploy
./deploy.sh

# Or run individual cities
./scrapers/chicago/scrape-all.sh
./scrapers/ny/scrape-all-ny.sh
./scrapers/la/scrape-all-la.sh
```

## 🎨 Customization

**Add a new venue:**
1. Create scraper in `scrapers/{city}/`
2. Add to merge script
3. Add filter button to HTML
4. Update preferred venues list

**Change colors:**
- Edit CSS variables in `styles.css`, `ny-styles.css`, `la-styles.css`

## 📝 Documentation

- Complete guide: `docs/GUIDE.md`
- Deployment notes: `docs/DEPLOYMENT_STATUS.md`

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Made with ❤️ for comedy lovers
