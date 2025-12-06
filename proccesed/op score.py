import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# 한글 폰트 설정 (Mac 기준)
# ----------------------------
plt.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

# ----------------------------
# 파일 입력
# ----------------------------
MATCH_PATH = "/Users/user/PycharmProjects/lol_data_process/data/raw/match/match_5.json"
match = json.load(open(MATCH_PATH))[0]["info"]
participants = pd.DataFrame(match["participants"])

# ----------------------------
# 1) 피해량 컬럼 자동 검색
# ----------------------------
damage_cols = [
    "totalDamageDealtToChampions",
    "damageDealtToChampions",
    "physicalDamageDealtToChampions",
    "magicDamageDealtToChampions",
    "trueDamageDealtToChampions"
]

damage_col = None
for col in damage_cols:
    if col in participants.columns:
        damage_col = col
        break

if damage_col is None:
    raise ValueError("피해량 관련 컬럼을 찾을 수 없습니다.")

print("사용된 피해량 컬럼:", damage_col)

# ----------------------------
# 2) Kill Participation 계산
# ----------------------------
team_kills = participants.groupby("teamId")["kills"].sum()

participants["kill_participation"] = participants.apply(
    lambda row: (row["kills"] + row["assists"]) / max(1, team_kills[row["teamId"]]),
    axis=1
)

# ----------------------------
# 3) Min-Max Normalization
# ----------------------------
def norm(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-9)

# ----------------------------
# 4) OP Score 계산
# ----------------------------
participants["OP_score"] = (
    0.40 * norm(participants["goldEarned"]) +
    0.25 * norm(participants[damage_col]) +
    0.20 * norm(participants["kill_participation"]) +
    0.15 * norm(participants["visionScore"])
)

# 점수순 정렬
participants = participants.sort_values("OP_score", ascending=True)

# ----------------------------
# 5) 팀별 색상 적용
# ----------------------------
def team_color(team_id):
    return "#3b82f6" if team_id == 100 else "#ef4444"   # BLUE / RED

colors = participants["teamId"].apply(team_color)

# 챔피언 이름 앞에 팀 표시
participants["label"] = participants.apply(
    lambda row: ("[BLUE] " if row["teamId"] == 100 else "[RED]  ") + row["championName"],
    axis=1
)

# ----------------------------
# 6) 시각화
# ----------------------------
plt.figure(figsize=(10, 7))

bars = plt.barh(participants["label"], participants["OP_score"], color=colors)

# 바 오른쪽에 수치 표시
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.01,
             bar.get_y() + bar.get_height() / 2,
             f"{width:.3f}",
             va='center',
             fontsize=10)

plt.title("match_5 — 블루/레드팀별 10명 OP Score 비교", fontsize=15)
plt.xlabel("OP Score (정규화)", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()

print(participants[["label", "teamId", "individualPosition", "OP_score"]])
import matplotlib.pyplot as plt

# 팀 색상 지정
def team_color(team_id):
    return "#4A90E2" if team_id == 100 else "#D0021B"   # 파랑 / 빨강

participants = participants.sort_values("OP_score", ascending=True)

plt.figure(figsize=(10, 7))

bars = plt.barh(
    participants["label"],
    participants["OP_score"],
    color=[team_color(t) for t in participants["teamId"]]
)

plt.title("Match 5 (KR_7462492891) – 챔피언별 OP Score", fontsize=14)
plt.xlabel("OP Score")

for i, v in enumerate(participants["OP_score"]):
    plt.text(v + 0.02, i, f"{v:.2f}", va="center")

plt.tight_layout()
plt.savefig("/Users/user/PycharmProjects/lol_data_process/analysis/analysis/output_plots/op_score_match5.png", dpi=200)
plt.show()

print("🔵 저장 완료: op_score_match5.png")
