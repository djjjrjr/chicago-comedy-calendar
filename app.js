// State management
let allShows = [];
let filteredShows = [];
let currentFilter = 'all';
let currentView = 'date';
let currentTypeFilter = 'all';
let searchTerm = '';
let dateFilterStart = '';
let dateFilterEnd = '';

// Venue configurations with location data
const venues = {
    'second-city': {
        name: 'Second City',
        color: '#003E7E',
        address: '1616 N Wells St, Chicago, IL 60614',
        phone: '(312) 337-3992',
        website: 'https://www.secondcity.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2968.8!2d-87.6348!3d41.9126!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2ed1d7dc75f%3A0x3e7f7f4dfc4d3e8e!2sThe%20Second%20City!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'io-theater': {
        name: 'iO Theater',
        color: '#C8102E',
        address: '1501 N Kingsbury St, Chicago, IL 60642',
        phone: '(312) 929-2401',
        website: 'https://ioimprov.com/chicago',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2969.2!2d-87.6535!3d41.9095!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2ef1f7f7f7f%3A0x7f7f7f7f7f7f7f7f!2siO%20Theater!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'annoyance': {
        name: 'Annoyance Theatre',
        color: '#000000',
        address: '851 W Belmont Ave, Chicago, IL 60657',
        phone: '(773) 697-9693',
        website: 'https://theannoyance.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2968.1!2d-87.6495!3d41.9395!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2f1f7f7f7f7%3A0x8f8f8f8f8f8f8f8f!2sThe%20Annoyance%20Theatre!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'zanies': {
        name: 'Zanies',
        color: '#D2691E',
        address: '1548 N Wells St, Chicago, IL 60610',
        phone: '(312) 337-4027',
        website: 'https://chicago.zanies.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2969.0!2d-87.6345!3d41.9108!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2ed1f7f7f7f%3A0x9f9f9f9f9f9f9f9f!2sZanies%20Comedy%20Club!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'laugh-factory': {
        name: 'Laugh Factory',
        color: '#8B4513',
        address: '3175 N Broadway, Chicago, IL 60657',
        phone: '(773) 327-3175',
        website: 'https://chicago.laughfactory.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2967.5!2d-87.6450!3d41.9425!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2f3f7f7f7f7%3A0xa0a0a0a0a0a0a0a0!2sLaugh%20Factory%20Chicago!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'lincoln-lodge': {
        name: 'Lincoln Lodge',
        color: '#2F4F4F',
        address: '2424 N Lincoln Ave, Chicago, IL 60614',
        phone: '(773) 868-0608',
        website: 'https://www.lincolnlodge.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2968.5!2d-87.6530!3d41.9265!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2f0f7f7f7f7%3A0xb0b0b0b0b0b0b0b0!2sLincoln%20Lodge!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'den-theatre': {
        name: 'Den Theatre',
        color: '#4B0082',
        address: '1331 N Milwaukee Ave, Chicago, IL 60622',
        phone: '(773) 697-3830',
        website: 'https://thedentheatre.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2969.8!2d-87.6655!3d41.9055!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880fd2f2f7f7f7f7%3A0xc0c0c0c0c0c0c0c0!2sDen%20Theatre!5e0!3m2!1sen!2sus!4v1234567890'
    }
};

// Initialize app
async function init() {
    setupEventListeners();
    await loadShows();
}

// Setup event listeners
function setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchTerm = e.target.value.toLowerCase();
            filterAndDisplayShows();
        });
    }

    // Date range filters
    const dateFilterStartEl = document.getElementById('dateFilterStart');
    const dateFilterEndEl = document.getElementById('dateFilterEnd');

    if (dateFilterStartEl) {
        dateFilterStartEl.addEventListener('change', (e) => {
            dateFilterStart = e.target.value;
            filterAndDisplayShows();
        });
    }

    if (dateFilterEndEl) {
        dateFilterEndEl.addEventListener('change', (e) => {
            dateFilterEnd = e.target.value;
            filterAndDisplayShows();
        });
    }

    // Venue filter buttons
    const filterBtns = document.querySelectorAll('[data-filter]');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            filterAndDisplayShows();
        });
    });

    // Comedy type filter buttons
    const typeFilterBtns = document.querySelectorAll('[data-type-filter]');
    typeFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            typeFilterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentTypeFilter = btn.dataset.typeFilter;
            filterAndDisplayShows();
        });
    });

    // View toggle buttons
    const viewBtns = document.querySelectorAll('.view-btn[data-view]');
    viewBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            viewBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentView = btn.dataset.view;
            filterAndDisplayShows();
        });
    });

    // Modal close
    const modal = document.getElementById('venueModal');
    const closeBtn = document.querySelector('.modal-close');

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }

    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    }
}

