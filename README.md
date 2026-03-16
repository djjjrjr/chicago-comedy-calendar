# 🎭 Comedy Calendar - Chicago, New York & Los Angeles

A beautiful, aggregated schedule viewer for comedy venues across three major cities - all in one place!

## 🌆 Cities

**[Chicago](index.html)** | **[New York](ny.html)** | **[Los Angeles](la.html)**

## 🌟 Features

- **ALL Comedy Events** - Aggregates all comedy shows from Do312, DoNYC, and DoLosAngeles
- **Preferred Venues** - Quick access to 7 curated venues per city
- **Other Venues** - Discover new comedy spots beyond the well-known venues
- **Auto-Updated** - Schedules refresh daily via GitHub Actions
- **Beautiful Design** - Brutalist design with unique color scheme for each city
- **Smart Filtering** - Filter by venue, comedy type (improv/standup/sketch), and date
- **Multiple Views** - Group by date, venue, or see a simple list
- **NYC Borough Grouping** - New York includes borough-based grouping
- **Direct Tickets** - Links to buy tickets on event pages

## 🎨 Design

Each city has a unique brutalist design with distinctive colors:

- **Chicago**: Red & Blue (Chicago flag colors)
- **New York**: Orange & Blue (Mets/Knicks colors)
- **Los Angeles**: Sunset Gradient (Orange → Pink → Purple)

Features:
- Bold, high-contrast brutalist aesthetic
- City-specific color palettes
- Responsive mobile design
- Clean, readable typography

## 📍 Featured Venues

### Chicago (7 venues)
- Second City
- iO Theater
- Annoyance Theatre
- Zanies
- Laugh Factory
- Lincoln Lodge
- Den Theatre

### New York (7 venues)
- Comedy Cellar (Manhattan)
- Gotham Comedy Club (Manhattan)
- The Stand (Manhattan)
- The Bell House (Brooklyn)
- Union Hall (Brooklyn)
- Carolines on Broadway (Manhattan)
- UCB Theatre (Manhattan)

### Los Angeles (7 venues)
- The Comedy Store
- Laugh Factory Hollywood
- The Hollywood Improv
- UCB Theatre LA
- Dynasty Typewriter
- Largo at the Coronet
- The Groundlings Theatre

## 🚀 Live Site

Visit: [https://djjjrjr.github.io/chicago-comedy-calendar](https://djjjrjr.github.io/chicago-comedy-calendar)

## 🛠️ How It Works

### Frontend
- Pure HTML/CSS/JavaScript (no frameworks!)
- Each city has its own page: `index.html` (Chicago), `ny.html` (New York), `la.html` (Los Angeles)
- Navigation bar to switch between cities
- Client-side filtering and sorting

### Scrapers
- Python scripts using Playwright (headless browser)
- **Chicago**: Scrapes ALL comedy events from Do312.com
- **New York**: Scrapes ALL comedy events from DoNYC.com
- **Los Angeles**: Scrapes ALL comedy events from DoLosAngeles.com
- Outputs to `shows.json`, `ny-shows.json`, `la-shows.json`
- Includes deduplication logic

### Data Strategy
Instead of scraping individual venue websites, we use event aggregator sites:
- **Do312.com** - Chicago event aggregator
- **DoNYC.com** - New York event aggregator
- **DoLosAngeles.com** - Los Angeles event aggregator

This approach is simpler, more maintainable, and captures MORE events including smaller venues!

### Automation
- GitHub Actions workflow runs daily at 6 AM UTC
- Runs all three scrapers in parallel
- Automatically commits updated schedules
- Fail-safe: keeps existing data if scraper fails
- GitHub Pages serves the latest version

## 📁 Project Structure

```
chicago-comedy-calendar/
├── index.html              # Chicago main page
├── app.js                  # Chicago JavaScript
├── styles.css              # Chicago styles
├── shows.json              # Chicago show data (auto-generated)
├── scraper.py              # Chicago scraper
│
├── ny.html                 # New York main page
├── ny-app.js               # New York JavaScript (with borough grouping)
├── ny-styles.css           # New York styles (orange/blue theme)
├── ny-shows.json           # New York show data (auto-generated)
├── ny-scraper.py           # New York scraper
│
├── la.html                 # Los Angeles main page
├── la-app.js               # Los Angeles JavaScript
├── la-styles.css           # Los Angeles styles (sunset gradient)
├── la-shows.json           # Los Angeles show data (auto-generated)
├── la-scraper.py           # Los Angeles scraper
│
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── update_schedules.yml  # GitHub Actions workflow
└── README.md
```

## 🔧 Development

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/djjjrjr/chicago-comedy-calendar.git
cd chicago-comedy-calendar
```

2. Open `index.html`, `ny.html`, or `la.html` in your browser

### Running the Scrapers

1. Install Python dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Run the scrapers:
```bash
python scraper.py      # Chicago
python ny-scraper.py   # New York
python la-scraper.py   # Los Angeles
```

### Customization

**Change preferred venues:**
1. Edit `PREFERRED_VENUES` array in the respective `app.js` file
2. Update the `venues` config object with venue details

**Change colors:**
- Edit CSS variables in `:root` selector in the respective `styles.css` file

**Change update frequency:**
- Modify cron schedule in `.github/workflows/update_schedules.yml`

## 🎯 Key Features by City

### Chicago
- Standard date/venue/list views
- Filter by preferred venues or "Other Venues"
- Chicago flag color scheme (red & blue)

### New York
- **Borough Grouping** - Unique view to group shows by Manhattan, Brooklyn, Queens, Bronx, Staten Island
- Date/venue/borough/list views
- NYC-inspired color scheme (orange & blue)

### Los Angeles
- Standard date/venue/list views
- Sunset gradient theme (orange → pink → purple)
- LA-specific venue curation

## 📝 Technical Notes

- Scrapers use Playwright to handle JavaScript-rendered pages
- Pagination support to capture all events (not just first page)
- Deduplication prevents duplicate events
- Venue name normalization for consistent grouping
- "Other Venues" displays venue name on each card since it's not in group header
- Borough detection uses keyword matching for non-preferred venues in NYC
- Fail-safe GitHub Actions: keeps existing data if scraper fails

## 🔮 Future Ideas

- [ ] More cities (SF, Austin, Seattle, etc.)
- [ ] Price range indicators
- [ ] Calendar export (iCal)
- [ ] Email/SMS notifications
- [ ] Performer information
- [ ] Reviews and ratings
- [ ] Map view

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

Made with ❤️ for comedy lovers everywhere

Data sourced from Do312.com, DoNYC.com, and DoLosAngeles.com
