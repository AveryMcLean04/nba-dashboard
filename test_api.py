from nba_api.stats.endpoints import leaguedashplayerstats

SEASON = "2025-26"

result = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON,
    per_mode_detailed="Totals",
    timeout=60,
)
df = result.get_data_frames()[0]

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

slim = df[KEEP + ["TEAM_COUNT"]].copy()
slim.insert(0, "SEASON", SEASON)

print("All players have GP > 0:", (slim["GP"] > 0).all())

for col in COUNTING:
    slim[f"{col}_PG"] = slim[col] / slim["GP"]

print(slim.shape)
print(
    slim.sort_values("PTS_PG", ascending=False)[
        ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "PTS", "PTS_PG", "AST_PG", "BLK_PG"]
    ]
    .head(5)
    .round(1)
)

print(
    slim[slim["TEAM_COUNT"] > 1][["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "TEAM_COUNT"]]
    .head(10)
)

print("Rows:", len(slim))
print("Unique players:", slim["PLAYER_ID"].nunique())

print(
    slim.loc[
        slim["PLAYER_NAME"] == "Charles Bassey",
        ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "PTS", "PTS_PG"],
    ]
)