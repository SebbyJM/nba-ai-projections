import pandas as pd
import joblib

def generate_projections(input_csv, model_file, output_csv):
    """
    Loads a merged dataset, applies the trained AI model, and saves AI projections.
    """
    print(f"📂 Loading data from: {input_csv}")
    df = pd.read_csv(input_csv)
    print(f"✅ Data loaded! Shape: {df.shape}")

    # Load trained model
    model = joblib.load(model_file)
    print(f"✅ Model loaded: {model_file}")

    # Drop non-numeric columns
    drop_cols = ["player", "category"]
    df_numeric = df.drop(columns=drop_cols, errors="ignore")

    # Convert all remaining columns to numeric
    df_numeric = df_numeric.apply(pd.to_numeric, errors="coerce")

    # Ensure correct feature order
    trained_features = model.feature_names_in_
    df_numeric = df_numeric[trained_features]
    print(f"📊 Data for prediction: {df_numeric.shape}")

    # Make AI projections
    df["AI_Projection"] = model.predict(df_numeric)

    # Ensure 'best_point' is float for AI_Edge calculation
    df["best_point"] = pd.to_numeric(df["best_point"], errors="coerce")

    # Compute AI Edge (Difference between projection & betting line)
    df["AI_Edge"] = df["AI_Projection"] - df["best_point"]
    print("✅ AI Projections calculated!")

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"✅ AI Projections saved: {output_csv}")

# Run for all three datasets
generate_projections("Merged_Rebounds.csv", "AI_Model_Rebounds.pkl", "AI_Projections_Rebounds.csv")
generate_projections("Merged_Assists.csv", "AI_Model_Assists.pkl", "AI_Projections_Assists.csv")
generate_projections("Merged_Points.csv", "AI_Model_Points.pkl", "AI_Projections_Points.csv")

print("🎯 AI Projections for all categories completed!")