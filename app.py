import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBA AI Projections", layout="wide")

# Robotic font and custom colors
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
}

body {
    background-color: #000000;
    color: #FFFFFF;
}

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF;
}

.stButton>button {
    background-color: #0E6EB8;
    color: white;
}

.stTextInput>div>div>input {
    background-color: #222;
    color: #FFF;
}

table {
    color: #FFFFFF;
}

.blue-name {
    color: #00BFFF !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    files = {
        "Points": "AI_Projections_Points.csv",
        "Rebounds": "AI_Projections_Rebounds.csv",
        "Assists": "AI_Projections_Assists.csv"
    }
    dfs = {k: pd.read_csv(v) for k, v in files.items()}
    return dfs

data = load_data()

st.title("🤖 Solar CTB AI")

menu = st.sidebar.selectbox("Choose Option:", ["🔍 Player Search", "🚀 AI Picks Per Category"])

if menu == "🔍 Player Search":
    st.header("🔍 Player Search")
    player_name = st.text_input("Enter Player Name:")
    if player_name:
        results = []
        for cat, df in data.items():
            player_data = df[df['player'].str.lower() == player_name.lower()]
            if not player_data.empty:
                row = player_data.iloc[0]
                results.append({
                    "PROP": cat,
                    "PROJ": f'{row["AI_Projection"]:.1f}'.rstrip('0').rstrip('.'),
                    "LINE": f'{row["best_point"]:.1f}',
                    "EDGE": f'{row["AI_Edge"]:.1f}'.rstrip('0').rstrip('.')
                })
        if results:
            result_df = pd.DataFrame(results)
            st.table(result_df.set_index("PROP"))
        else:
            st.warning(f"No data found for {player_name}. Try another name.")

elif menu == "🚀 AI Picks Per Category":
    st.header("🚀 Best AI Picks Per Category")

    thresholds = {"Points": 18, "Rebounds": 4.5, "Assists": 4.5}
    best_picks = []

    for cat, df in data.items():
        threshold = thresholds[cat]
        df_filtered = df[df["best_point"] >= threshold]
        df_filtered = df_filtered.sort_values(by="AI_Edge", ascending=False)

        if not df_filtered.empty:
            best = df_filtered.iloc[0]
            best_picks.append({
                "NAME": best["player"],
                "PROP": cat,
                "PROJ": f'{best["AI_Projection"]:.1f}'.rstrip('0').rstrip('.'),
                "LINE": f'{best["best_point"]:.1f}',
                "EDGE": f'{best["AI_Edge"]:.1f}'.rstrip('0').rstrip('.')
            })

    if best_picks:
        best_df = pd.DataFrame(best_picks)
        
        def color_name(val):
            return 'color: #00BFFF' if val in best_df['NAME'].values else 'color: white'
        
        st.table(best_df.style.applymap(color_name, subset=['NAME']))
    else:
        st.warning("⚠️ No top picks found today. Adjust thresholds or try again later.")