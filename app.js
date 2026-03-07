// State management
let allShows = [];
let filteredShows = [];
let currentFilter = 'all';
let currentSort = 'date';

// Venue configurations
const venues = {
    'second-city': { name: 'Second City', color: '#FF6B6B' },
    'io-theater': { name: 'iO Theater', color: '#4ECDC4' },
    'annoyance': { name: 'The Annoyance', color: '#FFE66D' },
    'zanies': { name: 'Zanies', color: '#A8DADC' },
    'laugh-factory': { name: 'Laugh Factory', color: '#F4A261' },
    'lincoln-lodge': { name: 'Lincoln Lodge', color: '#E76F51' },
    'den-theatre': { name: 'Den Theatre', color: '#2A9D8F' }
};

// Initialize app
async function init() {
    setupEventListeners();
    await loadShows();
}

// Setup event listeners
function setupEventListeners() {
    // Filter buttons
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            filterAndDisplayShows();
        });
    });

    // Sort buttons
    const sortBtns = document.querySelectorAll('.sort-btn');
    sortBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            sortBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentSort = btn.dataset.sort;
            filterAndDisplayShows();
        });
    });
}

// Load shows from JSON file
async function loadShows() {
    try {
        const response = await fetch('shows.json');
        const data = await response.json();

        allShows = data.shows || [];

        // Update last updated time
        if (data.lastUpdated) {
            const date = new Date(data.lastUpdated);
            document.getElementById('updateTime').textContent = date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: 'numeric',
                minute: '2-digit'
            });
        }

        filterAndDisplayShows();

        // Hide loading, show content
        document.getElementById('loading').style.display = 'none';
        if (allShows.length > 0) {
            document.getElementById('showsContainer').style.display = 'grid';
        } else {
            document.getElementById('noShows').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading shows:', error);
        document.getElementById('loading').innerHTML = `
            <p style="color: var(--primary);">Unable to load shows. Please try again later.</p>
        `;
    }
}

// Filter and sort shows
function filterAndDisplayShows() {
    // Filter
    if (currentFilter === 'all') {
        filteredShows = [...allShows];
    } else {
        filteredShows = allShows.filter(show => show.venue === currentFilter);
    }

    // Sort
    if (currentSort === 'date') {
        filteredShows.sort((a, b) => new Date(a.date) - new Date(b.date));
    } else if (currentSort === 'venue') {
        filteredShows.sort((a, b) => venues[a.venue].name.localeCompare(venues[b.venue].name));
    }

    displayShows();
}

// Display shows
function displayShows() {
    const container = document.getElementById('showsContainer');

    if (filteredShows.length === 0) {
        container.style.display = 'none';
        document.getElementById('noShows').style.display = 'block';
        return;
    }

    document.getElementById('noShows').style.display = 'none';
    container.style.display = 'grid';

    container.innerHTML = filteredShows.map(show => createShowCard(show)).join('');
}

// Create show card HTML
function createShowCard(show) {
    const venueInfo = venues[show.venue];
    const date = new Date(show.date);
    const dateStr = date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });

    return `
        <div class="show-card venue-${show.venue}">
            <span class="venue-tag">${venueInfo.name}</span>
            <h3 class="show-title">${show.title}</h3>
            <div class="show-date">
                📅 ${dateStr}
            </div>
            ${show.time ? `<div class="show-time">🕐 ${show.time}</div>` : ''}
            ${show.description ? `<p class="show-description">${show.description}</p>` : ''}
            ${show.url ? `<a href="${show.url}" target="_blank" rel="noopener noreferrer" class="show-link">Get Tickets →</a>` : ''}
        </div>
    `;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
