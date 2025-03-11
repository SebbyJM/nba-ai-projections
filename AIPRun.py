import pandas as pd
import joblib

def generate_projections(data_file, model_file, output_file):
    print(f"📂 Loading data from: {data_file}")

    # Load data
    df = pd.read_csv(data_file)
    print(f"✅ Data loaded! Shape: {df.shape}")

    # Ensure numeric conversion
    numeric_cols = ["best_over_odds", "best_under_odds", "best_point", "average"] + \
                   [f"game {i}" for i in range(1, 11)]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Load model
    print(f"📊 Data for prediction: {df.shape}")
    model = joblib.load(model_file)
    print(f"✅ Model loaded: {model_file}")

    # Select only numeric columns for prediction
    feature_cols = [col for col in numeric_cols if col in df.columns]
    df_features = df[feature_cols]

    # Ensure feature names match (based on model training)
    if hasattr(model, "feature_names_in_"):
        model_features = model.feature_names_in_
        df_features = df_features[model_features]  # Reorder to match training

    # Generate AI projections
    df["AI_Projection"] = model.predict(df_features)

    # Calculate AI Edge
    df["AI_Edge"] = df["AI_Projection"] - df["best_point"]

    # Save the updated file
    df.to_csv(output_file, index=False)
    print(f"🚀 AI projections saved as: {output_file}")

# Run for all three categories
generate_projections("Merged_Rebounds.csv", "AI_Model_Rebounds.pkl", "AI_Projections_Rebounds.csv")
generate_projections("Merged_Assists.csv", "AI_Model_Assists.pkl", "AI_Projections_Assists.csv")
generate_projections("Merged_Points.csv", "AI_Model_Points.pkl", "AI_Projections_Points.csv")