import requests
import pandas as pd
import sys

print(f"Using Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

def dfs_scraper():
    # Fetch data from PrizePicks API
    url = "https://partner-api.prizepicks.com/projections?per_page=1000"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"API hiccup: {response.status_code}")
        return []
    prizepicks = response.json()
    
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
        stat_type = attrs.get('statType', 'N/A')  # e.g., 'points'
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
        print("No data—API dry?")
