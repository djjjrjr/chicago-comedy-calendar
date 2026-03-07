# Setup Guide for Chicago Comedy Calendar

## ✅ What's Done

- ✅ Beautiful frontend with sleek design
- ✅ Do312 scraper built and ready
- ✅ All 7 venues configured
- ✅ GitHub Pages enabled

## 🚀 Final Steps to Enable Auto-Updates

### Step 1: Add GitHub Actions Workflow

Your GitHub token doesn't have `workflow` permission, so you need to manually add the workflow file:

1. Go to https://github.com/djjjrjr/chicago-comedy-calendar
2. Click **"Add file"** → **"Create new file"**
3. Name it: `.github/workflows/update-schedules.yml`
4. Copy the contents from `update-schedules.yml` in your repo root
5. Click **"Commit new file"**

**The workflow will:**
- Run daily at midnight Chicago time
- Scrape all 7 venues from Do312
- Update `shows.json` automatically
- Deploy to GitHub Pages

### Step 2: Test the Scraper Locally (Optional)

If you want to test before enabling automation:

```bash
# Clone the repo
git clone https://github.com/djjjrjr/chicago-comedy-calendar.git
cd chicago-comedy-calendar

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run the scraper
python scraper.py

# Check the output
cat shows.json
```

### Step 3: Manual Trigger (First Run)

After adding the workflow file:

1. Go to https://github.com/djjjrjr/chicago-comedy-calendar/actions
2. Click **"Update Comedy Schedules"** in the sidebar
3. Click **"Run workflow"** button
4. Click **"Run workflow"** in the dropdown
5. Watch it run! (takes ~2-3 minutes)

### Step 4: Verify It Worked

1. Check the **Actions** tab to see if it completed successfully
2. Look for a new commit from "Comedy Calendar Bot"
3. Visit your live site to see the updated shows!

## 🔧 Troubleshooting

### If the scraper fails:

**Problem:** Do312 changed their website structure

**Solution:** The scraper uses flexible selectors, but if it breaks:
1. Check the Actions log to see the error
2. The scraper looks for `.event-item` or `[class*="event"]`
3. May need to adjust selectors in `scraper.py`

**Problem:** No shows found

**Solutions:**
- Do312 might be blocking GitHub's IP (rare)
- Venue might not have upcoming shows yet
- Check if the venue slug is correct

### If GitHub Actions won't run:

**Problem:** Workflow file not in the right place

**Solution:** Must be at `.github/workflows/update-schedules.yml`
- Note the dot at the start of `.github`
- Must be in `workflows` folder

**Problem:** Permission denied

**Solution:** Make sure the repository has Actions enabled:
1. Go to Settings → Actions → General
2. Set "Workflow permissions" to "Read and write permissions"

## 📊 Monitoring

Once set up, you can:
- View scraper runs in the **Actions** tab
- See the commit history for updates
- Check `shows.json` to see what data was scraped

## 🎨 Next Steps

With automation running, you can:
- Customize the design further
- Add more features (search, filters, etc.)
- Improve date parsing in the scraper
- Add more venues from Do312

## 💡 Tips

- The scraper runs at midnight Chicago time (6 AM UTC)
- You can manually trigger it anytime from the Actions tab
- Shows.json updates automatically push to your site
- GitHub Pages usually updates within 1-2 minutes

## 🆘 Need Help?

If something goes wrong:
1. Check the Actions tab for error logs
2. Look at recent commits to see if updates are happening
3. The scraper is designed to be forgiving - if one venue fails, it continues with the rest

---

**Ready to go live!** Just add that workflow file and you're all set! 🎉
