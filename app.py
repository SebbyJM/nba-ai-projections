import streamlit as st
import pandas as pd

# Load AI projection data
df = pd.read_csv("AI_Projections_Today.csv")  # Change to the correct file

st.title("📊 NBA AI Projections")

# Search for a player
player_name = st.text_input("Enter player name:")

if player_name:
    filtered_df = df[df["player"].str.contains(player_name, case=False, na=False)]
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No data found for this player.")

# Show top AI projections
st.subheader("🔥 Top AI Projections")
st.dataframe(df.sort_values(by="AI_Edge", ascending=False).head(10))