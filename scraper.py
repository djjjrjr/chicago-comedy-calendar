#!/usr/bin/env python3
"""
Wrapper for Chicago scraper - calls the actual scraper in scrapers/chicago/
"""
import subprocess
import sys

result = subprocess.run(['bash', 'scrapers/chicago/scrape-all.sh'], cwd='.')
sys.exit(result.returncode)
