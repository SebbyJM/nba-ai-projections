import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

# Function to train an AI model for projections
def train_ai_model(input_file, model_file):
    # Load the merged dataset
    df = pd.read_csv(input_file)

    # Select relevant features
    features = ["average", "best_point", "best_over_odds", "best_under_odds"]
    target = "AI_Projection"

    # Handle missing values
    df = df.dropna(subset=features)

    # Create AI projection target (use average as baseline)
    df[target] = df["average"] * 1.05  # Adjusting slightly upward as an initial guess

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Define model pipeline (scaling + regression)
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Train the model
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, model_file)

    print(f"✅ Model trained and saved: {model_file}")

# Train models for each category
train_ai_model("Merged_Rebounds.csv", "AI_Model_Rebounds.pkl")
train_ai_model("Merged_Points.csv", "AI_Model_Points.pkl")
train_ai_model("Merged_Assists.csv", "AI_Model_Assists.pkl")
