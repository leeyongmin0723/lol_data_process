import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# macOS 한글 폰트
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

INPUT_PATH = "/Users/user/PycharmProjects/lol_data_process/data/processed/lane_contribution.csv"
OUTPUT_DIR = "analysis/output_plots"

def main():
    print("📂 Loading lane_contribution.csv ...")
    df = pd.read_csv(INPUT_PATH)

    # 필요한 컬럼 확인
    required = ["lane", "Ct_norm", "win"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"❌ Missing required column: {col}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 승패 텍스트 변환
    df["result"] = df["win"].map({1: "승리", 0: "패배"})

    # ★ 라인 순서 고정
    lane_order = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM"]
    df["lane"] = pd.Categorical(df["lane"], categories=lane_order, ordered=True)

    # ---------------------------------------------------------
    # 1) Boxplot
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="lane", y="Ct_norm", hue="result", order=lane_order)
    plt.title("라인별 기여도 분포 (Boxplot)")
    plt.savefig(f"{OUTPUT_DIR}/lane_boxplot.png", dpi=300)
    plt.close()

    # ---------------------------------------------------------
    # 2) Violin Plot
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df, x="lane", y="Ct_norm", hue="result", split=True, order=lane_order)
    plt.title("라인별 기여도 분포 (Violin plot)")
    plt.savefig(f"{OUTPUT_DIR}/lane_violinplot.png", dpi=300)
    plt.close()

    print("🎉 DONE! Saved boxplot + violin plot to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
