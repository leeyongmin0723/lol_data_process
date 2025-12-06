import pandas as pd
import numpy as np

INPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"
OUTPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution.csv"

def main():
    print(f"📂 Loading {INPUT} ...")
    df = pd.read_csv(INPUT)

    # 필요한 컬럼 확인
    required_cols = ["match_id", "participant_id", "teamId",
                     "puuid", "champion", "lane"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"❌ Missing required column: {col}")

    # diff feature columns
    diff_cols = [c for c in df.columns if c.endswith("_diff")]

    if len(diff_cols) == 0:
        raise ValueError("❌ No *_diff columns found!")

    # Ct_raw 계산
    df["Ct_raw"] = df[diff_cols].sum(axis=1)

    # 중앙값(abs)
    median_abs = df["Ct_raw"].abs().median()
    print(f"📊 median(|Ct_raw|) = {median_abs}")

    df["Ct_norm"] = df["Ct_raw"] / median_abs

    # win 컬럼이 diff_features.csv에 없으면 merge되지 않음 → add_win_column에서 처리됨
    win_col = "win"
    if win_col not in df.columns:
        print("⚠ win column missing. Expected to be added earlier (add_win_column.py).")
        df[win_col] = None

    # 최종 저장 컬럼
    keep_cols = ["match_id", "participant_id", "teamId",
                 "puuid", "champion", "lane",
                 "Ct_raw", "Ct_norm", "win"]

    out = df[keep_cols]

    out.to_csv(OUTPUT, index=False)
    print(f"🎉 DONE → {OUTPUT}")

if __name__ == "__main__":
    main()