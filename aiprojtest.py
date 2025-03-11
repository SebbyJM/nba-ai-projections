import pandas as pd
import joblib

# Load trained AI model
model_filename = "AI_Projection_Model.pkl"
try:
    model = joblib.load(model_filename)
    print(f"✅ Loaded trained model: {model_filename}")
except FileNotFoundError:
    print(f"❌ Error: {model_filename} not found. Train the model first by running aitrain.py.")
    exit()

# Load today's data
data_filename = "AI_Model_Data.csv"
try:
    df_today = pd.read_csv(data_filename)
    print(f"✅ Loaded today's data: {data_filename}")
except FileNotFoundError:
    print(f"❌ Error: {data_filename} not found. Ensure the file is in the directory.")
    exit()

# Ensure necessary columns exist
features = ["average", "best_point", "recent_form", "edge"]
for col in features:
    if col not in df_today.columns:
        print(f"❌ Error: Missing required column '{col}' in {data_filename}")
        exit()

# Convert columns to numeric
df_today[features] = df_today[features].apply(pd.to_numeric, errors="coerce")

# Drop rows with NaN values
df_today = df_today.dropna(subset=features)

# Generate AI predictions
df_today["AI_Projection"] = model.predict(df_today[features])

# Calculate AI Edge (AI Projection - Vegas Line)
df_today["AI_Edge"] = df_today["AI_Projection"] - df_today["best_point"]

# Save results
output_filename = "AI_Projections_Today.csv"
df_today.to_csv(output_filename, index=False)

print(f"🚀 AI projections saved as: {output_filename}")

# Display top projections sorted by AI edge
top_picks = df_today.sort_values(by="AI_Edge", ascending=False)[["player", "category", "AI_Projection", "best_point", "AI_Edge"]].head(10)
print("\n🔥 Top AI-Driven Picks for Today:\n")
print(top_picks)
