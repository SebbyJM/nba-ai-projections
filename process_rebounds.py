import pandas as pd

# List of input and output file names
files = {
    "NBA STATS - REBOUNDS.csv": "Cleaned_Best_Odds_Rebounds.csv",
    "NBA STATS - ASSISTS.csv": "Cleaned_Best_Odds_Assists.csv",
    "NBA STATS - POINTS.csv": "Cleaned_Best_Odds_Points.csv"
}

# Function to clean and extract best odds
def process_file(file_path, output_file):
    try:
        # Load the CSV file and manually define column names
        df = pd.read_csv(file_path, names=["label", "description", "price", "point"], header=None)

        # Remove any leading/trailing spaces in column names
        df.columns = df.columns.str.strip().str.lower()

        # Ensure price column is numeric
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

        # Function to extract the best odds
        def get_best_odds(group):
            best_over = group[group["label"] == "Over"].nsmallest(1, "price")  # Most negative Over
            best_under = group[group["label"] == "Under"]
            best_under = best_under.loc[best_under["price"].abs().idxmin()] if not best_under.empty else None  # Closest to 0 Under

            return pd.DataFrame({
                "Player": [group["description"].iloc[0]],
                "Best_Over_Odds": [best_over["price"].values[0] if not best_over.empty else None],
                "Best_Under_Odds": [best_under["price"] if best_under is not None else None],
                "Best_Point": [group["point"].iloc[0]]
            })

        # Apply function to group by player
        cleaned_df = df.groupby("description", group_keys=False).apply(get_best_odds).reset_index(drop=True)

        # Ensure "Best_Point" retains decimal values properly
        def format_point(x):
            try:
                return str(float(x)) if pd.notna(x) else ""
            except ValueError:
                return str(x)

        # Apply formatting
        cleaned_df["Best_Over_Odds"] = cleaned_df["Best_Over_Odds"].apply(lambda x: str(int(x)) if pd.notna(x) and x % 1 == 0 else str(x))
        cleaned_df["Best_Under_Odds"] = cleaned_df["Best_Under_Odds"].apply(lambda x: str(int(x)) if pd.notna(x) and x % 1 == 0 else str(x))
        cleaned_df["Best_Point"] = cleaned_df["Best_Point"].apply(format_point)

        # Save the cleaned data as a new CSV file
        cleaned_df.to_csv(output_file, index=False)

        print(f"✅ Cleaned file saved as: {output_file}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

# Loop through all three files and clean them
for input_file, output_file in files.items():
    process_file(input_file, output_file)