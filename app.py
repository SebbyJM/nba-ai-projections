import streamlit as st
import pandas as pd

# Set title
st.title("🏀 AI NBA Projections Dashboard")

# Load AI projections from CSVs
@st.cache_data
def load_data():
    rebounds = pd.read_csv("AI_Projections_Rebounds.csv")
    points = pd.read_csv("AI_Projections_Points.csv")
    assists = pd.read_csv("AI_Projections_Assists.csv")
    return rebounds, points, assists

rebounds_df, points_df, assists_df = load_data()

# Sidebar menu
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["📊 AI Projections", "🔍 Player Lookup"])

# 1️⃣ **AI Projections Table**
if page == "📊 AI Projections":
    st.subheader("📊 AI-Driven Best Picks")
    category = st.selectbox("Select a category:", ["Points", "Rebounds", "Assists"])

    if category == "Points":
        st.dataframe(points_df)
    elif category == "Rebounds":
        st.dataframe(rebounds_df)
    else:
        st.dataframe(assists_df)

# 2️⃣ **Player Lookup**
elif page == "🔍 Player Lookup":
    st.subheader("🔍 Search for a Player's Data")
    player_name = st.text_input("Enter player name:")

    if player_name:
        df_list = [rebounds_df, points_df, assists_df]
        results = pd.concat([df[df["player"].str.contains(player_name, case=False, na=False)] for df in df_list])

        if not results.empty:
            st.dataframe(results)
        else:
            st.warning("Player not found. Try another name.")