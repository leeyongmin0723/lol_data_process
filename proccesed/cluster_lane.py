import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import os

# 저장 경로
save_dir = "/Users/user/PycharmProjects/lol_data_process/analysis/analysis/output_plots"
os.makedirs(save_dir, exist_ok=True)

plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

df = pd.read_csv("/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_win.csv")

# 바텀 통합
df["lane"] = df["lane"].replace({"UTILITY": "BOTTOM"})


def run_cluster_timeseries(lane_name, lane_df, k=3, min_games=3):

    print(f"\n===== [{lane_name}] 군집 시계열 분석 =====")

    # puuid별 최근 10경기 Ct_norm 시계열 확보
    player_series = {}

    for puuid, group in lane_df.groupby("puuid"):
        g = group.sort_values("match_id").tail(10)

        if len(g) < min_games:
            continue

        player_series[puuid] = g["Ct_norm"].values

    if len(player_series) < k:
        print(f"⚠ {lane_name}: 군집 불가 (플레이어 부족)")
        return

    # 모든 시계열의 길이 맞추기 (패딩)
    max_len = max(len(v) for v in player_series.values())

    matrix = []
    for puuid, seq in player_series.items():
        padded = np.pad(seq, (0, max_len - len(seq)), mode='edge')
        matrix.append(padded)

    matrix = np.array(matrix)

    # kmeans
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(matrix)

    # cluster별 평균 곡선
    plt.figure(figsize=(12, 6))

    for cluster in range(k):
        cluster_members = matrix[labels == cluster]
        mean_curve = cluster_members.mean(axis=0)

        plt.plot(mean_curve, marker='o', label=f"군집 {cluster}")

    plt.title(f"{lane_name} 라인 기여도 군집 분석 (k={k}, min_games={min_games})")
    plt.xlabel("경기 순서 (1~10)")
    plt.ylabel("Ct_norm")
    plt.grid(alpha=0.3)
    plt.legend()

    save_path = os.path.join(save_dir, f"{lane_name}_cluster_timeseries.png")
    plt.savefig(save_path, dpi=200)
    print(f"저장 완료 → {save_path}")

    plt.show()


# 실행
for lane in ["TOP", "JUNGLE", "MIDDLE", "BOTTOM"]:
    run_cluster_timeseries(lane, df[df["lane"] == lane])
