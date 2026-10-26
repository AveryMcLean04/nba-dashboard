from pathlib import Path

import pandas as pd

files = sorted(Path("data/raw/players").glob("*.csv"))
print("Files:", len(files))

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
print("Total rows:", len(df))
print("Seasons:", df["SEASON"].nunique(), "|", df["SEASON"].min(), "to", df["SEASON"].max())

dupes = df.duplicated(subset=["SEASON", "PLAYER_ID"]).sum()
print("Duplicate (season, player) rows:", dupes)

missing = df.isna().sum()
print("Columns with missing values:")
print(missing[missing > 0])

print(df.groupby("SEASON").size().to_string())