// Detect comedy type from show title and description
function detectComedyType(show) {
    const text = `${show.title} ${show.description || ''}`.toLowerCase();
    const types = [];

    // Check for improv keywords
    if (text.match(/improv|improvisation|harold|longform|shortform|whose line/i)) {
        types.push('improv');
    }

    // Check for standup keywords
    if (text.match(/standup|stand-up|stand up|comedian|comic|comedy night|open mic|showcase/i)) {
        types.push('standup');
    }

    // Check for sketch keywords
    if (text.match(/sketch|revue|skit|musical|parody|satire/i)) {
        types.push('sketch');
    }

    // Default to standup if no type detected
    if (types.length === 0) {
        types.push('standup');
    }

    return types;
}

// Load shows from JSON file
async function loadShows() {
    try {
        const response = await fetch('shows.json');
        const data = await response.json();

        allShows = data.shows || [];

        // Add comedy type to each show
        allShows = allShows.map(show => ({
            ...show,
            comedyTypes: detectComedyType(show)
        }));

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
            document.getElementById('showsContainer').style.display = 'block';
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
    // Start with all shows
    filteredShows = [...allShows];

    // Filter by venue
    if (currentFilter !== 'all') {
        filteredShows = filteredShows.filter(show => show.venue === currentFilter);
    }

    // Filter by comedy type
    if (currentTypeFilter !== 'all') {
        filteredShows = filteredShows.filter(show =>
            show.comedyTypes && show.comedyTypes.includes(currentTypeFilter)
        );
    }

    // Filter by search term
    if (searchTerm) {
        filteredShows = filteredShows.filter(show =>
            show.title.toLowerCase().includes(searchTerm) ||
            (show.description && show.description.toLowerCase().includes(searchTerm)) ||
            venues[show.venue].name.toLowerCase().includes(searchTerm)
        );
    }

    // Filter by date range
    if (dateFilterStart || dateFilterEnd) {
        filteredShows = filteredShows.filter(show => {
            const showDate = new Date(show.date).toISOString().split('T')[0];

            // If both dates set, check if show is in range
            if (dateFilterStart && dateFilterEnd) {
                return showDate >= dateFilterStart && showDate <= dateFilterEnd;
            }
            // If only start date, show dates on or after
            else if (dateFilterStart) {
                return showDate >= dateFilterStart;
            }
            // If only end date, show dates on or before
            else if (dateFilterEnd) {
                return showDate <= dateFilterEnd;
            }

            return true;
        });
    }

    displayShows();
}

// Display shows based on current view
function displayShows() {
    const container = document.getElementById('showsContainer');

    if (filteredShows.length === 0) {
        container.style.display = 'none';
        document.getElementById('noShows').style.display = 'block';
        return;
    }

    document.getElementById('noShows').style.display = 'none';
    container.style.display = 'block';

    if (currentView === 'date') {
        displayByDate(container);
    } else if (currentView === 'venue') {
        displayByVenue(container);
    } else {
        displayList(container);
    }
}

// Display shows grouped by date
function displayByDate(container) {
    // Group shows by date
    const groupedByDate = {};
    filteredShows.forEach(show => {
        const date = new Date(show.date).toISOString().split('T')[0];
        if (!groupedByDate[date]) {
            groupedByDate[date] = [];
        }
        groupedByDate[date].push(show);
    });

    // Sort dates
    const sortedDates = Object.keys(groupedByDate).sort();

    // Create HTML
    container.innerHTML = sortedDates.map(date => {
        const dateObj = new Date(date);
        const dateStr = dateObj.toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            year: 'numeric'
        });

        const shows = groupedByDate[date];
        const showsHtml = shows.map(show => createShowCard(show)).join('');

        return `
            <div class="date-group">
                <div class="date-group-header" onclick="toggleDateGroup(this)">
                    <span>${dateStr} (${shows.length} show${shows.length > 1 ? 's' : ''})</span>
                    <span class="arrow">▼</span>
                </div>
                <div class="date-group-shows">
                    ${showsHtml}
                </div>
            </div>
        `;
    }).join('');
}

