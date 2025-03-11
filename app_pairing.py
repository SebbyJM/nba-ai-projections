import streamlit as st
import pandas as pd

# ✅ Set up Streamlit page
st.set_page_config(page_title="NBA AI Projections", layout="wide")
st.title("NBA AI Projections")

# ✅ Sidebar Navigation (Ensures `page` is defined)
page = st.sidebar.radio("Select a Page", ["🏀 AI Projections", "🎯 AI's Best 2-Man Bet"])

# ✅ Load AI projection data (Handle missing files)
try:
    points_df = pd.read_csv("AI_Projections_Points.csv")
    rebounds_df = pd.read_csv("AI_Projections_Rebounds.csv")
    assists_df = pd.read_csv("AI_Projections_Assists.csv")
except FileNotFoundError as e:
    st.error(f"🚨 Missing file: {e}")
    st.stop()

# ✅ AI's Best 2-Man Bet Page
if page == "🎯 AI's Best 2-Man Bet":
    st.subheader("🎯 AI’s Top 2-Man Bet Recommendation")

    # ✅ Merge data from all categories
    all_data = pd.concat([
        points_df.assign(Category="Points"),
        rebounds_df.assign(Category="Rebounds"),
        assists_df.assign(Category="Assists")
    ], ignore_index=True)

    # ✅ Debugging: Show loaded data
    st.write("✅ Data Loaded for AI Best Bet Selection")
    st.dataframe(all_data.head(10))

    # ✅ Select top picks based on AI Edge
    top_picks = all_data.sort_values(by="AI_Edge", ascending=False).head(10)

    # ✅ Debugging: Show unique categories
    st.write("🛠️ Unique Categories in Top Picks:", list(top_picks["Category"].unique()))

    # ✅ Show top picks before filtering
    st.write("🔝 Top AI Picks Before Filtering")
    st.dataframe(top_picks)

    # ✅ Select 2 players from different categories
    best_bet = []
    seen_categories = set()

    for _, row in top_picks.iterrows():
        category = row["Category"]
        if category not in seen_categories:
            best_bet.append(row)
            seen_categories.add(category)

        if len(best_bet) == 2:  # Stop once we have two players
            break

    # ✅ Display the best bet selection
    if len(best_bet) == 2:
        st.write(f"🔥 **Best Bet:** {best_bet[0]['player']} ({best_bet[0]['Category']}) & {best_bet[1]['player']} ({best_bet[1]['Category']})")

        st.write(f"**Why?**")
        st.write(f"- **{best_bet[0]['player']}** has an AI edge of **{best_bet[0]['AI_Edge']}**, meaning their projection is well above the betting line.")
        st.write(f"- **{best_bet[1]['player']}** also stands out with an AI edge of **{best_bet[1]['AI_Edge']}**, making this a strong bet.")

        # ✅ Show selected players in a DataFrame
        st.dataframe(pd.DataFrame(best_bet))
    else:
        st.warning("⚠️ Not enough top players found for a 2-man bet. Consider lowering the AI edge threshold.")

# ✅ Default Page: AI Projections
elif page == "🏀 AI Projections":
    st.subheader("📊 AI Projections")
    st.write("Select a category from the sidebar to view AI projections.")