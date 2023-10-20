import pandas as pd
import streamlit as st

from trn10_table_football.io import load_matches, save_matches
from trn10_table_football.statistics import (player_leaderboard,
                                             team_leaderboard)
from trn10_table_football.utils import setup_logger

logger = setup_logger(__name__)


# Streamlit UI
st.title("TRN10 Table Football Match Tracker")

# Load matches
match_df = load_matches()
if match_df is None:
    # Create dummy DataFrame with specific column names & types
    match_df = pd.DataFrame(
        {
            "Date": pd.Series(["2023-10-20"], dtype="datetime64[D]"),
            "Team Blu": pd.Series(["Team 1"], dtype="str"),
            "Team Red": pd.Series(["Team 2"], dtype="str"),
            "Score": pd.Series(["8-7"], dtype="str"),
        }
    )


# Display match history
st.header("Match History")
edited_df = st.data_editor(
    match_df,
    hide_index=True,
    num_rows="dynamic",
    column_config={
        "Date": st.column_config.DateColumn("Date", width="medium"),
        "Team Blu": st.column_config.TextColumn("Team Blu", width="medium"),
        "Team Red": st.column_config.TextColumn("Team Red", width="medium"),
        "Score": st.column_config.TextColumn("Score", width="small"),
    },
)

# Display leaderboard
st.header("Team leaderboard")
team_leaderboard_df = team_leaderboard(edited_df)

if team_leaderboard_df is None:
    # Create empty DataFrame with specific column names & types
    team_leaderboard_df = pd.DataFrame(
        data={
            "Teams": pd.Series(dtype="str"),
            "Wins": pd.Series(dtype="int"),
            "Draws": pd.Series(dtype="int"),
            "Losses": pd.Series(dtype="int"),
            "Points": pd.Series(dtype="int"),
        },
    )
st.dataframe(
    team_leaderboard_df,
    hide_index=True,
    column_config={
        "Team": st.column_config.TextColumn("Team", width="medium"),
        "Wins": st.column_config.NumberColumn("Wins", width="small"),
        "Draws": st.column_config.NumberColumn("Draws", width="small"),
        "Losses": st.column_config.NumberColumn("Losses", width="small"),
        "Points": st.column_config.NumberColumn("Points", width="small"),
    },
)

st.header("Player leaderboard")
player_leaderboard_df = player_leaderboard(edited_df)

if player_leaderboard_df is None:
    # Create empty DataFrame with specific column names & types
    player_leaderboard_df = pd.DataFrame(
        data={
            "Players": pd.Series(dtype="str"),
            "Wins": pd.Series(dtype="int"),
            "Draws": pd.Series(dtype="int"),
            "Losses": pd.Series(dtype="int"),
            "Points": pd.Series(dtype="int"),
        },
    )
st.dataframe(
    player_leaderboard_df,
    hide_index=True,
    column_config={
        "Player": st.column_config.TextColumn("Team", width="medium"),
        "Wins": st.column_config.NumberColumn("Wins", width="small"),
        "Draws": st.column_config.NumberColumn("Draws", width="small"),
        "Losses": st.column_config.NumberColumn("Losses", width="small"),
        "Points": st.column_config.NumberColumn("Points", width="small"),
    },
)

if not edited_df.isna().any(axis=None):
    save_matches(edited_df)