// Display shows grouped by venue
function displayByVenue(container) {
    // Group shows by venue
    const groupedByVenue = {};
    filteredShows.forEach(show => {
        if (!groupedByVenue[show.venue]) {
            groupedByVenue[show.venue] = [];
        }
        groupedByVenue[show.venue].push(show);
    });

    // Sort by venue name
    const sortedVenues = Object.keys(groupedByVenue).sort((a, b) =>
        venues[a].name.localeCompare(venues[b].name)
    );

    // Create HTML
    container.innerHTML = sortedVenues.map(venueId => {
        const venueInfo = venues[venueId];
        const shows = groupedByVenue[venueId];
        const showsHtml = shows.map(show => createShowCard(show)).join('');

        return `
            <div class="venue-group">
                <div class="venue-group-header" onclick="toggleVenueGroup(this)">
                    <span>
                        ${venueInfo.name} (${shows.length} show${shows.length > 1 ? 's' : ''})
                        <button class="venue-info-btn" onclick="event.stopPropagation(); showVenueInfo('${venueId}')">
                            ℹ️ Info
                        </button>
                    </span>
                    <span class="arrow">▼</span>
                </div>
                <div class="venue-group-shows">
                    ${showsHtml}
                </div>
            </div>
        `;
    }).join('');
}

// Display shows as a simple list
function displayList(container) {
    // Sort by date
    const sortedShows = [...filteredShows].sort((a, b) =>
        new Date(a.date) - new Date(b.date)
    );

    container.innerHTML = `
        <div class="date-group-shows">
            ${sortedShows.map(show => createShowCard(show)).join('')}
        </div>
    `;
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

    // Join comedy types for data attribute
    const comedyTypes = show.comedyTypes ? show.comedyTypes.join(' ') : '';

    return `
        <div class="show-card venue-${show.venue}" data-comedy-type="${comedyTypes}">
            <span class="venue-tag" onclick="showVenueInfo('${show.venue}')" style="cursor: pointer;">
                ${venueInfo.name}
            </span>
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

// Toggle date group
function toggleDateGroup(header) {
    const showsContainer = header.nextElementSibling;
    showsContainer.classList.toggle('hidden');
    header.classList.toggle('collapsed');
}

// Toggle venue group
function toggleVenueGroup(header) {
    const showsContainer = header.nextElementSibling;
    showsContainer.classList.toggle('hidden');
    header.classList.toggle('collapsed');
}

// Show venue info modal
function showVenueInfo(venueId) {
    const venueInfo = venues[venueId];
    const modal = document.getElementById('venueModal');

    // Populate modal
    document.getElementById('modalVenueName').textContent = venueInfo.name;

    const detailsHtml = `
        <p class="venue-address">📍 ${venueInfo.address}</p>
        <p class="venue-phone">📞 ${venueInfo.phone}</p>
        <p class="venue-website">🌐 <a href="${venueInfo.website}" target="_blank">${venueInfo.website}</a></p>
    `;
    document.querySelector('.venue-details').innerHTML = detailsHtml;

    // Add map
    const mapHtml = `<iframe src="${venueInfo.mapEmbed}" loading="lazy"></iframe>`;
    document.getElementById('mapContainer').innerHTML = mapHtml;

    // Show modal
    modal.classList.add('active');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
