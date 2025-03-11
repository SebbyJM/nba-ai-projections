import streamlit as st
import pandas as pd

# Set page title and layout
st.set_page_config(page_title="@Solar CTB AI", page_icon="🤖", layout="wide")

# Apply "Source Code Pro" font globally, including all tables and numbers
st.markdown(
    """
    <style>
        * { font-family: 'Source Code Pro', monospace !important; }
        h1, h2, h3, h4, h5, h6 { font-family: 'Source Code Pro', monospace !important; }
        .stDataFrame, .stTable, .stMarkdown { font-family: 'Source Code Pro', monospace !important; }
        table, th, td { font-size: 16px !important; font-family: 'Source Code Pro', monospace !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Player Search", "Hot/Cold", "🤖 AI Props"])

# --- Function to Load Data ---
@st.cache_data
def load_data():
    df = pd.concat(
        [
            pd.read_csv("AI_Projections_Points.csv"),
            pd.read_csv("AI_Projections_Rebounds.csv"),
            pd.read_csv("AI_Projections_Assists.csv"),
        ],
        ignore_index=True,
    )

    # Convert columns to numeric and round to 1 decimal place
    df["AI_Projection"] = pd.to_numeric(df["AI_Projection"], errors="coerce").round(1)
    df["best_point"] = pd.to_numeric(df["best_point"], errors="coerce").round(1)

    # Calculate Edge column (AI Projection - Line)
    df["Edge"] = (df["AI_Projection"] - df["best_point"]).round(1)

    return df

# Load the dataset
df = load_data()

# Define thresholds for Hot/Cold streaks
thresholds = {"Points": 15, "Rebounds": 4, "Assists": 4}

# --- Function to Display Data with Correct Formatting ---
def format_dataframe(data):
    return (
        data.style.format(precision=1)  # Ensure all decimals are rounded to 1 place
        .set_properties(**{"font-family": "Source Code Pro"})  # Force font in table
    )

# --- Player Search ---
if page == "Player Search":
    st.title("Player Search")
    player_name = st.text_input("Search for a player:", "")

    if player_name:
        results = df[df["player"].str.contains(player_name, case=False, na=False)]

        if not results.empty:
            st.markdown("### Player Stats")
            st.dataframe(
                format_dataframe(
                    results[["player", "category", "best_point", "AI_Projection", "Edge"]]
                    .rename(columns={"player": "Player", "category": "Prop", "best_point": "Line", "AI_Projection": "Proj"})
                )
            )
        else:
            st.warning(f"No data found for {player_name}. Try a different name.")

# --- Hot/Cold Streaks ---
elif page == "Hot/Cold":
    st.title("Hot & Cold Streaks")

    hot_players = df[
        (df["AI_Projection"] > df["best_point"]) & (df["best_point"] >= df["category"].map(thresholds))
    ].nlargest(2, "Edge")

    cold_players = df[
        (df["AI_Projection"] < df["best_point"]) & (df["best_point"] >= df["category"].map(thresholds))
    ].nsmallest(2, "Edge")

    # Display results
    st.subheader("🔥 Hot Players")
    if not hot_players.empty:
        st.dataframe(
            format_dataframe(
                hot_players[["player", "category", "best_point", "AI_Projection", "Edge"]]
                .rename(columns={"player": "Player", "category": "Prop", "best_point": "Line", "AI_Projection": "L10 Avg", "Edge": "+/- Diff"})
            )
        )
    else:
        st.warning("No hot players found.")

    st.subheader("❄️ Cold Players")
    if not cold_players.empty:
        st.dataframe(
            format_dataframe(
                cold_players[["player", "category", "best_point", "AI_Projection", "Edge"]]
                .rename(columns={"player": "Player", "category": "Prop", "best_point": "Line", "AI_Projection": "L10 Avg", "Edge": "+/- Diff"})
            )
        )
    else:
        st.warning("No cold players found.")

# --- AI Best Picks ---
elif page == "🤖 AI Props":
    st.title("🤖 AI Best Picks")

    best_picks = []
    for category, threshold in thresholds.items():
        best_pick = df[(df["category"] == category) & (df["best_point"] >= threshold)].nlargest(1, "Edge")
        if not best_pick.empty:
            best_picks.append(best_pick)

    if best_picks:
        best_picks_df = pd.concat(best_picks)
        st.dataframe(
            format_dataframe(
                best_picks_df[["player", "category", "best_point", "AI_Projection", "Edge"]]
                .rename(columns={"player": "Player", "category": "Prop", "best_point": "Line", "AI_Projection": "Proj"})
            )
        )
    else:
        st.warning("No top AI picks found.")
