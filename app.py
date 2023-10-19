import streamlit as st
import pandas as pd

from trn10_table_football.io import load_matches, save_matches
from trn10_table_football.utils import setup_logger
from trn10_table_football.statistics import leaderboard


logger = setup_logger(__name__)


# Streamlit UI
st.title("TRN10 Table Football Match Tracker")

# Load matches
match_df = load_matches()
if match_df is None:
    # Create empty DataFrame with specific column names & types
    match_df = pd.DataFrame({
        'Date': pd.Series(dtype='datetime64[D]'),
        'Team Blu': pd.Series(dtype='str'),
        'Team Red': pd.Series(dtype='str'),
        'Score': pd.Series(dtype='str')
    })


# Display match history
st.header("Match History")
match_df = st.data_editor(
    match_df, 
    num_rows="dynamic",
    column_config={
        "Date": st.column_config.DateColumn("Date", width="medium"),
        "Team Blu": st.column_config.TextColumn("Team Blu", width="medium"),
        "Team Red": st.column_config.TextColumn("Team Red", width="medium"),
        "Score": st.column_config.TextColumn("Score", width="small")
    },
)

# Display leaderboard
st.header("Leaderboard")
leaderboard_df = leaderboard(match_df)

if leaderboard_df is None:
    # Create empty DataFrame with specific column names & types
    leaderboard_df = pd.DataFrame(data={
        'Teams':pd.Series(dtype='str'),
        'Wins': pd.Series(dtype='int'),
        'Draws': pd.Series(dtype='int'),
        'Losses': pd.Series(dtype='int'),
        'Points': pd.Series(dtype='int')
    },
)
st.dataframe(
    leaderboard_df,
    hide_index=True,
    column_config={
        "Team": st.column_config.TextColumn("Team", width="medium"),
        "Wins": st.column_config.NumberColumn("Wins", width="small"),
        "Draws": st.column_config.NumberColumn("Draws", width="small"),
        "Losses": st.column_config.NumberColumn("Losses", width="small"),
        "Points": st.column_config.NumberColumn("Points", width="small"),
    }
)

if "match_df" not in st.session_state:
    st.session_state.match_df = match_df

if match_df is not None and not match_df.equals(st.session_state["match_df"]):
    # This will only run if
    # 1. Some widget has been changed (including the dataframe editor), triggering a
    # script rerun, and
    # 2. The new dataframe value is different from the old value
    if not match_df.isna().any(axis=None):
        save_matches(match_df)
        st.session_state["match_df"] = match_df
