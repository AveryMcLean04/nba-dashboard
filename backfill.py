import time
from pathlib import Path

from ingest import fetch_player_season

FIRST_SEASON_START = 1996
CURRENT_SEASON = "2026-27"
DATA_DIR = Path("data/raw/players")
PAUSE_SECONDS = 2
MAX_TRIES = 3


def season_label(start_year: int) -> str:
    return f"{start_year}-{str(start_year + 1)[-2:]}"


def all_seasons() -> list[str]:
    last_start = int(CURRENT_SEASON[:4])
    return [season_label(y) for y in range(FIRST_SEASON_START, last_start + 1)]


def fetch_with_retry(season: str):
    for attempt in range(1, MAX_TRIES + 1):
        try:
            return fetch_player_season(season)
        except Exception as e:
            print(f"  attempt {attempt} failed: {e}")
            time.sleep(5 * attempt)
    return None


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for season in all_seasons():
        path = DATA_DIR / f"{season}.csv"

        if path.exists() and season != CURRENT_SEASON:
            print(f"{season}: already saved, skipping")
            continue

        df = fetch_with_retry(season)

        if df is None:
            print(f"{season}: FAILED after {MAX_TRIES} tries")
            continue
        if df.empty:
            print(f"{season}: no data")
            continue

        df.to_csv(path, index=False)
        print(f"{season}: saved {len(df)} rows")
        time.sleep(PAUSE_SECONDS)


if __name__ == "__main__":
    main()