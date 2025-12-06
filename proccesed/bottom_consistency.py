import pandas as pd
import matplotlib.pyplot as plt
import os

# 저장 경로 설정
save_dir = "/Users/user/PycharmProjects/lol_data_process/analysis/analysis/output_plots"
os.makedirs(save_dir, exist_ok=True)

# 한글 폰트
plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

df = pd.read_csv("/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution_with_win.csv")

def get_colors(series):
    return series.map({1: "blue", 0: "red"})


# ===============================
# 🔹 TOP / JUNGLE / MIDDLE 공통 함수
# ===============================
def plot_and_save(lane_name, lane_df):
    lane_df = lane_df.sort_values("match_id").tail(10).copy()
    lane_df["game_idx"] = range(1, len(lane_df) + 1)

    colors = get_colors(lane_df["win"])

    plt.figure(figsize=(12, 5))
    plt.scatter(lane_df["game_idx"], lane_df["Ct_norm"], c=colors, s=120)

    plt.axhline(0, color='gray', linestyle='--')
    plt.title(f"{lane_name} 라인 기여도 흐름 (최근 10경기)")
    plt.xlabel("경기 번호")
    plt.ylabel("Ct_norm")

    # 승/패 라벨
    plt.scatter([], [], color="blue", label="승리")
    plt.scatter([], [], color="red", label="패배")
    plt.legend(loc="upper right")
    plt.grid(alpha=0.3)

    file_path = os.path.join(save_dir, f"{lane_name}.png")
    plt.savefig(file_path, dpi=200)
    print(f"저장 완료: {file_path}")

    plt.show()


# ===============================
# 🔹 BOTTOM (ADC + SUPPORT 통합)
# ===============================
def select_bottom_players(df):
    # BOTTOM + SUPPORT(UTILITY) 통합
    bottom_df = df[df["lane"].isin(["BOTTOM", "UTILITY"])]

    counts = bottom_df["puuid"].value_counts()

    selected = []
    total = 0

    for puuid, cnt in counts.items():
        selected.append(puuid)
        total += cnt
        if total >= 10:   # 10경기 확보 시 종료
            break

    return selected


def plot_and_save_bottom(df):
    # BOTTOM + UTILITY 통합
    bottom_df = df[df["lane"].isin(["BOTTOM", "UTILITY"])].copy()

    selected_players = select_bottom_players(df)
    print("선택된 바텀 선수들:", selected_players)

    # 선택된 선수들의 경기 중 10경기만 추출
    plot_df = bottom_df[bottom_df["puuid"].isin(selected_players)].copy()
    plot_df = plot_df.sort_values("match_id").head(10)
    plot_df["game_idx"] = range(1, len(plot_df) + 1)

    colors = get_colors(plot_df["win"])

    plt.figure(figsize=(12, 5))
    plt.scatter(plot_df["game_idx"], plot_df["Ct_norm"], c=colors, s=120)

    plt.axhline(0, color="gray", linestyle="--")
    plt.title("BOTTOM(ADC+SUPPORT) 라인 기여도 흐름 (10경기)")
    plt.xlabel("경기 번호")
    plt.ylabel("Ct_norm")

    plt.scatter([], [], color="blue", label="승리")
    plt.scatter([], [], color="red", label="패배")
    plt.legend(loc="upper right")
    plt.grid(alpha=0.3)

    file_path = os.path.join(save_dir, "BOTTOM.png")
    plt.savefig(file_path, dpi=200)
    print(f"저장 완료: {file_path}")

    plt.show()


# ===============================
# 🔥 실행 — 4개 그래프 파일 저장
# ===============================
plot_and_save("TOP", df[df["lane"] == "TOP"])
plot_and_save("JUNGLE", df[df["lane"] == "JUNGLE"])
plot_and_save("MIDDLE", df[df["lane"] == "MIDDLE"])
plot_and_save_bottom(df)
