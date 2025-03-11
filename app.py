import streamlit as st
import pandas as pd
import random

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
page = st.sidebar.radio("Go to", ["📊 AI Projections", "🎯 AI's Best 2-Man Bet", "🔍 Player Lookup"])

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

# 2️⃣ **AI-Generated Best 2-Man Bet**
elif page == "🎯 AI's Best 2-Man Bet":
    st.subheader("🎯 AI’s Top 2-Man Bet Recommendation")

    # Combine all categories into one DataFrame
    all_data = pd.concat([
        points_df.assign(category="Points"),
        rebounds_df.assign(category="Rebounds"),
        assists_df.assign(category="Assists")
    ])

    # Select top picks based on AI Edge
    top_picks = all_data.sort_values(by="AI_Edge", ascending=False).head(10)

    # Choose the best 2-man bet from different categories (if possible)
    best_bet = []
    seen_categories = set()

    for _, row in top_picks.iterrows():
        if row["category"] not in seen_categories:
            best_bet.append(row)
            seen_categories.add(row["category"])

        if len(best_bet) == 2:  # Stop once we have two players
            break

    # Display best bet with reasoning
    if len(best_bet) == 2:
        st.write(f"🔥 **Best Bet:** {best_bet[0]['player']} ({best_bet[0]['category']}) & {best_bet[1]['player']} ({best_bet[1]['category']})")

        st.write(f"**Why?**")
        st.write(f"- **{best_bet[0]['player']}** has an AI edge of **{best_bet[0]['AI_Edge']}**, meaning their projection is well above the betting line.")
        st.write(f"- **{best_bet[1]['player']}** also stands out with an AI edge of **{best_bet[1]['AI_Edge']}**, making this a strong bet.")
        
        # Show selected players in a DataFrame
        st.dataframe(pd.DataFrame(best_bet))
    else:
        st.warning("Not enough top players found for a 2-man bet.")

# 3️⃣ **Player Lookup**
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