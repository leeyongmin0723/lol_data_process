import pandas as pd
import os

DIFF_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"
SAVE_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features_lane.csv"

def main():
    print("📂 Loading diff_features.csv ...")
    df = pd.read_csv(DIFF_PATH)

    keep_cols = [
        "match_id", "participant_id", "teamId",
        "puuid", "champion", "lane"
    ] + [c for c in df.columns if c.endswith("_diff")]

    out = df[keep_cols]

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    out.to_csv(SAVE_PATH, index=False)

    print("🎉 DONE! Saved diff_features_lane.csv")

if __name__ == "__main__":
    main()
