import requests
import pandas as pd
import sys

print(f"Using Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

def dfs_scraper():
    # Fetch data from PrizePicks API (NBA: league_id=7)
    url = "https://api.prizepicks.com/projections?league_id=7&per_page=1000"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    print(f"API Status: {response.status_code}")  # Diagnostic: 200=win
    if response.status_code != 200:
        print(f"API hiccup: {response.text[:200]}")  # Error peek
        return []
    prizepicks = response.json()
    print(f"Fetched {len(prizepicks.get('data', []))} projections")  # Count check
    
    # Initialize lists/dicts to store data
    plist = []  # Projections list
    library = {}  # Player library: ID → info
    
    # Build library from included (players)
    for included in prizepicks.get('included', []):
        inc_id = included['id']
        attrs = included['attributes']
        name = attrs.get('name', 'N/A')
        team = attrs.get('team', 'N/A')
        league = attrs.get('league', 'N/A')
        library[inc_id] = {'name': name, 'team': team, 'league': league}
    
    # Parse projections from data
    for proj in prizepicks.get('data', []):
        attrs = proj['attributes']
        stat_type = attrs.get('statType', attrs.get('stat_type', 'N/A'))  # Flex key
        line = attrs.get('line', 'N/A')  # Prop line
        
        # Link to player via relationship
        if 'relationships' in proj and 'player' in proj['relationships']:
            player_id = proj['relationships']['player']['data']['id']
            if player_id in library:
                player_info = library[player_id]
                # NBA filter—only hoops for 2025!
                if player_info['league'] == 'NBA':
                    entry = {
                        'player': player_info['name'],
                        'team': player_info['team'],
                        'league': player_info['league'],
                        'stat_type': stat_type,
                        'line': line
                    }
                    plist.append(entry)
    
    return plist

if __name__ == "__main__":
    plist = dfs_scraper()
    if plist:
        df = pd.DataFrame(plist)
        df.to_csv('NBA_odds_2025.csv', index=False)
        print(f"Data Saved... {len(df)} NBA props forged! 🏀")
    else:
        print("No data—API dry? Check logs above.")
