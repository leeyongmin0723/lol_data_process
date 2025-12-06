import os
import json
import pandas as pd

from parse_match import parse_match
from parse_timeline import parse_timeline

MATCH_DIR = "/Users/user/PycharmProjects/lol_data_process/data/raw/match"
TIMELINE_DIR = "/Users/user/PycharmProjects/lol_data_process/data/raw/timeline"
SAVE_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/final_features.csv"

df_columns_written = False


def extract_index(filename):
    return filename.split("_")[-1].replace(".json", "")


# ⭐ goldEarned + goldDiff@10min 추가 함수
def add_gold_features(df, match_json, timeline_json):

    # match.json이 리스트면 첫 요소만 사용
    if isinstance(match_json, list):
        match_json = match_json[0]
    if isinstance(timeline_json, list):
        timeline_json = timeline_json[0]

    # -----------------------------
    # 1) goldEarned: 최종 골드
    # -----------------------------
    puuid_to_gold = {}
    for p in match_json["info"]["participants"]:
        puuid_to_gold[p["puuid"]] = p.get("goldEarned", None)

    df["goldEarned"] = df["puuid"].map(puuid_to_gold)

    # -----------------------------
    # 2) goldDiff@10
    # -----------------------------
    try:
        frame10 = timeline_json["info"]["frames"][9]["participantFrames"]

        pid_to_gold10 = {
            int(pid): pdata.get("totalGold", 0)
            for pid, pdata in frame10.items()
        }

        blue = sum(pid_to_gold10.get(i, 0) for i in range(1, 6))
        red = sum(pid_to_gold10.get(i, 0) for i in range(6, 11))

        diffs = []
        for _, row in df.iterrows():
            if row["teamId"] == 100:
                diffs.append(blue - red)
            else:
                diffs.append(red - blue)

        df["gold_diff_@10min"] = diffs

    except Exception as e:
        print("⚠ goldDiff@10 계산 불가:", e)
        df["gold_diff_@10min"] = None

    return df


# ⭐ 한 경기 처리
def process_one_game(match_file, timeline_file):
    with open(match_file, "r", encoding="utf-8") as f:
        match_json = json.load(f)
    with open(timeline_file, "r", encoding="utf-8") as f:
        timeline_json = json.load(f)

    # JSON이 리스트 형태라면 첫 요소 사용
    if isinstance(match_json, list):
        match_json = match_json[0]
    if isinstance(timeline_json, list):
        timeline_json = timeline_json[0]

    df_match = parse_match(match_json)
    df_timeline = parse_timeline(timeline_json)

    df = df_match.merge(df_timeline, on="participant_id", how="left")

    # 골드 추가
    df = add_gold_features(df, match_json, timeline_json)

    return df


# 메인 함수
def main():
    global df_columns_written

    match_files = sorted(os.listdir(MATCH_DIR))

    for match_name in match_files:

        if not match_name.endswith(".json"):
            continue

        idx = extract_index(match_name)
        match_path = os.path.join(MATCH_DIR, match_name)
        timeline_path = os.path.join(TIMELINE_DIR, f"timeline_{idx}.json")

        if not os.path.exists(timeline_path):
            print(f"⚠ timeline missing → skipping match {idx}")
            continue

        print(f"📌 Processing match={match_name}")

        try:
            df = process_one_game(match_path, timeline_path)
        except Exception as e:
            print(f"❌ Error processing match={match_name}: {e}")
            continue

        if not df_columns_written:
            df.to_csv(SAVE_PATH, index=False)
            df_columns_written = True
        else:
            df.to_csv(SAVE_PATH, mode="a", header=False, index=False)

    print("\n🎉 ALL DONE — saved to:", SAVE_PATH)


if __name__ == "__main__":
    main()
