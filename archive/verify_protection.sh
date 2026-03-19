#!/bin/bash
# Verification script to ensure all scrapers have data protection

echo "=================================="
echo "Data Protection Verification"
echo "=================================="
echo ""

check_function() {
    local file=$1
    local function=$2
    if grep -q "def ${function}" "$file"; then
        echo "  ✓ $function() exists"
    else
        echo "  ✗ $function() MISSING"
        return 1
    fi
}

check_pattern() {
    local file=$1
    local pattern=$2
    local description=$3
    if grep -q "$pattern" "$file"; then
        echo "  ✓ $description"
    else
        echo "  ✗ $description MISSING"
        return 1
    fi
}

check_scraper() {
    local scraper=$1
    local name=$2
    
    echo "Checking $name ($scraper):"
    echo "----------------------------"
    
    if [ ! -f "$scraper" ]; then
        echo "  ✗ File not found!"
        echo ""
        return 1
    fi
    
    # Check for required functions
    check_function "$scraper" "load_existing_shows"
    check_function "$scraper" "save_shows"
    check_function "$scraper" "main"
    
    # Check for protection patterns
    check_pattern "$scraper" "MIN_SHOWS_THRESHOLD = 20" "Minimum threshold (20 shows)"
    check_pattern "$scraper" "loss_threshold = 0.5" "Loss threshold (50%)"
    check_pattern "$scraper" "existing_shows = load_existing_shows" "Loads existing data in main()"
    check_pattern "$scraper" "save_shows(shows, existing_shows)" "Passes existing_shows to save_shows()"
    check_pattern "$scraper" "saved = save_shows" "Checks save_shows return value"
    check_pattern "$scraper" "return True" "save_shows returns boolean"
    check_pattern "$scraper" "return False" "save_shows can return False"
    
    # Check Python syntax
    if python3 -m py_compile "$scraper" 2>/dev/null; then
        echo "  ✓ Python syntax valid"
    else
        echo "  ✗ Python syntax errors"
        return 1
    fi
    
    echo ""
}

# Check all three scrapers
all_pass=true

check_scraper "scraper-improved.py" "Chicago Scraper" || all_pass=false
check_scraper "ny-scraper.py" "NY Scraper" || all_pass=false
check_scraper "la-scraper.py" "LA Scraper" || all_pass=false

echo "=================================="
if [ "$all_pass" = true ]; then
    echo "✓ All scrapers have data protection"
    echo "=================================="
    exit 0
else
    echo "✗ Some checks failed"
    echo "=================================="
    exit 1
fi
