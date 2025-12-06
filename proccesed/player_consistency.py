import pandas as pd
import matplotlib.pyplot as plt
import os

# 저장 경로
save_dir = "/Users/user/PycharmProjects/lol_data_process/analysis/analysis/output_plots"
os.makedirs(save_dir, exist_ok=True)

# 한글 폰트
plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

# 데이터 입력
df = pd.read_csv("/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_win.csv")

def get_colors(series):
    return series.map({1: "blue", 0: "red"})

# -------------------------------------------------
# 🔥 대표 플레이어 1명 선정
# -------------------------------------------------
def select_representative_player(lane_df):
    counts = lane_df["puuid"].value_counts()
    rep_player = counts.index[0]   # 경기 가장 많은 puuid
    return rep_player


# -------------------------------------------------
# 🔥 그래프 생성 함수
# -------------------------------------------------
def plot_lane(lane_name, lane_df):

    # 대표 플레이어 선별
    rep_player = select_representative_player(lane_df)
    print(f"[{lane_name}] 대표 플레이어:", rep_player)

    player_df = lane_df[lane_df["puuid"] == rep_player].copy()

    # 최근 10경기 선택
    player_df = player_df.sort_values("match_id").tail(10)
    player_df["game_idx"] = range(1, len(player_df) + 1)

    colors = get_colors(player_df["win"])

    # 그림
    plt.figure(figsize=(12, 5))
    plt.scatter(player_df["game_idx"], player_df["Ct_norm"], c=colors, s=120)

    plt.axhline(0, color='gray', linestyle='--')
    plt.title(f"{lane_name} 대표 플레이어 기여도 흐름 (최근 10경기)")
    plt.xlabel("경기 번호")
    plt.ylabel("Ct_norm")

    plt.scatter([], [], color="blue", label="승리")
    plt.scatter([], [], color="red", label="패배")
    plt.legend(loc="upper right")
    plt.grid(alpha=0.3)

    # 저장 파일
    file_path = os.path.join(save_dir, f"{lane_name}_representative.png")
    plt.savefig(file_path, dpi=200)
    print(f"저장 완료 → {file_path}\n")

    plt.show()


# -------------------------------------------------
# 🔥 실행 (TOP/JUNGLE/MIDDLE/BOTTOM)
# -------------------------------------------------
plot_lane("TOP", df[df["lane"] == "TOP"])
plot_lane("JUNGLE", df[df["lane"] == "JUNGLE"])
plot_lane("MIDDLE", df[df["lane"] == "MIDDLE"])
plot_lane("BOTTOM", df[df["lane"] == "BOTTOM"])
