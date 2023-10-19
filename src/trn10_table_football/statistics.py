from typing import Tuple
import pandas as pd


class MatchPoints:
    WIN = 3
    DRAW = 1
    LOSS = 0


def assign_points(score: str) -> Tuple[int, int]:
    b, r = score.split("-")
    b = int(b.strip())
    r = int(r.strip())

    if b > r:
        points_blu = MatchPoints.WIN
        points_red = MatchPoints.LOSS
    elif b < r:
        points_blu = MatchPoints.LOSS
        points_red = MatchPoints.WIN
    else:
        points_blu = MatchPoints.DRAW
        points_red = MatchPoints.DRAW

    return points_blu, points_red


def leaderboard(match_df: pd.DataFrame) -> pd.DataFrame:
    if match_df is None or len(match_df) <= 0:
        return None

    # For each match, find out points
    teams = set(
        match_df["Team Blu"].unique()
    ).union(match_df["Team Red"].unique())

    team_stats = {
        team: {
            "Wins": 0,
            "Draws": 0,
            "Losses": 0,
            "Points": 0,
        }
        for team in teams
        if team is not None
    }
    for idx, row in match_df.iterrows():
        if row.isna().any():
            continue

        team_blu, team_red = row["Team Blu"], row["Team Red"]
        points_blu, points_red = assign_points(row["Score"])

        if points_blu == MatchPoints.WIN:
            team_stats[team_blu]["Wins"] += 1
            team_stats[team_red]["Losses"] += 1
        elif points_red == MatchPoints.WIN:
            team_stats[team_blu]["Losses"] += 1
            team_stats[team_red]["Wins"] += 1
        else:
            team_stats[team_blu]["Draws"] += 1
            team_stats[team_red]["Draws"] += 1

        team_stats[team_blu]["Points"] += int(points_blu)
        team_stats[team_red]["Points"] += int(points_red)

    leaderboard_df = pd.DataFrame.from_dict(team_stats, orient="index")

    if len(leaderboard_df) <= 0:
        return None

    leaderboard_df = leaderboard_df.reset_index(
    ).rename(columns={"index": "Team"})

    leaderboard_df = leaderboard_df.sort_values("Points", ascending=False)

    return leaderboard_df
