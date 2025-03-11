import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib  # To save and load the trained model

# Load AI training data
try:
    df = pd.read_csv("AI_Model_Data.csv")
    print("✅ AI_Model_Data.csv successfully loaded!")
except FileNotFoundError:
    print("❌ Error: AI_Model_Data.csv not found. Make sure the file exists in the directory.")
    exit()

# Select relevant features for ML training
features = ["average", "best_point", "recent_form", "edge"]

# Ensure the features exist in the dataframe
for col in features:
    if col not in df.columns:
        print(f"❌ Error: Missing required column '{col}' in AI_Model_Data.csv")
        exit()

# Convert columns to numeric (handle missing data)
df[features] = df[features].apply(pd.to_numeric, errors="coerce")

# Drop rows with NaN values (important for clean training)
df = df.dropna(subset=features)

# Define target variable (AI-based projection)
X = df[features]
y = df["projection"]  # Target: Predicting player's performance

# Split data into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model accuracy
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"✅ Model Trained! Mean Absolute Error: {mae:.2f}")

# Save the trained model for future predictions
joblib.dump(model, "AI_Projection_Model.pkl")
print("✅ Model saved as AI_Projection_Model.pkl")
