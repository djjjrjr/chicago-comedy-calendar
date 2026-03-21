// State management
let allShows = [];
let filteredShows = [];
let currentFilter = 'all';
let currentView = 'date';
let currentTypeFilter = 'all';
let currentBoroughFilter = 'all';
let searchTerm = '';
let dateFilterStart = '';
let dateFilterEnd = '';

// Preferred venues list - these are the main comedy venues
const PREFERRED_VENUES = [
    'Comedy Cellar',
    'Gotham Comedy Club',
    'The Stand',
    'The Bell House',
    'Union Hall',
    'Caveat',
    'UCB Theatre'
];

// Borough mapping for NY venues
const BOROUGH_MAP = {
    'Comedy Cellar': 'Manhattan',
    'Gotham Comedy Club': 'Manhattan',
    'The Stand': 'Manhattan',
    'Caveat': 'Manhattan',
    'UCB Theatre': 'Manhattan',
    'The Bell House': 'Brooklyn',
    'Union Hall': 'Brooklyn'
};

// Venue configurations with location data (for preferred venues only)
const venues = {
    'Comedy Cellar': {
        name: 'Comedy Cellar',
        color: '#8B0000',
        address: '117 MacDougal St, New York, NY 10012',
        phone: '(212) 254-3480',
        website: 'https://www.comedycellar.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.2!2d-74.0011!3d40.7295!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c2598f0f0f0f0f%3A0x1f1f1f1f1f1f1f1f!2sComedy%20Cellar!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'Gotham Comedy Club': {
        name: 'Gotham Comedy Club',
        color: '#000080',
        address: '208 W 23rd St, New York, NY 10011',
        phone: '(212) 367-9000',
        website: 'https://www.gothamcomedyclub.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3023.8!2d-73.9955!3d40.7438!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a0a0a0a0a0%3A0x2f2f2f2f2f2f2f2f!2sGotham%20Comedy%20Club!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'The Stand': {
        name: 'The Stand',
        color: '#DC143C',
        address: '239 3rd Ave, New York, NY 10003',
        phone: '(212) 933-3029',
        website: 'https://thestandnyc.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3023.5!2d-73.9843!3d40.7356!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259b1b1b1b1b1%3A0x3f3f3f3f3f3f3f3f!2sThe%20Stand!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'The Bell House': {
        name: 'The Bell House',
        color: '#2F4F4F',
        address: '149 7th St, Brooklyn, NY 11215',
        phone: '(718) 643-6510',
        website: 'https://www.thebellhouseny.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3025.2!2d-73.9801!3d40.6708!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a0c0c0c0c0c%3A0x4f4f4f4f4f4f4f4f!2sThe%20Bell%20House!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'Union Hall': {
        name: 'Union Hall',
        color: '#8B4513',
        address: '702 Union St, Brooklyn, NY 11215',
        phone: '(718) 638-4400',
        website: 'https://www.unionhallny.com',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3025.5!2d-73.9834!3d40.6755!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25a1d1d1d1d1d%3A0x5f5f5f5f5f5f5f5f!2sUnion%20Hall!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'Caveat': {
        name: 'Caveat',
        color: '#9B59B6',
        address: '21 A Clinton St, New York, NY 10002',
        phone: '(212) 228-2100',
        website: 'https://caveat.nyc',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.5!2d-73.9838!3d40.7215!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25990a0a0a0a0%3A0x1f1f1f1f1f1f1f1f!2sCaveat!5e0!3m2!1sen!2sus!4v1234567890'
    },
    'UCB Theatre': {
        name: 'UCB Theatre',
        color: '#006400',
        address: '242 E 14th St, New York, NY 10003',
        phone: '(212) 366-9231',
        website: 'https://ucbcomedy.com/shows/new-york/',
        mapEmbed: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3023.5!2d-73.9843!3d40.7315!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c25990b0b0b0b0%3A0x2e2e2e2e2e2e2e2e!2sUCB%20Theatre!5e0!3m2!1sen!2sus!4v1234567890'
    }
};

// Normalize venue names to group sub-venues under parent
function normalizeVenueName(venueName) {
    if (!venueName) return venueName;

    // Comedy Cellar rooms → Comedy Cellar
    if (venueName.includes('Comedy Cellar')) {
        return 'Comedy Cellar';
    }
    return venueName;
}

// Helper function to check if a venue is preferred
function isPreferredVenue(venueName) {
    const normalized = normalizeVenueName(venueName);
    return PREFERRED_VENUES.includes(normalized);
}

// Helper function to detect borough from venue name
function detectBorough(venueName) {
    // First check if it's in our borough map
    if (BOROUGH_MAP[venueName]) {
        return BOROUGH_MAP[venueName];
    }

    // Try to detect from venue name keywords
    const lowerName = venueName.toLowerCase();
    if (lowerName.includes('brooklyn')) return 'Brooklyn';
    if (lowerName.includes('queens')) return 'Queens';
    if (lowerName.includes('bronx')) return 'Bronx';
    if (lowerName.includes('staten island')) return 'Staten Island';

    // Default to Manhattan if we can't determine
    return 'Manhattan';
}

// Load venue information database
async function loadVenueInfo() {
    try {
        const response = await fetch('venue-info.json');
        if (response.ok) {
            window.venueInfoData = await response.json();
            console.log(`✓ Loaded info for ${Object.keys(window.venueInfoData.venues || {}).length} venues`);
        }
    } catch (error) {
        console.log('ℹ️ No venue info database found yet (will be created on first scrape)');
        window.venueInfoData = { venues: {} };
    }
}

// Initialize app
async function init() {
    setupEventListeners();
    await Promise.all([loadShows(), loadVenueInfo()]);
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

    // Date picker modal
    const datePickerInput = document.getElementById('datePickerInput');
    if (datePickerInput) {
        datePickerInput.addEventListener('click', () => {
            document.getElementById('datePickerModal').classList.remove('hidden');
        });
    }

    // Radio button handling
    const radioButtons = document.querySelectorAll('input[name="dateMode"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', (e) => {
            const singleDate = document.getElementById('singleDate');
            const rangeStart = document.getElementById('rangeStart');
            const rangeEnd = document.getElementById('rangeEnd');

            if (e.target.value === 'single') {
                singleDate.disabled = false;
                rangeStart.disabled = true;
                rangeEnd.disabled = true;
            } else {
                singleDate.disabled = true;
                rangeStart.disabled = false;
                rangeEnd.disabled = false;
            }
        });
    });

    // Initialize - disable range inputs by default
    document.getElementById('rangeStart').disabled = true;
    document.getElementById('rangeEnd').disabled = true;

    // Venue filter buttons
    const filterBtns = document.querySelectorAll('[data-filter]');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;

            // Hide active filter pill when using static buttons
            const pill = document.getElementById('activeFilterPill');
            if (pill) pill.classList.add('hidden');

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

    // Borough filter buttons
    const boroughFilterBtns = document.querySelectorAll('[data-borough-filter]');
    boroughFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            boroughFilterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentBoroughFilter = btn.dataset.boroughFilter;
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
        // Add cache-busting to always get fresh data
        const response = await fetch('ny-shows.json?t=' + Date.now());
        const data = await response.json();

        allShows = data.shows || [];

        // Add comedy type and borough to each show
        allShows = allShows.map(show => ({
            ...show,
            comedyTypes: detectComedyType(show),
            borough: detectBorough(show.venue)
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
    // Start with all shows, filtering out past events
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Start of today

    filteredShows = allShows.filter(show => {
        const showDate = new Date(show.date);
        return showDate >= today; // Only show today and future events
    });

    // Filter by venue
    if (currentFilter !== 'all') {
        if (currentFilter === 'other') {
            // Show only non-preferred venues
            filteredShows = filteredShows.filter(show => !isPreferredVenue(show.venue));
        } else {
            // Show only the selected preferred venue
            filteredShows = filteredShows.filter(show => show.venue === currentFilter);
        }
    }

    // Filter by comedy type
    if (currentTypeFilter !== 'all') {
        filteredShows = filteredShows.filter(show =>
            show.comedyTypes && show.comedyTypes.includes(currentTypeFilter)
        );
    }

    // Filter by borough
    if (currentBoroughFilter !== 'all') {
        filteredShows = filteredShows.filter(show =>
            show.borough === currentBoroughFilter
        );
    }

    // Filter by search term
    if (searchTerm) {
        filteredShows = filteredShows.filter(show => {
            const titleMatch = show.title.toLowerCase().includes(searchTerm);
            const descMatch = show.description && show.description.toLowerCase().includes(searchTerm);
            const venueMatch = show.venue.toLowerCase().includes(searchTerm);
            return titleMatch || descMatch || venueMatch;
        });
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

    // Separate preferred venues from other venues
    const preferredVenueNames = Object.keys(groupedByVenue).filter(venueName => isPreferredVenue(venueName));
    const otherVenueNames = Object.keys(groupedByVenue).filter(venueName => !isPreferredVenue(venueName));

    // Sort preferred venues alphabetically
    preferredVenueNames.sort((a, b) => a.localeCompare(b));

    // Combine: preferred venues first, then "Other Venues" if there are any
    const sortedVenues = [...preferredVenueNames];
    if (otherVenueNames.length > 0) {
        sortedVenues.push('__OTHER__'); // Special marker for other venues group
    }

    // Create HTML
    container.innerHTML = sortedVenues.map(venueIdentifier => {
        if (venueIdentifier === '__OTHER__') {
            // Create "Other Venues" group
            const allOtherShows = [];
            otherVenueNames.forEach(venueName => {
                allOtherShows.push(...groupedByVenue[venueName]);
            });
            const showsHtml = allOtherShows.map(show => createShowCard(show, true)).join('');

            return `
                <div class="venue-group">
                    <div class="venue-group-header" onclick="toggleVenueGroup(this)">
                        <span>
                            Other Venues (${allOtherShows.length} show${allOtherShows.length > 1 ? 's' : ''})
                        </span>
                        <span class="arrow">▼</span>
                    </div>
                    <div class="venue-group-shows">
                        ${showsHtml}
                    </div>
                </div>
            `;
        } else {
            // Preferred venue group
            const venueInfo = venues[venueIdentifier];
            const shows = groupedByVenue[venueIdentifier];
            const showsHtml = shows.map(show => createShowCard(show)).join('');

            return `
                <div class="venue-group">
                    <div class="venue-group-header" onclick="toggleVenueGroup(this)">
                        <span>
                            ${venueInfo.name} (${shows.length} show${shows.length > 1 ? 's' : ''})
                            <button class="venue-info-btn" onclick="event.stopPropagation(); showVenueInfo('${venueIdentifier}')">
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
        }
    }).join('');
}

// Display shows grouped by borough
function displayByBorough(container) {
    // Group shows by borough
    const groupedByBorough = {};
    filteredShows.forEach(show => {
        const borough = show.borough || 'Manhattan';
        if (!groupedByBorough[borough]) {
            groupedByBorough[borough] = [];
        }
        groupedByBorough[borough].push(show);
    });

    // Sort boroughs by priority (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
    const boroughOrder = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'];
    const sortedBoroughs = boroughOrder.filter(b => groupedByBorough[b]);

    // Create HTML
    container.innerHTML = sortedBoroughs.map(borough => {
        const shows = groupedByBorough[borough];
        const showsHtml = shows.map(show => createShowCard(show, true)).join('');

        return `
            <div class="venue-group">
                <div class="venue-group-header" onclick="toggleVenueGroup(this)">
                    <span>
                        ${borough} (${shows.length} show${shows.length > 1 ? 's' : ''})
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
function createShowCard(show, showVenueOnCard = false) {
    const isPreferred = isPreferredVenue(show.venue);
    const date = new Date(show.date);
    const dateStr = date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });

    // Join comedy types for data attribute
    const comedyTypes = show.comedyTypes ? show.comedyTypes.join(' ') : '';

    // Generate venue class (for preferred venues only, use sanitized version)
    let venueClass = '';
    if (isPreferred) {
        // Create a safe CSS class name from the venue name
        venueClass = `venue-${show.venue.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`;
    }

    // For "Other Venues" group in venue view, or non-preferred venues, show venue name on card
    const shouldShowVenueOnCard = showVenueOnCard || !isPreferred;

    if (shouldShowVenueOnCard) {
        // Non-preferred venue: show venue name with info button (like preferred venues)
        const escapedVenue = show.venue.replace(/'/g, "\\'");
        return `
            <div class="show-card ${venueClass}" data-comedy-type="${comedyTypes}">
                <span class="venue-tag" onclick="showOtherVenueInfo('${escapedVenue}')" style="cursor: pointer;">
                    ${show.venue}
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
    } else {
        // Preferred venue: show venue tag with click handler
        const venueInfo = venues[show.venue];
        return `
            <div class="show-card ${venueClass}" data-comedy-type="${comedyTypes}">
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
// Show venue info modal for preferred venues
function showVenueInfo(venueName) {
    const venueInfo = venues[venueName];
    if (!venueInfo) return; // Only show modal for preferred venues

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

// Show venue info modal for other (non-preferred) venues
function showOtherVenueInfo(venueName) {
    const modal = document.getElementById('venueModal');

    // Populate modal with venue name
    document.getElementById('modalVenueName').textContent = venueName;

    // Check if we have scraped venue info
    const venueInfo = window.venueInfoData?.venues?.[venueName];

    let detailsHtml = '';

    if (venueInfo) {
        // Show available venue information
        if (venueInfo.address) {
            detailsHtml += `<p class="venue-address">📍 ${venueInfo.address}</p>`;
        }
        if (venueInfo.phone) {
            detailsHtml += `<p class="venue-phone">📞 ${venueInfo.phone}</p>`;
        }
        if (venueInfo.website) {
            detailsHtml += `<p class="venue-website">🌐 <a href="${venueInfo.website}" target="_blank">${venueInfo.website}</a></p>`;
        }
    }

    // Always add "See all events" button
    detailsHtml += `
        <button class="see-all-venue-btn-modal" onclick="filterToVenue('${venueName.replace(/'/g, "\\'")}', true); closeVenueModal();">
            See all events at this venue →
        </button>
    `;

    document.querySelector('.venue-details').innerHTML = detailsHtml;

    // Clear map (we don't have coordinates for scraped venues yet)
    document.getElementById('mapContainer').innerHTML = '';

    // Show modal
    modal.classList.add('active');
}

// Close venue modal
function closeVenueModal() {
    const modal = document.getElementById('venueModal');
    modal.classList.remove('active');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Date Picker Modal Functions
function closeDatePicker() {
    document.getElementById('datePickerModal').classList.add('hidden');
}

function clearDateFilter() {
    dateFilterStart = '';
    dateFilterEnd = '';
    document.getElementById('singleDate').value = '';
    document.getElementById('rangeStart').value = '';
    document.getElementById('rangeEnd').value = '';
    document.getElementById('datePickerInput').value = '';
    closeDatePicker();
    filterAndDisplayShows();
}

function applyDateFilter() {
    const mode = document.querySelector('input[name="dateMode"]:checked').value;
    const datePickerInput = document.getElementById('datePickerInput');

    if (mode === 'single') {
        const singleDate = document.getElementById('singleDate').value;
        if (singleDate) {
            dateFilterStart = singleDate;
            dateFilterEnd = singleDate;

            // Format for display
            const dateObj = new Date(singleDate + 'T00:00:00');
            const formatted = dateObj.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
            datePickerInput.value = formatted;
        }
    } else {
        const rangeStart = document.getElementById('rangeStart').value;
        const rangeEnd = document.getElementById('rangeEnd').value;

        if (rangeStart || rangeEnd) {
            dateFilterStart = rangeStart;
            dateFilterEnd = rangeEnd;

            // Format for display
            let displayText = '';
            if (rangeStart && rangeEnd) {
                const startObj = new Date(rangeStart + 'T00:00:00');
                const endObj = new Date(rangeEnd + 'T00:00:00');
                const startFormatted = startObj.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                });
                const endFormatted = endObj.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                displayText = `${startFormatted} - ${endFormatted}`;
            } else if (rangeStart) {
                const startObj = new Date(rangeStart + 'T00:00:00');
                const startFormatted = startObj.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                displayText = `From ${startFormatted}`;
            } else if (rangeEnd) {
                const endObj = new Date(rangeEnd + 'T00:00:00');
                const endFormatted = endObj.toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                displayText = `Until ${endFormatted}`;
            }
            datePickerInput.value = displayText;
        }
    }

    closeDatePicker();
    filterAndDisplayShows();
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('datePickerModal');
    if (modal && e.target === modal) {
        closeDatePicker();
    }
});

// Filter to a specific venue (for "other venues" clicking)
function filterToVenue(venueName, isOtherVenue = false) {
    // Set the current filter to this specific venue
    currentFilter = venueName;

    // Update filter button states
    const filterBtns = document.querySelectorAll('[data-filter]');
    filterBtns.forEach(b => b.classList.remove('active'));

    // Find and activate the matching button, or activate "Other" button
    const matchingBtn = Array.from(filterBtns).find(btn => btn.dataset.filter === venueName);
    if (matchingBtn) {
        matchingBtn.classList.add('active');
    } else if (isOtherVenue) {
        const otherBtn = Array.from(filterBtns).find(btn => btn.dataset.filter === 'other');
        if (otherBtn) otherBtn.classList.add('active');
    }

    // Show active filter indicator
    showActiveFilterPill(venueName);

    // Apply the filter
    filterAndDisplayShows();
}

function showActiveFilterPill(venueName) {
    const pill = document.getElementById('activeFilterPill');
    const text = document.getElementById('activeFilterText');

    if (!pill || !text) return;

    // Only show pill for non-static-button filters
    const isStaticButton = document.querySelector(`[data-filter="${venueName}"]`);
    if (!isStaticButton) {
        text.textContent = `Showing: ${venueName}`;
        pill.classList.remove('hidden');
    } else {
        pill.classList.add('hidden');
    }
}

function clearVenueFilter() {
    const pill = document.getElementById('activeFilterPill');
    if (pill) pill.classList.add('hidden');

    // Reset to "All Venues"
    currentFilter = 'all';
    const filterBtns = document.querySelectorAll('[data-filter]');
    filterBtns.forEach(b => b.classList.remove('active'));
    const allBtn = document.querySelector('[data-filter="all"]');
    if (allBtn) allBtn.classList.add('active');

    filterAndDisplayShows();
}
