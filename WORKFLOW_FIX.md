# Fix Scraper Workflow - Add System Dependencies

The scraper is failing because Playwright needs system libraries to run Chromium in GitHub Actions.

## What to do:

Edit `.github/workflows/update_schedules.yml` on GitHub and add this step **after line 20** (after "Set up Python"):

```yaml
      - name: Install system dependencies for Playwright
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            libnss3 \
            libnspr4 \
            libatk1.0-0 \
            libatk-bridge2.0-0 \
            libcups2 \
            libdrm2 \
            libxkbcommon0 \
            libxcomposite1 \
            libxdamage1 \
            libxfixes3 \
            libxrandr2 \
            libgbm1 \
            libasound2
```

## Complete section should look like:

```yaml
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install system dependencies for Playwright
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            libnss3 \
            libnspr4 \
            libatk1.0-0 \
            libatk-bridge2.0-0 \
            libcups2 \
            libdrm2 \
            libxkbcommon0 \
            libxcomposite1 \
            libxdamage1 \
            libxfixes3 \
            libxrandr2 \
            libgbm1 \
            libasound2

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
```

## Why this is needed:

Playwright's Chromium browser needs these Linux libraries to run in GitHub Actions. Without them, the browser silently fails to launch, causing the scraper to find 0 shows.

## To edit on GitHub:

1. Go to https://github.com/djjjrjr/chicago-comedy-calendar/blob/main/.github/workflows/update_schedules.yml
2. Click the pencil icon (Edit this file)
3. Add the system dependencies step as shown above
4. Commit directly to main
5. Run the workflow again

This should fix the scraper!
