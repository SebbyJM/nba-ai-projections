import pandas as pd
import os

# Define file paths
files = {
    "Assists": "NBA STATS - ASSISTS.csv",
    "Rebounds": "NBA STATS - REBOUNDS.csv",
    "Points": "NBA STATS - POINTS.csv"
}

output_files = {
    "Assists": "Cleaned_Assists.csv",
    "Rebounds": "Cleaned_Rebounds.csv",
    "Points": "Cleaned_Points.csv"
}

# Function to process odds and find best over/under for each player
def process_odds(stat_type, file_name, output_file):
    if not os.path.exists(file_name):
        print(f"⚠️ Missing file: {file_name}")
        return
    
    try:
        # Read CSV with NO header (since format can vary)
        df = pd.read_csv(file_name, header=None)

        # Expected 4 columns: Bet type (Over/Under), Player, Odds, Line
        if df.shape[1] != 4:
            print(f"❌ Error: {file_name} does not have 4 columns as expected.")
            return
        
        # Assign correct column names
        df.columns = ["bet_type", "player", "odds", "line"]

        # Convert odds and line to numeric
        df["odds"] = pd.to_numeric(df["odds"], errors="coerce")
        df["line"] = pd.to_numeric(df["line"], errors="coerce")

        # Separate Over and Under bets
        over_df = df[df["bet_type"].str.lower() == "over"]
        under_df = df[df["bet_type"].str.lower() == "under"]

        # Get best Over and Under odds per player
        best_over = over_df.loc[over_df.groupby("player")["odds"].idxmax(), ["player", "line", "odds"]]
        best_under = under_df.loc[under_df.groupby("player")["odds"].idxmax(), ["player", "line", "odds"]]

        # Rename columns properly
        best_over.rename(columns={"odds": "best_over_odds"}, inplace=True)
        best_under.rename(columns={"odds": "best_under_odds"}, inplace=True)

        # Merge Over and Under into final dataset
        final_df = pd.merge(best_over, best_under, on=["player", "line"], how="outer")

        # Save cleaned file
        final_df.to_csv(output_file, index=False)
        print(f"✅ Cleaned odds saved: {output_file}")

    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")

# Process all three stat categories
for stat, file in files.items():
    process_odds(stat, file, output_files[stat])

print("🎯 Odds cleaning completed successfully!")