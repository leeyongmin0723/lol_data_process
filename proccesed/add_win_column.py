import pandas as pd
import json
import os

MATCH_DIR = "/Users/user/PycharmProjects/lol_data_process/data/raw/match"
INPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"
OUTPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features_with_win.csv"


def load_match_win_map():
    """
    match_id → {100: win(0/1), 200: win(0/1)} 형태 생성
    match.json 형태가 dict 또는 list 둘 다 처리 가능
    """
    mapping = {}

    for fname in os.listdir(MATCH_DIR):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(MATCH_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # match.json 최상단이 list인지 dict인지 판별
        if isinstance(data, list):
            data = data[0]   # 리스트면 첫 요소가 match 데이터

        # metadata, info 파트 추출
        metadata = data["metadata"]
        info = data["info"]

        match_id = metadata["matchId"]

        teams = info["teams"]  # list 두 개: 100팀, 200팀
        team100_win = 1 if teams[0]["win"] else 0
        team200_win = 1 if teams[1]["win"] else 0

        mapping[match_id] = {100: team100_win, 200: team200_win}

    return mapping


def main():
    print("📂 Loading diff_features.csv ...")
    df = pd.read_csv(INPUT)

    print("📌 Building match → win map ...")
    win_map = load_match_win_map()

    print("🧩 Merging win column ...")
    df["win"] = df.apply(lambda row: win_map[row["match_id"]][row["teamId"]], axis=1)

    df.to_csv(OUTPUT, index=False)
    print(f"🎉 DONE! Saved → {OUTPUT}")


if __name__ == "__main__":
    main()