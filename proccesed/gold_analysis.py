import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns

INPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_win.csv"

df = pd.read_csv(INPUT)

# ================================
# 1) 전체 상관 분석
# ================================

corr_gold, p_gold = pearsonr(df["Ct_norm"], df["goldEarned"])
corr_gold10, p_gold10 = pearsonr(df["Ct_norm"], df["gold_diff_10"])

print("===== 전체 골드 관련 상관 분석 =====")
print(f"Ct_norm ↔ goldEarned  상관계수 = {corr_gold:.4f},   p={p_gold:.20f}")
print(f"Ct_norm ↔ gold_diff_10 상관계수 = {corr_gold10:.4f}, p={p_gold10:.20f}")




# ================================
# 2) 라인별 상관 분석
# ================================
print("\n===== 라인별 상관 분석 =====")
lanes = df["lane"].unique()

for lane in lanes:
    lane_df = df[df["lane"] == lane]

    corr1, _ = pearsonr(lane_df["Ct_norm"], lane_df["goldEarned"])
    corr2, _ = pearsonr(lane_df["Ct_norm"], lane_df["gold_diff_10"])

    print(f"[{lane}] Ct_norm~goldEarned = {corr1:.4f},  Ct_norm~gold_diff10 = {corr2:.4f}")


# ================================
# 3) 시각화 — 산점도 + 회귀선
# ================================
plt.figure(figsize=(10, 5))
sns.regplot(data=df, x="goldEarned", y="Ct_norm", scatter_kws={'alpha':0.3})
plt.title("전체 Ct_norm vs 골드 획득량(goldEarned)")
plt.xlabel("골드 획득량")
plt.ylabel("기여도 정규값 (Ct_norm)")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 5))
sns.regplot(data=df, x="gold_diff_10", y="Ct_norm", scatter_kws={'alpha':0.3})
plt.title("전체 Ct_norm vs 10분 골드 격차(gold_diff_10)")
plt.xlabel("10분 골드 격차")
plt.ylabel("기여도 정규값 (Ct_norm)")
plt.grid(True)
plt.show()
