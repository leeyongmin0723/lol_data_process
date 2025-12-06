import pandas as pd
import os

INPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/final_features.csv"
OUTPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"

# diff 계산 대상 feature 목록 (final_features.csv 에 있는 실제 컬럼만 사용)
DIFF_COLS = [
    "gold_10",
    "cs_10",
    "lane_cs_10",
    "jungle_cs_10",
    "xp_10",
    "solo_kills_15",
    "team_damage_pct",
    "damage_to_turrets",
    "vision_score_per_min",
    "total_damage_taken",
    "kill_participation",
    "kills"  # ADC/SUP 합산용
]


def main():
    df = pd.read_csv(INPUT)

    output_rows = []

    for match_id, match_df in df.groupby("match_id"):

        team100 = match_df[match_df["teamId"] == 100]
        team200 = match_df[match_df["teamId"] == 200]

        for pos in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]:

            p100 = team100[team100["individualPosition"] == pos]
            p200 = team200[team200["individualPosition"] == pos]

            if len(p100) == 1 and len(p200) == 1:

                r100 = p100.iloc[0].copy()
                r200 = p200.iloc[0].copy()

                for col in DIFF_COLS:
                    r100[f"{col}_diff"] = r100[col] - r200[col]
                    r200[f"{col}_diff"] = r200[col] - r100[col]

                output_rows.append(r100)
                output_rows.append(r200)

    out = pd.DataFrame(output_rows)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    out.to_csv(OUTPUT, index=False)

    print("🎉 diff_features.csv 생성 완료!")


if __name__ == "__main__":
    main()
