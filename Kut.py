import pandas as pd

# List of input files and their corresponding L10 stats files
files = {
    "Cleaned_Best_Odds_Rebounds.csv": "rebounds_l10.csv",
    "Cleaned_Best_Odds_Assists.csv": "assists_l10.csv",
    "Cleaned_Best_Odds_Points.csv": "points_l10.csv"
}

# Function to calculate projections
def process_projection(odds_file, l10_file, output_file):
    try:
        # Load the cleaned odds file
        df_odds = pd.read_csv(odds_file)

        # Load the L10 file
        df_l10 = pd.read_csv(l10_file)

        # Ensure column names are clean
        df_odds.columns = df_odds.columns.str.strip().str.lower()
        df_l10.columns = df_l10.columns.str.strip().str.lower()

        # Ensure "average" column exists in L10 file
        if "average" not in df_l10.columns:
            raise KeyError(f"'average' column not found in {l10_file}")

        # Merge both datasets on player name
        merged_df = df_odds.merge(df_l10[['player', 'average']], left_on='player', right_on='player', how='left')

        # Convert average column to numeric
        merged_df["average"] = pd.to_numeric(merged_df["average"], errors="coerce")

        # Convert best point column to numeric (Vegas line)
        merged_df["best_point"] = pd.to_numeric(merged_df["best_point"], errors="coerce")

        # Calculate projection as the midpoint between L10 average and Vegas Line
        merged_df["projection"] = (merged_df["average"] + merged_df["best_point"]) / 2

        # Save the projection file
        merged_df.to_csv(output_file, index=False)

        print(f"✅ Projection file saved as: {output_file}")

    except Exception as e:
        print(f"❌ Error processing {odds_file}: {e}")

# Loop through all three categories (Rebounds, Assists, Points)
for odds_file, l10_file in files.items():
    output_file = f"Projections_{odds_file.split('_')[-1]}"  # Naming output file dynamically
    process_projection(odds_file, l10_file, output_file)
