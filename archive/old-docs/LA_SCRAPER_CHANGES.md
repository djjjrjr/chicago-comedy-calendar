# LA Scraper Data Protection Changes

## Summary

Applied Chicago's proven data protection logic to the LA scraper to prevent data loss from partial or failed scrapes.

## Files Modified

- `/workspace/group/chicago-comedy-calendar/la-scraper.py`

## Changes Made

### 1. Updated Header Documentation

```diff
 #!/usr/bin/env python3
 """
-Los Angeles Comedy Calendar Scraper
-Fetches ALL comedy show schedules from DoLosAngeles.com
+Los Angeles Comedy Calendar Scraper - IMPROVED VERSION
+- Better timeout handling
+- Prevents data loss on partial scrapes
+- Only saves if scrape is successful enough
 """
```

### 2. Added `load_existing_shows()` Function

**New function** (lines 17-24):

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

**Purpose**: Load existing show data before scraping so we can compare new results and protect against data loss.

### 3. Completely Rewrote `save_shows()` Function

#### Before (lines 266-276):

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

**Problem**: Always saves, even if scrape only returned 5 shows due to a timeout or error.

#### After (lines 278-328):

```python
def save_shows(shows: List[Dict], existing_shows: List[Dict]):
    """
    Save shows to JSON file, but only if we got enough data

    DATA PROTECTION: This function prevents overwriting good data with partial scrapes
    by checking two conditions:
    1. Minimum threshold check - New scrape must have at least 20 shows
    2. Loss percentage check - New scrape must have at least 50% of existing data

    If either check fails, we keep the existing data to prevent data loss.

    Args:
        shows: Newly scraped shows
        existing_shows: Previously saved shows

    Returns:
        True if data was saved, False if existing data was kept
    """
    # Determine if new scrape is good enough to save
    MIN_SHOWS_THRESHOLD = 20  # Require at least 20 shows

    if len(shows) < MIN_SHOWS_THRESHOLD:
        if len(existing_shows) > 0:
            print(f"\n⚠️  WARNING: Only scraped {len(shows)} shows (below threshold of {MIN_SHOWS_THRESHOLD})")
            print(f"   Keeping existing {len(existing_shows)} shows to avoid data loss")
            print(f"   NOT overwriting la-shows.json")
            return False
        else:
            print(f"\n⚠️  WARNING: Only scraped {len(shows)} shows and no existing data")
            print(f"   Saving anyway (better than nothing)")

    # If new scrape is significantly worse than existing, warn but don't save
    if len(existing_shows) > 0:
        loss_threshold = 0.5  # Don't save if we lose more than 50% of shows
        if len(shows) < len(existing_shows) * loss_threshold:
            print(f"\n⚠️  WARNING: New scrape has {len(shows)} shows vs {len(existing_shows)} existing (>{100-loss_threshold*100}% loss)")
            print(f"   Keeping existing shows to avoid data loss")
            print(f"   NOT overwriting la-shows.json")
            return False

    # Save the new data
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'shows': shows
    }

    with open('la-shows.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Saved {len(shows)} shows to la-shows.json")
    return True
```

**Key improvements**:
- Takes `existing_shows` parameter for comparison
- Returns boolean indicating whether data was saved
- Checks minimum threshold (20 shows)
- Checks loss percentage (50%)
- Provides clear warning messages
- Preserves existing data when new scrape is insufficient

### 4. Updated `main()` Function

#### Before (lines 279-328):

```python
def main():
    start_time = time.time()
    print(f"{'='*60}")
    print(f"Los Angeles Comedy Calendar Scraper")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        shows = scrape_all_events()

        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total shows scraped: {len(shows)}")
        print(f"Time elapsed: {elapsed:.1f} seconds")

        if shows:
            # ... venue summary code ...

        if not shows:
            print("\n⚠️  Warning: No shows were scraped.")
            sys.exit(1)

        save_shows(shows)
        print("\n✓ Scraping complete!")
        sys.exit(0)

    except Exception as e:
        print(f"\nSCRAPING FAILED")
        print(f"Error: {e}")
        traceback.print_exc()
        sys.exit(1)
```

#### After (lines 331-391):

