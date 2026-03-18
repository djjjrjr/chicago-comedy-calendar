#!/usr/bin/env python3
"""Fix venue-info.json with correct data"""
import json
import re

CORRECT_VENUES = {
    'The Second City': {'address': '1616 N Wells St, Chicago, IL 60614', 'phone': '(312) 337-3992', 'website': 'https://www.secondcity.com'},
    'iO Theater': {'address': '1501 N Kingsbury St, Chicago, IL 60642', 'phone': '(312) 929-2401', 'website': 'https://ioimprov.com/chicago'},
    'Annoyance Theatre': {'address': '851 W Belmont Ave, Chicago, IL 60657', 'phone': '(773) 697-9693', 'website': 'https://theannoyance.com'},
    'Zanies Comedy Club': {'address': '1548 N Wells St, Chicago, IL 60610', 'phone': '(312) 337-4027', 'website': 'https://chicago.zanies.com'},
    'Laugh Factory': {'address': '3175 N Broadway, Chicago, IL 60657', 'phone': '(773) 327-3175', 'website': 'https://chicago.laughfactory.com'},
    'The Lincoln Lodge': {'address': '2424 N Lincoln Ave, Chicago, IL 60614', 'phone': '(773) 868-0608', 'website': 'https://www.lincolnlodge.com'},
    'Den Theatre': {'address': '1331 N Milwaukee Ave, Chicago, IL 60622', 'phone': '(773) 697-3830', 'website': 'https://www.dentheatre.com'},
    'Comedy Cellar': {'address': '117 MacDougal St, New York, NY 10012', 'phone': '(212) 254-3480', 'website': 'https://www.comedycellar.com', 'borough': 'Manhattan'},
    'Gotham Comedy Club': {'address': '208 W 23rd St, New York, NY 10011', 'phone': '(212) 367-9000', 'website': 'https://gothamcomedyclub.com', 'borough': 'Manhattan'},
    'The Stand': {'address': '116 E 16th St, New York, NY 10003', 'phone': '(212) 933-3950', 'website': 'https://thestandnyc.com', 'borough': 'Manhattan'},
    'The Bell House': {'address': '149 7th St, Brooklyn, NY 11215', 'phone': '(718) 643-6510', 'website': 'https://www.thebellhouseny.com', 'borough': 'Brooklyn'},
    'Union Hall': {'address': '702 Union St, Brooklyn, NY 11215', 'phone': '(718) 638-4400', 'website': 'https://www.unionhallny.com', 'borough': 'Brooklyn'},
    'Caveat': {'address': '21 A Clinton St, New York, NY 10002', 'phone': '(212) 228-2100', 'website': 'https://caveat.nyc', 'borough': 'Manhattan'},
    'UCB Theatre': {'address': '242 E 14th St, New York, NY 10003', 'phone': '(212) 366-9231', 'website': 'https://ucbcomedy.com/shows/new-york/', 'borough': 'Manhattan'},
    'The Comedy Store': {'address': '8433 Sunset Blvd, West Hollywood, CA 90069', 'phone': '(323) 650-6268', 'website': 'https://www.thecomedystore.com'},
    'The Laugh Factory': {'address': '8001 Sunset Blvd, Los Angeles, CA 90046', 'phone': '(323) 656-1336', 'website': 'https://laughfactory.com/clubs/hollywood'},
    'Hollywood Improv': {'address': '8162 Melrose Ave, Los Angeles, CA 90046', 'phone': '(323) 651-2583', 'website': 'https://www.improv.com/hollywood'},
    'UCB FRANKLIN': {'address': '5919 Franklin Ave, Los Angeles, CA 90028', 'phone': '(323) 908-8702', 'website': 'https://ucbcomedy.com/shows/los-angeles/'},
    'Dynasty Typewriter': {'address': '2511 Wilshire Blvd, Los Angeles, CA 90057', 'phone': '(213) 915-1929', 'website': 'https://dynastytypewriter.com'},
    'Largo at the Coronet': {'address': '366 N La Cienega Blvd, Los Angeles, CA 90048', 'phone': '(310) 855-0350', 'website': 'https://largo-la.com'},
    'The Groundlings Theatre': {'address': '7307 Melrose Ave, Los Angeles, CA 90046', 'phone': '(323) 934-4747', 'website': 'https://www.groundlings.com'}
}

try:
    with open('venue-info.json') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {'venues': {}, 'lastUpdated': None}

venues = data.get('venues', {})
for name, info in CORRECT_VENUES.items():
    venues[name] = info
    print(f"✓ {name}")

data['venues'] = venues
with open('venue-info.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Fixed {len(CORRECT_VENUES)} venues with boroughs!")
