import pandas as pd
import os

# 파일 경로 설정
DIFF_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"
CT_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution.csv"
SAVE_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_id.csv"

def main():

    print("📂 Loading files...")
    df_diff = pd.read_csv(DIFF_PATH)
    df_ct = pd.read_csv(CT_PATH)

    # 필요 컬럼 있는지 체크
    required_cols = ["match_id", "teamId", "participant_id", "puuid", "champion", "lane"]
    for col in required_cols:
        if col not in df_diff.columns:
            raise ValueError(f"❌ diff_features.csv 에 {col} 컬럼이 없음!")

    print("🔗 Merging puuid + champion + lane 정보...")
    # merge key는 match_id + participant_id (정확한 매칭)
    merged = df_ct.merge(
        df_diff[["match_id", "participant_id", "puuid", "champion", "lane"]],
        on=["match_id", "participant_id"],
        how="left"
    )

    # puuid가 없으면 merge가 제대로 안된 것 → 경고 출력
    missing = merged["puuid"].isna().sum()
    if missing > 0:
        print(f"⚠ puuid 매칭 실패한 행 개수: {missing}")

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    merged.to_csv(SAVE_PATH, index=False)

    print("🎉 Saved new file →", SAVE_PATH)

if __name__ == "__main__":
    main()
