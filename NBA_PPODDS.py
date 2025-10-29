import requests
import pandas as pd
import sys
print(f"Using Python executable: {sys.executable}")
print(f"Python version: {sys.version}")




def dfs_scraper():
    
    # Fetch data from Prizepicks API
    response = requests.get('https://partner-api.prizepicks.com/projections?per_page=1000')
    prizepicks = response.json()

    # Initialize List and Dictionaries to Store Data
    pplist = []
    library = {}

    for included in prizepicks['included']:
        if 'attributes' in included and 'name' in included['attributes']:
            PPname_id = included['id']
            PPname = included['attributes']['name']
            if 'team' in included['attributes']:
                ppteam = included['attributes']['team']
            else:
                ppteam = 'N/A'
            if 'league' in included['attributes']:
                ppleague = included['attributes']['league']
            else:
                ppleague = 'N/A'
            library[PPname_id] = {'name': PPname, 'team': ppteam, 'league': ppleague}

    for ppdata in prizepicks['data']:
        PPid = ppdata.get('relationships', {}).get('new_player', {}).get('data', {}).get('id', 'N/A')
        PPprop_value = ppdata.get('attributes', {}).get('line_score', 'N/A')
        PPprop_type = ppdata.get('attributes', {}).get('stat_type', 'N/A')
        versus_team = ppdata.get('attributes', {}).get('description', 'N/A')
        odds_type = ppdata.get('attributes', {}).get('odds_type', 'N/A')


        ppinfo = {"name_id": PPid, "Stat": PPprop_type, "Prizepicks": PPprop_value, "Versus": versus_team, "Odds Type": odds_type}
        pplist.append(ppinfo)

    for element in pplist:
        name_id = element['name_id']
        if name_id in library:
            player_data = library[name_id]
            element['Name'] = player_data['name']
            element['Team'] = player_data['team']
            element['League'] = player_data['league']
        else:
            element['Name'] = "Unknown"
            element['Team'] = "N/A"
            element['League'] = "N/A"
        del element['name_id']

    rows = []
    for element in pplist:
        name = element['Name']
        league = element['League']
        team = element['Team']
        stat = element['Stat']
        versus_team = element['Versus']
        odds_type = element['Odds Type']

        prizepicks_value = element['Prizepicks']
        if league == 'NBA' and '+' not in name:
            rows.append((name, league, team, stat, versus_team, prizepicks_value,odds_type))

    df = pd.DataFrame(rows, columns=['Name', 'League', 'Team', 'Stat', 'Versus', 'Prizepicks', 'Odds Type'])
    df.to_csv('NBA_odds_2024.csv',index=False)
    print("Data Saved...")
    return df
    
    
    

dfs_scraper()
