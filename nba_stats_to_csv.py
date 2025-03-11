import pandas as pd
import requests
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from datetime import datetime
import time
import unicodedata

# NBA Stats API headers to avoid getting blocked
HEADERS = {
    "Host": "stats.nba.com",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "Referer": "https://www.nba.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9"
}

def normalize_name(name):
    """ Normalize player name to match API format (handles accents) """
    return unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8')

def get_player_id(player_name):
    """ Fetches the player's ID from NBA Stats API. """
    player_dict = players.get_players()
    normalized_name = normalize_name(player_name)

    for player in player_dict:
        if normalized_name.lower() == normalize_name(player['full_name']).lower():
            return player['id']
    
    return None  # Player not found

def get_last_10_games(player_id, up_to_date):
    """ Fetches the last 10 games of the player up to the specified date. """
    url = "https://stats.nba.com/stats/playergamelogs"
    params = {
        "PlayerID": player_id,
        "Season": "2024-25",  # Adjust if necessary
        "SeasonType": "Regular Season"
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"⚠️ API Request Failed for Player {player_id}! Status Code: {response.status_code}")
        return pd.DataFrame()

    data = response.json()

    if "resultSets" not in data or not data["resultSets"][0]["rowSet"]:
        print(f"⚠️ No game data returned for player ID {player_id}!")
        return pd.DataFrame()

    # Convert response to DataFrame
    games_df = pd.DataFrame(data["resultSets"][0]["rowSet"], columns=data["resultSets"][0]["headers"])

    # Convert GAME_DATE to datetime with proper handling
    try:
        games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'], errors='coerce')
    except Exception:
        games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'], infer_datetime_format=True, errors='coerce')

    # Drop rows where GAME_DATE couldn't be parsed
    games_df = games_df.dropna(subset=['GAME_DATE'])

    # Filter games up to the specified date
    games_df = games_df[games_df['GAME_DATE'] <= up_to_date]

    # Sort by date and take the last 10 games
    games_df = games_df.sort_values(by='GAME_DATE', ascending=False).head(10)

    return games_df

def process_players(file_path):
    """ Reads a list of player names from a file and processes them. """
    up_to_date = datetime.today()  # Always fetch up to today's date

    # Read player names from file
    with open(file_path, 'r') as file:
        players_list = [line.strip() for line in file.readlines()]

    # Initialize data structures for combined stats
    stats_data = {
        "points": [],
        "assists": [],
        "rebounds": []
    }

    for player_name in players_list:
        print(f"🚀 Processing {player_name}...")
        player_id = get_player_id(player_name)

        if not player_id:
            print(f"❌ Player '{player_name}' not found! (Check spelling or try using full name)")
            continue

        games_df = get_last_10_games(player_id, up_to_date)

        if games_df.empty:
            print(f"⚠️ No game data found for {player_name}! Skipping...")
            continue

        # Extract stats
        stats = {
            "points": "PTS",
            "assists": "AST",
            "rebounds": "REB"
        }

        for stat_name, column in stats.items():
            # Get the last 10 games' stats
            values = games_df[column].tolist()

            # Calculate average and round to 2 decimal places
            average_value = round(sum(values) / len(values), 2) if values else 0

            # Ensure 10 columns even if fewer games available
            while len(values) < 10:
                values.append(None)

            # Append row to the respective stat list
            stats_data[stat_name].append([player_name] + values + [average_value])

        # Small delay to prevent API rate limits
        time.sleep(2)

    # Save each stat as a combined CSV file
    for stat_name, data in stats_data.items():
        if data:  # Only save if there's data
            df = pd.DataFrame(data, columns=["Player"] + [f"Game {i+1}" for i in range(10)] + ["Average"])
            file_name = f"{stat_name}_L10.csv"
            df.to_csv(file_name, index=False)
            print(f"✅ Saved {file_name}")

    print("✅ All players processed successfully!")

if __name__ == "__main__":
    process_players("players.txt")