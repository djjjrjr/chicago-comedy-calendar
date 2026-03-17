# Fix Node.js 24 Deprecation Warning

GitHub Actions is showing a deprecation warning about Node.js 20. Here's how to fix it:

## The Warning

```
Node.js 20 actions are deprecated. The following actions are running on Node.js 20 and may not work as expected: actions/checkout@v4, actions/upload-artifact@v4.
```

## The Fix

Add this environment variable to both workflow files:

### For `.github/workflows/update_schedules.yml`

Find this section (around line 12-14):

```yaml
jobs:
  scrape-and-update:
    runs-on: ubuntu-latest

    steps:
```

Change it to:

```yaml
jobs:
  scrape-and-update:
    runs-on: ubuntu-latest
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

    steps:
```

### For `.github/workflows/update_venue_info.yml`

Find this section:

```yaml
jobs:
  scrape-venue-info:
    runs-on: ubuntu-latest

    steps:
```

Change it to:

```yaml
jobs:
  scrape-venue-info:
    runs-on: ubuntu-latest
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

    steps:
```

## What This Does

- Forces the workflow to use Node.js 24 instead of Node.js 20
- Prevents deprecation warnings
- Ensures compatibility when Node.js 24 becomes the default on June 2, 2026

## How to Apply

1. Go to your GitHub repository
2. Navigate to `.github/workflows/update_schedules.yml`
3. Click the pencil icon to edit
4. Add the `env:` section as shown above
5. Commit the changes
6. Repeat for `update_venue_info.yml` (if you've uploaded it)

That's it! The warning will disappear on the next workflow run.
