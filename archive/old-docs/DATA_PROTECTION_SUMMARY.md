# Data Protection Logic Implementation Summary

## Overview

This document summarizes the data protection logic applied to all three scrapers (Chicago, NY, LA) to prevent data loss from partial or failed scrapes.

## Problem Solved

Without data protection, a scraper that fails or returns partial results would overwrite good existing data with incomplete data, causing data loss. This happened before when scrapers timed out or websites had temporary issues.

## Solution: Three-Layer Data Protection

All scrapers now implement identical data protection logic with three key checks:

### 1. Load Existing Data First

```python
def load_existing_shows() -> List[Dict]:
    """Load existing shows from {city}-shows.json"""
    try:
        with open('shows.json', 'r') as f:
            data = json.load(f)
            return data.get('shows', [])
    except FileNotFoundError:
        return []
```

**What it does**: Loads existing data before scraping so we can compare new results against it.

### 2. Minimum Threshold Check

```python
MIN_SHOWS_THRESHOLD = 20  # Require at least 20 shows

if len(shows) < MIN_SHOWS_THRESHOLD:
    if len(existing_shows) > 0:
        print(f"\n⚠️  WARNING: Only scraped {len(shows)} shows (below threshold of {MIN_SHOWS_THRESHOLD})")
        print(f"   Keeping existing {len(existing_shows)} shows to avoid data loss")
        print(f"   NOT overwriting {filename}")
        return False
```

**What it does**: If the new scrape has fewer than 20 shows AND we have existing data, don't save. Keep the existing data.

**Exception**: If there's NO existing data, save anyway (something is better than nothing).

### 3. Loss Percentage Check

```python
loss_threshold = 0.5  # Don't save if we lose more than 50% of shows

if len(existing_shows) > 0:
    if len(shows) < len(existing_shows) * loss_threshold:
        print(f"\n⚠️  WARNING: New scrape has {len(shows)} shows vs {len(existing_shows)} existing (>50% loss)")
        print(f"   Keeping existing shows to avoid data loss")
        print(f"   NOT overwriting {filename}")
        return False
```

