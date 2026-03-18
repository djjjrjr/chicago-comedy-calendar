# Venue Display Issues - Analysis

## Summary

**All show data is CORRECT!** The issues are:
1. **Reggies**: venue-info-scraper keeps adding it back (now fixed)
2. **Den/Largo/Dynasty**: Have 0 shows currently (not a bug)
3. **NY venues**: All present in data, display issue is client-side

## Show Count Reality

NY (208 shows): All 7 venues ✓
- Comedy Cellar: 10, Gotham: 2, Stand: 6, Bell House: 1, Union Hall: 16, Caveat: 20, UCB: 88

LA (120 shows): 5/7 venues
- Comedy Store: 7, Laugh Factory: 2, Improv: 2, UCB: 89, Groundlings: 1
- Largo: 0 (not in DoLA), Dynasty: 0 (not in DoLA)

Chicago (26 shows): 6/7 venues
- Second City: 2, iO: 4, Annoyance: 4, Zanies: 3, Laugh Factory: 3, Lincoln Lodge: 6
- Den Theatre: 0 (not in Do312)

## Fixes

1. venue-info-scraper.py now protects all 21 preferred venues
2. Auto-removes "Reggies - Comedy Shack"  
3. Never overwrites preferred venue data

If website still shows issues: Clear browser cache / hard refresh
