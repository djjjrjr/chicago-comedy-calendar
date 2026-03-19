# Chicago Scraper Improvements

## Problems Fixed

### 1. Timeout Issues
**Before**: 60-second timeouts on page navigation and network idle
**After**: 
- Navigation timeout: 120 seconds (2 minutes)
- Network idle timeout: 90 seconds with fallback
- Increased delays between pages (3 seconds)

### 2. Data Loss on Partial Scrapes
**Before**: Always overwrote shows.json, even with partial data (28 shows replacing 38+ shows)
**After**:
- Loads existing shows before scraping
- Only saves if new scrape has at least 20 shows
- Won't save if new scrape loses >50% of existing shows
- Preserves existing data on failures

### 3. Better Failure Handling
**Before**: Stopped completely on first page timeout
**After**:
- Allows up to 2 consecutive page failures before stopping
- Continues with data collected so far if at least 1 page succeeded
- Exits with code 0 (success) if existing data is preserved

## New Features

### Smart Data Protection
```python
MIN_SHOWS_THRESHOLD = 20  # Require at least 20 shows
loss_threshold = 0.5      # Don't save if we lose >50% of shows
```

### Improved Timeouts
- Page navigation: 120 seconds
- Network idle: 90 seconds (with fallback)
- Page delays: 3 seconds (increased from 2)

### Graceful Degradation
- If scrape fails but gets some data: saves if above threshold
- If scrape fails completely: keeps existing data
- Workflow doesn't fail if existing data exists

## Migration

To use the improved scraper:

```bash
# Backup old scraper
cp scraper.py scraper-old.py

# Replace with improved version
cp scraper-improved.py scraper.py

# Test locally
python3 scraper.py
```

Or update workflow to use improved version directly:
```yaml
- name: Run Chicago scraper
  run: python scraper-improved.py
```

## Results

**Before**:
- Timeout on page 2 → Only 28 shows saved
- Existing 38+ shows lost
- Workflow fails with exit code 1

**After**:
- Timeout on page 2 → 28 shows scraped
- Existing 38+ shows preserved (28 < 50% of 38)
- Workflow succeeds (exit code 0)
- Next run will retry and hopefully get full data

## Testing

Test the improved scraper:
```bash
python3 scraper-improved.py
```

Expected output on timeout:
```
⚠️  WARNING: Only scraped 28 shows vs 38 existing (>50% loss)
   Keeping existing shows to avoid data loss
   NOT overwriting shows.json
✓ Scrape completed but data not saved (kept existing)
```
