import pandas as pd
import numpy as np

# ================================
# 1) 파일 경로 설정
# ================================
INPUT_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/final_features.csv"
OUTPUT_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_win.csv"

# ================================
# 2) 데이터 불러오기
# ================================
df = pd.read_csv(INPUT_PATH)

# ================================
# 3) 라인 통합 (BOTTOM + UTILITY)
# ================================
df["lane"] = df["lane"].replace({"UTILITY": "BOTTOM"})

# ================================
# 4) 피처명 통일
# ================================
df.rename(columns={
    "gold_diff_@10min": "gold_diff_10",
    "gold_10": "gold10",
    "xp_10": "xp10",
    "cs_10": "cs10"
}, inplace=True)

# ================================
# 5) 라인별 특성치 계산
# ================================
df["cs_diff_10"] = df.groupby("match_id")["cs10"].transform(lambda x: x - x.mean())
df["xp_diff_10"] = df.groupby("match_id")["xp10"].transform(lambda x: x - x.mean())

# placeholder
df["turret_damage"] = 0
df["solo_kills"] = 0
df["damage_taken_per_death"] = 0
df["jungle_cs_diff_10"] = 0
df["level_diff_10"] = 0
df["kill_participation"] = 0
df["objective_damage"] = 0

# ================================
# 6) 라인별 가중치 정의
# ================================
WEIGHTS = {
    "TOP": {
        "cs_diff_10": 0.20,
        "xp_diff_10": 0.20,
        "gold_diff_10": 0.25,
        "turret_damage": 0.15,
        "solo_kills": 0.10,
        "damage_taken_per_death": 0.10
    },
    "JUNGLE": {
        "jungle_cs_diff_10": 0.20,
        "level_diff_10": 0.20,
        "gold_diff_10": 0.25,
        "kill_participation": 0.20,
        "objective_damage": 0.15
    },
    "MIDDLE": {
        "cs_diff_10": 0.25,
        "xp_diff_10": 0.25,
        "gold_diff_10": 0.25,
        "turret_damage": 0.15,
        "solo_kills": 0.10
    },
    "BOTTOM": {
        "cs_diff_10": 0.30,
        "xp_diff_10": 0.25,
        "gold_diff_10": 0.20,
        "kill_participation": 0.15,
        "turret_damage": 0.10
    }
}

# ================================
# 7) Ct_raw 계산
# ================================
def compute_ct_raw(row):
    lane = row["lane"]
    if lane not in WEIGHTS:
        return 0

    s = 0
    for f, w in WEIGHTS[lane].items():
        s += row.get(f, 0) * w
    return s

df["Ct_raw"] = df.apply(compute_ct_raw, axis=1)

# ================================
# 8) Ct_norm 계산
# ================================
df["Ct_norm"] = df.groupby("match_id")["Ct_raw"].transform(
    lambda x: (x - x.mean()) / (x.std() + 1e-9)
)

# ================================
# 9) 최종 저장
# ================================
df.to_csv(OUTPUT_PATH, index=False)
print(f"🎉 Saved updated file: {OUTPUT_PATH}")
