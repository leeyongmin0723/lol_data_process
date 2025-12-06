import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rc('font', family='AppleGothic')  # 맥OS 한글
plt.rcParams['axes.unicode_minus'] = False


INPUT_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution.csv"
SAVE_DIR = "player_plots"


def plot_player_contribution(puuid, df_player):
    """각 소환사별 Ct_norm 시퀀스 그래프 저장"""
    df_player = df_player.sort_values("match_id")  # 경기 순서 정렬

    x = range(1, len(df_player) + 1)
    y = df_player["Ct_norm"].values
    wins = df_player["win"].values

    colors = ["blue" if w == 1 else "red" for w in wins]

    plt.figure(figsize=(12, 5))
    plt.scatter(x, y, c=colors, s=20, alpha=0.8)
    plt.plot(x, y, color='gray', alpha=0.3)

    plt.axhline(1, color="black", linestyle="--", linewidth=1)  # 평균기준선(=1)

    plt.title(f"소환사 기여도 일관성 ({puuid})")
    plt.xlabel("경기 순서")
    plt.ylabel("기여도 (Ct_norm)")

    plt.grid(alpha=0.3)

    save_path = os.path.join(SAVE_DIR, f"{puuid}.png")
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()


def main():
    print("📂 Loading lane_contribution.csv ...")
    df = pd.read_csv(INPUT_PATH)

    os.makedirs(SAVE_DIR, exist_ok=True)

    players = df["puuid"].unique()
    print(f"🎯 Total players: {len(players)}")
    print("📊 Generating consistency plots...")

    for puuid in players:
        df_player = df[df["puuid"] == puuid]
        if len(df_player) < 20:  # 경기 수 너무 적으면 스킵
            continue
        plot_player_contribution(puuid, df_player)

    print("🎉 ALL DONE! Player graphs saved →", SAVE_DIR)


if __name__ == "__main__":
    main()
