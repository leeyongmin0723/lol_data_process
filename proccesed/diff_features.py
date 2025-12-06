import pandas as pd
import os

RAW_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/final_features.csv"
SAVE_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"

def main():
    print("📂 Loading final_features.csv ...")
    df = pd.read_csv(RAW_PATH)

    # 반드시 포함되어야 하는 컬럼 확인
    required = ["match_id", "participant_id", "teamId", "puuid", "champion", "lane"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"❌ final_features.csv 에 {col} 없음!")

    # diff 를 계산할 지표들
    diff_cols = [
        "gold_10", "cs_10", "lane_cs_10", "jungle_cs_10", "xp_10", "solo_kills_15",
        "team_damage_pct", "damage_to_turrets", "vision_score_per_min",
        "total_damage_taken", "kill_participation", "kills"
    ]

    out_rows = []

    print("🧮 Computing lane diff values...")
    for match_id, g in df.groupby("match_id"):

        # 라인별로 정렬
        for lane, gg in g.groupby("lane"):

            if len(gg) != 2:
                continue

            t1 = gg.iloc[0]
            t2 = gg.iloc[1]

            diff_dict = {
                "match_id": match_id,
                "participant_id": t1["participant_id"],
                "teamId": t1["teamId"],
                "puuid": t1["puuid"],
                "champion": t1["champion"],
                "lane": lane
            }

            diff_dict_opp = {
                "match_id": match_id,
                "participant_id": t2["participant_id"],
                "teamId": t2["teamId"],
                "puuid": t2["puuid"],
                "champion": t2["champion"],
                "lane": lane
            }

            # diff 실제 계산
            for col in diff_cols:
                d = t1[col] - t2[col]
                diff_dict[f"{col}_diff"] = d
                diff_dict_opp[f"{col}_diff"] = -d

            out_rows.append(diff_dict)
            out_rows.append(diff_dict_opp)

    out = pd.DataFrame(out_rows)

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    out.to_csv(SAVE_PATH, index=False)

    print("🎉 DONE! Saved diff_features.csv")

if __name__ == "__main__":
    main()
