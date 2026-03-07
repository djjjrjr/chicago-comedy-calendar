# 🎭 Chicago Comedy Calendar

A beautiful, aggregated schedule viewer for Chicago comedy venues - all in one place!

## 🌟 Features

- **7 Venues** - Second City, iO Theater, The Annoyance, Zanies, Laugh Factory, Lincoln Lodge, and Den Theatre
- **Auto-Updated** - Schedules refresh daily via GitHub Actions
- **Beautiful Design** - Modern, responsive interface with smooth animations
- **Smart Filtering** - Filter by venue and sort by date or venue name
- **Direct Tickets** - Links to buy tickets on venue websites

## 🎨 Design

The site features a vibrant, comedy-themed color palette with:
- Gradient headers with animated emoji
- Color-coded venue cards
- Smooth hover effects and transitions
- Fully responsive mobile design
- Clean, readable typography

## 🚀 Live Site

Visit: [https://djjjrjr.github.io/chicago-comedy-calendar](https://djjjrjr.github.io/chicago-comedy-calendar)

## 🛠️ How It Works

### Frontend
- Pure HTML/CSS/JavaScript (no frameworks needed!)
- Fetches data from `shows.json`
- Client-side filtering and sorting

### Scraper
- Python script using BeautifulSoup
- Scrapes show information from each venue's website
- Outputs to `shows.json`

### Automation
- GitHub Actions workflow runs daily at 6 AM UTC (12 AM Chicago)
- Automatically commits updated schedules
- GitHub Pages serves the latest version

## 📁 Project Structure

```
chicago-comedy-calendar/
├── index.html              # Main HTML file
├── styles.css              # Styling and design
├── app.js                  # JavaScript logic
├── shows.json              # Show data (auto-generated)
├── scraper.py              # Python scraper script
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── update-schedules.yml  # GitHub Actions workflow
└── README.md
```

## 🔧 Development

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/djjjrjr/chicago-comedy-calendar.git
cd chicago-comedy-calendar
```

2. Open `index.html` in your browser

### Running the Scraper

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the scraper:
```bash
python scraper.py
```

### Customization

**Add a new venue:**
1. Add venue config to `scraper.py` VENUES dict
2. Implement scraper function
3. Add filter button in `index.html`
4. Add venue color in `app.js` venues object

**Change colors:**
- Edit CSS variables in `:root` selector in `styles.css`

**Change update frequency:**
- Modify cron schedule in `.github/workflows/update-schedules.yml`

## 🔮 Future Ideas

- [ ] Add performer names to show cards
- [ ] Price range indicators
- [ ] Search functionality
- [ ] Calendar export (iCal)
- [ ] Email/SMS notifications for favorite venues
- [ ] Show duration and age restrictions
- [ ] Map view of venues

## 📝 Notes

- Scrapers need to be implemented/updated based on each venue's website structure
- Some venues may block scraping - consider using APIs if available
- Show times and availability are subject to change - always verify on venue websites

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

Made with ❤️ for Chicago comedy lovers
