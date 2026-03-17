#!/bin/bash
# Comedy Cellar FAST Scraper - Keeps browser open, just changes dropdown

echo "🎭 Starting Comedy Cellar FAST scraper..."

MAX_DAYS=${MAX_DAYS:-14}
echo "📅 Scraping $MAX_DAYS days..."

# Open browser once
agent-browser open https://www.comedycellar.com/new-york-line-up/
sleep 3

echo '[]' > /tmp/cc-all.json

for i in $(seq 0 $((MAX_DAYS - 1))); do
    echo "Day $((i+1))/$MAX_DAYS..."

    # Get date value for this index
    DATE_VAL=$(agent-browser eval "document.querySelector('select').options[$i]?.value || null")

    if [ "$DATE_VAL" == "null" ]; then
        break
    fi

    # Select date
    agent-browser select "select" "$DATE_VAL" > /dev/null
    sleep 2

    # Scrape shows
    agent-browser eval "
const shows=[];const s=document.querySelector('select');const d=s.options[s.selectedIndex].text;const m=d.match(/(\\w+)\\s+(\\w+)\\s+(\\d+),\\s+(\\d{4})/);let iso=new Date().toISOString();if(m){iso=new Date(\`\${m[2]} \${m[3]}, \${m[4]}\`).toISOString()}const txt=document.body.innerText;[...txt.matchAll(/(\\d+:\\d+)\\s*([ap]m)\\s+show-([^\\n\\+]+)/gi)].forEach(m=>{const t=m[1]+' '+m[2];const v=m[3].trim();let vn='Comedy Cellar',ti='Comedy Showcase';if(v.includes('MacDougal'))vn='Comedy Cellar - MacDougal Street';else if(v.includes('Village'))vn='Comedy Cellar - Village Underground';else if(v.includes('Fat Black')||v.includes('FBPC'))vn=v.includes('Bar')?'Comedy Cellar - Fat Black Pussycat (Bar)':v.includes('Lounge')?'Comedy Cellar - Fat Black Pussycat (Lounge)':'Comedy Cellar - Fat Black Pussycat';const sp=v.match(/([^:]+):/);if(sp)ti=sp[1].trim();shows.push({title:ti,venue:vn,date:iso,time:t,description:'Lineup TBA',url:'https://www.comedycellar.com/reservations-newyork/'})});JSON.stringify(shows);
" > /tmp/cc-day-$i.json

    COUNT=$(cat /tmp/cc-day-$i.json 2>/dev/null | grep -o '"title"' | wc -l)
    echo "  ✓ $COUNT shows"
done

agent-browser close

# Combine all
python3 << 'EOF'
import json, glob
from datetime import datetime
shows = []
for f in sorted(glob.glob('/tmp/cc-day-*.json')):
    try:
        with open(f) as file:
            shows.extend(json.loads(file.read()))
    except: pass
with open('comedy-cellar-shows.json', 'w') as f:
    json.dump({'shows': shows, 'lastUpdated': datetime.now().isoformat()+'Z', 'venue': 'Comedy Cellar', 'totalShows': len(shows)}, f, indent=2)
print(f'\n✅ {len(shows)} shows saved!')
EOF

rm -f /tmp/cc-day-*.json /tmp/cc-all.json
