import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ================================
# 🔧 한글 폰트 설정 (Mac 기준)
# ================================
plt.rc('font', family='AppleGothic')  # Mac 한글폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# ================================
# 📂 데이터 로드
# ================================
INPUT_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution.csv"
SAVE_DIR = "analysis/plots"
os.makedirs(SAVE_DIR, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

# 데이터 체크
required_cols = ["lane", "Ct_norm", "win"]
for c in required_cols:
    if c not in df.columns:
        raise ValueError(f"❌ Missing column: {c}")

lanes = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM"]

# ================================
# ① 라인별 평균 기여도 막대그래프
# ================================
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="lane", y="Ct_norm", order=lanes, palette="Set2")
plt.axhline(1, linestyle="--", color="red", label="평균 기준 (=1)")
plt.title("라인별 평균 기여도 (Ct_norm)")
plt.ylabel("평균 기여도 (Ct_norm)")
plt.xlabel("라인")
plt.legend()
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/lane_avg_contribution.png", dpi=300)
plt.close()

# ================================
# ② 승/패 구분 라인별 평균 기여도
# ================================

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df,
    x="lane",
    y="Ct_norm",
    hue="win",
    palette=["red", "blue"],
    order=lanes
)

plt.axhline(1, linestyle="--", color="black")
plt.title("승/패에 따른 라인별 평균 기여도")
plt.ylabel("기여도 (Ct_norm)")
plt.xlabel("라인")
plt.legend(labels=["패배", "승리"])
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/lane_win_loss_contribution.png", dpi=300)
plt.close()

# ================================
# ③ 라인별 기복(표준편차) 비교
# ================================
std_df = df.groupby("lane")["Ct_norm"].std().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=std_df, x="lane", y="Ct_norm", order=lanes, palette="pastel")
plt.title("라인별 기복 비교 (표준편차, Std)")
plt.ylabel("Ct_norm 표준편차 (기복)")
plt.xlabel("라인")
plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/lane_variability_std.png", dpi=300)
plt.close()

print("🎉 모든 그래프 저장 완료 →", SAVE_DIR)
