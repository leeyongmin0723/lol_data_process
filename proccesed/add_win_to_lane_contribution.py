import json
import pandas as pd
import os
from glob import glob

MATCH_DIR = "/Users/user/PycharmProjects/lol_data_process/data/raw/match"
INPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution.csv"
OUTPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_win.csv"

def load_match_win_map():
    win_map = {}  # key: (match_id, teamId) → win(1/0)

    match_files = glob(os.path.join(MATCH_DIR, "match_*.json"))

    for path in match_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)[0]  # json list → element 0
        match_id = data["metadata"]["matchId"]

        for team in data["info"]["teams"]:
            team_id = team["teamId"]
            win = 1 if team["win"] else 0
            win_map[(match_id, team_id)] = win

    return win_map


def main():
    print("📂 Loading lane_contribution.csv ...")
    df = pd.read_csv(INPUT)

    print("📌 Building win map from match JSON...")
    win_map = load_match_win_map()

    print("🔗 Mapping win value...")
    df["win"] = df.apply(
        lambda row: win_map.get((row["match_id"], int(row["teamId"])), None),
        axis=1
    )

    missing = df["win"].isna().sum()
    print(f"⚠ Missing win values: {missing}")

    df.to_csv(OUTPUT, index=False)
    print(f"🎉 DONE! Saved → {OUTPUT}")

if __name__ == "__main__":
    main()