```python
def main():
    start_time = time.time()
    print(f"{'='*60}")
    print(f"Los Angeles Comedy Calendar Scraper - IMPROVED")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Load existing shows first (for data protection)
        existing_shows = load_existing_shows()
        if existing_shows:
            print(f"📚 Found {len(existing_shows)} existing shows in la-shows.json\n")

        # Scrape new data
        shows = scrape_all_events()

        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total shows scraped: {len(shows)}")
        print(f"Existing shows: {len(existing_shows)}")
        print(f"Time elapsed: {elapsed:.1f} seconds")

        if shows:
            # ... venue summary code ...

        # Try to save, but protect against bad scrapes
        saved = save_shows(shows, existing_shows)

        if saved:
            print("\n✓ Scraping complete!")
            sys.exit(0)
        else:
            print("\n⚠️  Scrape completed but data not saved (kept existing)")
            sys.exit(0)  # Still exit 0 so workflow doesn't fail

    except Exception as e:
        print(f"\nSCRAPING FAILED")
        print(f"Error: {e}")
        traceback.print_exc()

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

**Key improvements**:
- Loads existing shows before scraping
- Shows existing show count in summary
- Passes existing_shows to save_shows()
- Checks return value from save_shows()
- Exits with 0 even when not saving (preserves data, doesn't fail workflow)
- Added exception handler fallback to preserve existing data

## Protection Logic Details

### Check 1: Minimum Threshold

```python
if len(shows) < 20 and len(existing_shows) > 0:
    # Don't save - keep existing data
```

**Example**: If we had 150 shows and only scraped 8 shows (likely a timeout), don't overwrite.

### Check 2: Loss Percentage

```python
if len(shows) < len(existing_shows) * 0.5:
    # Don't save - losing more than 50% of data
```

**Example**: If we had 200 shows and only scraped 90 shows (55% loss), don't overwrite.

### Exception: First Run

```python
if len(shows) < 20 and len(existing_shows) == 0:
    # Save anyway - better than nothing
```

**Example**: First time running the scraper, even 15 shows is better than 0.

## Testing

Run the test script to verify protection:

```bash
python3 test_data_protection.py
```

Or test manually:

```bash
# Should work normally
python3 la-scraper.py

# Check the output to see:
# - Loaded existing shows count
# - Scraped shows count
# - Whether data was saved or preserved
```

## Exit Codes

| Scenario | Old Behavior | New Behavior |
|----------|--------------|--------------|
| Successful scrape (200 shows) | Exit 0 | Exit 0 |
| Partial scrape (15 shows, have existing 200) | Exit 0, overwrites | Exit 0, keeps existing |
| Failed scrape (exception, have existing data) | Exit 1 | Exit 0, keeps existing |
| Failed scrape (exception, no existing data) | Exit 1 | Exit 1 |

**Key improvement**: Workflows don't fail unnecessarily when we have existing data to fall back on.

## Comparison with Chicago and NY Scrapers

All three scrapers now have **identical** data protection logic:

| Feature | Chicago | NY | LA |
|---------|---------|----|----|
| `load_existing_shows()` | ✓ | ✓ | ✓ |
| Minimum threshold (20 shows) | ✓ | ✓ | ✓ |
| Loss percentage check (50%) | ✓ | ✓ | ✓ |
| Graceful exit (0 when preserving) | ✓ | ✓ | ✓ |
| Exception handler fallback | ✓ | ✓ | ✓ |

## Lines of Code Changed

- **Total lines modified**: ~115 lines
- **Functions added**: 1 (`load_existing_shows`)
- **Functions modified**: 2 (`save_shows`, `main`)
- **Header updated**: 1 docstring

## Benefits

1. No more data loss from partial scrapes
2. Workflows remain stable (don't fail unnecessarily)
3. Clear logging shows when protection triggers
4. Consistent behavior across all scrapers
5. Automatic recovery on next successful scrape

## What to Watch For

After deploying, monitor scraper logs for these messages:

**Normal operation**:
```
📚 Found 187 existing shows in la-shows.json
...
Total shows scraped: 195
✓ Saved 195 shows to la-shows.json
✓ Scraping complete!
```

**Protection triggered (good - data preserved)**:
```
📚 Found 187 existing shows in la-shows.json
...
Total shows scraped: 12
⚠️  WARNING: Only scraped 12 shows (below threshold of 20)
   Keeping existing 187 shows to avoid data loss
   NOT overwriting la-shows.json
⚠️  Scrape completed but data not saved (kept existing)
```

**First run (no existing data)**:
```
Starting Los Angeles Comedy Calendar scraper...
...
Total shows scraped: 15
⚠️  WARNING: Only scraped 15 shows and no existing data
   Saving anyway (better than nothing)
✓ Saved 15 shows to la-shows.json
```

## Rollback Plan

If issues arise, revert to previous version:

```bash
git log la-scraper.py  # Find previous commit
git checkout <commit-hash> la-scraper.py
```

Previous version was simpler but unsafe:
- Always saved data (no protection)
- Could overwrite good data with partial scrapes
- No comparison with existing data

## Next Steps

1. Monitor first few runs of LA scraper
2. Verify protection triggers correctly if scrape fails
3. Confirm workflows don't fail when data is preserved
4. Consider adjusting thresholds if needed:
   - Lower threshold (10) if LA consistently has fewer shows
   - Higher loss tolerance (40%) if site is less stable

## Conclusion

The LA scraper now has the same robust data protection as Chicago and NY scrapers. This prevents data loss from partial or failed scrapes while keeping workflows stable.