**What it does**: If the new scrape has less than 50% of the existing show count, don't save. This catches cases where:
- We had 200 shows, now only got 80 shows (60% loss - DON'T SAVE)
- We had 100 shows, now got 55 shows (45% loss - OK to save)

### 4. Graceful Exit Handling

```python
# In main():
saved = save_shows(shows, existing_shows)

if saved:
    print("\n✓ Scraping complete!")
    sys.exit(0)
else:
    print("\n⚠️  Scrape completed but data not saved (kept existing)")
    sys.exit(0)  # Still exit 0 so workflow doesn't fail
```

**What it does**: Even when we don't save new data, exit with code 0 (success) so GitHub Actions workflows don't fail. The existing data is preserved and everything continues normally.

### 5. Exception Handling Fallback

```python
except Exception as e:
    print(f"\nSCRAPING FAILED")
    print(f"Error: {e}")

    # Check if we have existing data to fall back on
    try:
        existing = load_existing_shows()
        if existing:
            print(f"\n✓ Keeping existing {len(existing)} shows (data preserved)")
            sys.exit(0)  # Don't fail the workflow if we have existing data
    except:
        pass

    sys.exit(1)
```

**What it does**: If the scraper crashes completely, check if we have existing data. If yes, exit with success (0) to preserve data. If no existing data, exit with failure (1).

## Implementation Status

| Scraper | File | Status | Notes |
|---------|------|--------|-------|
| Chicago | `scraper-improved.py` | ✓ Already had protection | Reference implementation |
| New York | `ny-scraper.py` | ✓ Already had protection | Was updated previously |
| Los Angeles | `la-scraper.py` | ✓ Protection added | **Updated in this task** |

## Changes Made to LA Scraper

### File: `la-scraper.py`

#### 1. Added `load_existing_shows()` function (lines 17-24)

```python
def load_existing_shows() -> List[Dict]:
    """Load existing shows from la-shows.json"""
    try:
        with open('la-shows.json', 'r') as f:
            data = json.load(f)
            return data.get('shows', [])
    except FileNotFoundError:
        return []
```

#### 2. Updated `save_shows()` function (lines 278-328)

**Before**: Simple save with no checks
```python
def save_shows(shows: List[Dict]):
    """Save shows to JSON file"""
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'shows': shows
    }
    with open('la-shows.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Saved {len(shows)} shows to la-shows.json")
```

**After**: Smart save with protection logic
```python
def save_shows(shows: List[Dict], existing_shows: List[Dict]):
    """
    Save shows to JSON file, but only if we got enough data

    DATA PROTECTION: This function prevents overwriting good data with partial scrapes
    by checking two conditions:
    1. Minimum threshold check - New scrape must have at least 20 shows
    2. Loss percentage check - New scrape must have at least 50% of existing data

    If either check fails, we keep the existing data to prevent data loss.
    """
    MIN_SHOWS_THRESHOLD = 20

    # Threshold check
    if len(shows) < MIN_SHOWS_THRESHOLD and len(existing_shows) > 0:
        print(f"\n⚠️  WARNING: Only scraped {len(shows)} shows (below threshold)")
        print(f"   NOT overwriting la-shows.json")
        return False

    # Loss percentage check
    if len(existing_shows) > 0:
        loss_threshold = 0.5
        if len(shows) < len(existing_shows) * loss_threshold:
            print(f"\n⚠️  WARNING: New scrape has {len(shows)} vs {len(existing_shows)} existing")
            print(f"   NOT overwriting la-shows.json")
            return False

    # Save if checks pass
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'shows': shows
    }
    with open('la-shows.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Saved {len(shows)} shows to la-shows.json")
    return True
```

#### 3. Updated `main()` function (lines 331-391)

**Changes**:
- Load existing shows before scraping
- Pass `existing_shows` to `save_shows()`
- Check return value of `save_shows()`
- Exit with 0 even when data not saved
- Added fallback logic in exception handler

**Before**:
```python
def main():
    try:
        shows = scrape_all_events()
        if not shows:
            sys.exit(1)
        save_shows(shows)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
```

**After**:
```python
def main():
    try:
        # Load existing shows first (for data protection)
        existing_shows = load_existing_shows()
        if existing_shows:
            print(f"📚 Found {len(existing_shows)} existing shows in la-shows.json\n")

        shows = scrape_all_events()

        # Try to save, but protect against bad scrapes
        saved = save_shows(shows, existing_shows)

        if saved:
            print("\n✓ Scraping complete!")
            sys.exit(0)
        else:
            print("\n⚠️  Scrape completed but data not saved (kept existing)")
            sys.exit(0)  # Still exit 0 so workflow doesn't fail

    except Exception as e:
        print(f"Error: {e}")

        # Check if we have existing data to fall back on
        try:
            existing = load_existing_shows()
            if existing:
                print(f"\n✓ Keeping existing {len(existing)} shows (data preserved)")
                sys.exit(0)  # Don't fail the workflow if we have existing data
        except:
            pass

        sys.exit(1)
```

#### 4. Updated header comment (lines 2-7)

Changed from "Los Angeles Comedy Calendar Scraper" to "IMPROVED VERSION" with notes about the protection features.

## Testing

Created `test_data_protection.py` to verify the protection logic works correctly. The test confirms:

1. Scrapers load existing data before scraping
2. Scrapers refuse to save when getting partial results
3. Scrapers save when starting from scratch (no existing data)
4. Exit codes are correct (0 for success, even when not saving)

## Example Scenarios

### Scenario 1: Normal scrape (200 shows → 195 shows)
- ✓ Pass threshold check (195 > 20)
- ✓ Pass loss check (195 > 200 * 0.5 = 100)
- **Result**: Save new data

### Scenario 2: Partial scrape (200 shows → 15 shows)
- ✗ Fail threshold check (15 < 20)
- **Result**: Keep existing 200 shows, don't save

### Scenario 3: Site timeout (200 shows → 80 shows)
- ✓ Pass threshold check (80 > 20)
- ✗ Fail loss check (80 < 200 * 0.5 = 100)
- **Result**: Keep existing 200 shows, don't save

### Scenario 4: First scrape ever (0 shows → 15 shows)
- Notice: No existing data
- **Result**: Save anyway (better than nothing)

### Scenario 5: Scraper crashes completely
- Exception caught
- Check for existing data
- **Result**: If existing data exists, exit 0 (preserve data). If not, exit 1 (failure).

## Benefits

1. **No more data loss**: Partial scrapes can't overwrite good data
2. **Workflow stability**: Workflows don't fail unnecessarily
3. **Automatic recovery**: Next successful scrape will update data
4. **Clear logging**: Easy to see when protection triggers
5. **Consistent behavior**: All three scrapers work the same way

## Configuration

The thresholds can be adjusted in each scraper's `save_shows()` function:

```python
MIN_SHOWS_THRESHOLD = 20     # Minimum shows required to save
loss_threshold = 0.5          # Don't save if losing more than 50% of shows
```

Recommended values:
- Chicago: 20 shows, 50% loss threshold
- New York: 20 shows, 50% loss threshold
- Los Angeles: 20 shows, 50% loss threshold

## Maintenance

When adding new scrapers or modifying existing ones:

1. Always implement `load_existing_shows()` first
2. Add protection logic to `save_shows()`
3. Update `main()` to use both functions
4. Test with `test_data_protection.py`
5. Verify exit codes are correct

## Conclusion

All three scrapers now have identical, robust data protection logic that prevents data loss from partial or failed scrapes. This ensures the comedy calendar data remains stable and reliable even when websites have temporary issues.
