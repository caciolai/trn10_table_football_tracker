from __future__ import annotations

from datetime import datetime
from typing import List

import pandas as pd
from pydantic import BaseModel, NonNegativeInt

from trn10_table_football.constants import SCORE_SEP_CHAR, TEAM_SEP_CHAR


class Player(BaseModel):
    name: str = None


class Team(BaseModel):
    players: List[Player]


class Score(BaseModel):
    score_blu: NonNegativeInt
    score_red: NonNegativeInt


class Match(BaseModel):
    date: datetime
    team_blu: Team
    team_red: Team
    score: Score


class Matches:
    def __init__(self, matches: List[Match]) -> None:
        self.matches = matches

    @staticmethod
    def from_pandas(df: pd.DataFrame) -> Matches:
        matches = []

        for idx, row in df.iterrows():
            team_blu = Team(
                players=[
                    Player(name=p.strip()) for p in row["Team Blu"].split(TEAM_SEP_CHAR)
                ]
            )

            team_red = Team(
                players=[
                    Player(name=p.strip()) for p in row["Team Red"].split(TEAM_SEP_CHAR)
                ]
            )

            score = Score(
                score_blu=row["Score"].split(SCORE_SEP_CHAR)[0],
                score_red=row["Score"].split(SCORE_SEP_CHAR)[1],
            )

            match = Match(
                date=row["Date"], team_blu=team_blu, team_red=team_red, score=score
            )

            matches.append(match)

        return Matches(matches)

    def to_pandas(self) -> pd.DataFrame:
        data = []

        for match in self.matches:
            team_blu = TEAM_SEP_CHAR.join(
                str(player) for player in match.team_blu.players
            )
            team_red = TEAM_SEP_CHAR.join(
                str(player) for player in match.team_red.players
            )
            score = (
                str(match.score.score_blu) + SCORE_SEP_CHAR + str(match.score.score_red)
            )

            data.append(
                {
                    "Date": match.date,
                    "Team Blu": team_blu,
                    "Team Red": team_red,
                    "Score": score,
                }
            )

        return pd.DataFrame(data)
