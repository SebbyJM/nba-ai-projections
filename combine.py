import pandas as pd

# Function to merge cleaned odds with L10 stats
def merge_odds_l10(odds_file, l10_file, output_file, category):
    # Load the cleaned odds data
    df_odds = pd.read_csv(odds_file)

    # Load the L10 stats
    df_l10 = pd.read_csv(l10_file)

    # Normalize column names
    df_odds.columns = df_odds.columns.str.strip().str.lower()
    df_l10.columns = df_l10.columns.str.strip().str.lower()

    # Merge the datasets on "player"
    merged_df = pd.merge(df_odds, df_l10, on="player", how="left")

    # Add category column
    merged_df["category"] = category

    # Save the merged dataset
    merged_df.to_csv(output_file, index=False)

    print(f"✅ Merged file saved as: {output_file}")

# Process all three categories
merge_odds_l10("Cleaned_Best_Odds_Rebounds.csv", "rebounds_l10.csv", "Merged_Rebounds.csv", "Rebounds")
merge_odds_l10("Cleaned_Best_Odds_Points.csv", "points_l10.csv", "Merged_Points.csv", "Points")
merge_odds_l10("Cleaned_Best_Odds_Assists.csv", "assists_l10.csv", "Merged_Assists.csv", "Assists")
