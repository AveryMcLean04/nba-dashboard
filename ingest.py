import sys

import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

KEEP = [
    "PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "TEAM_ABBREVIATION", "AGE",
    "GP", "MIN",
    "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
    "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "BLKA", "PF", "PFD",
    "PTS", "PLUS_MINUS", "DD2", "TD3",
]

COUNTING = [
    "MIN", "FGM", "FGA", "FG3M", "FG3A", "FTM", "FTA",
    "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "BLKA",
    "PF", "PFD", "PTS", "PLUS_MINUS",
]


def fetch_player_season(season: str) -> pd.DataFrame:
    result = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="Totals",
        timeout=60,
    )
    df = result.get_data_frames()[0]

    if df.empty:
        return pd.DataFrame()

    slim = df[KEEP].copy()
    slim = slim[slim["GP"] > 0].copy()
    slim.insert(0, "SEASON", season)

    for col in COUNTING:
        slim[f"{col}_PG"] = slim[col] / slim["GP"]

    return slim


if __name__ == "__main__":
    season = sys.argv[1] if len(sys.argv) > 1 else "2025-26"
    data = fetch_player_season(season)
    print(f"{season}: {data.shape}")
    if not data.empty:
        print(
            data.sort_values("PTS_PG", ascending=False)[
                ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "PTS_PG", "AST_PG", "BLK_PG"]
            ]
            .head(5)
            .round(1)
        )
        print(data[["PTS", "AST", "REB", "STL", "BLK", "TOV", "FG3A", "PLUS_MINUS"]].describe().loc[["min", "max", "mean"]].round(1))