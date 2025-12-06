import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

MATCH_PATH = "/Users/user/PycharmProjects/lol_data_process/data/raw/match/match_5.json"
TIMELINE_PATH = "/Users/user/PycharmProjects/lol_data_process/data/raw/timeline/timeline_5.json"

SAVE = "/Users/user/PycharmProjects/lol_data_process/analysis/analysis/output_plots/match_KR_7462492891_timeseries.png"

plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

# ---------------------------------------
# 1. JSON 로드
# ---------------------------------------
with open(MATCH_PATH, "r", encoding="utf-8") as f:
    match = json.load(f)
with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
    timeline = json.load(f)

# match / timeline은 리스트 → 반드시 0번 사용
match_info = match[0]["info"]
match_participants = match_info["participants"]
match_teams = match_info["teams"]

timeline_info = timeline[0]["info"]
frames = timeline_info["frames"]     # ← 이걸로 끝! 아래에 다시 덮어쓰면 안됨

# 승패 정보 추출
win_team = 100 if match_teams[0]["win"] else 200

# participantId → lane 매핑
lane_map = {}
for p in match_participants:
    lane_map[p["participantId"]] = p["individualPosition"]

# ---------------------------------------
# 2. 분 단위 골드/CS/XP 추출
# ---------------------------------------
records = []

for minute, frame in enumerate(frames):
    if minute == 0:
        continue

    pf = frame["participantFrames"]

    for pid, data in pf.items():
        pid = int(pid)
        lane = lane_map.get(pid, "NONE")

        records.append({
            "minute": minute,
            "participantId": pid,
            "team": 100 if pid <= 5 else 200,
            "lane": lane,
            "gold": data["totalGold"],
            "cs": data["minionsKilled"] + data["jungleMinionsKilled"],
            "xp": data["xp"]
        })

df = pd.DataFrame(records)

# ---------------------------------------
# 3. 라인별 블루 vs 레드 골드 격차 계산
# ---------------------------------------
results = []
lanes = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM"]

for lane in lanes:
    lane_df = df[df["lane"] == lane]

    for minute in sorted(lane_df["minute"].unique()):
        temp = lane_df[lane_df["minute"] == minute]

        blue = temp[temp["team"] == 100]
        red = temp[temp["team"] == 200]

        if len(blue) == 0 or len(red) == 0:
            continue

        blue_gold = blue["gold"].sum()
        red_gold = red["gold"].sum()

        diff = blue_gold - red_gold

        results.append({
            "minute": minute,
            "lane": lane,
            "gold_diff": diff
        })

df2 = pd.DataFrame(results)

# 정규화 (Z-score)
df2["Ct_norm"] = (df2["gold_diff"] - df2["gold_diff"].mean()) / df2["gold_diff"].std()

# ---------------------------------------
# 4. 시각화
# ---------------------------------------
plt.figure(figsize=(14, 9))

for lane in lanes:
    sub = df2[df2["lane"] == lane]
    plt.plot(sub["minute"], sub["Ct_norm"], label=lane)

plt.axhline(0, color='black', linestyle='--')

title_team = "BLUE 승리" if win_team == 100 else "RED 승리"
plt.title(f"KR_7462492891 경기 — 라인별 Ct_norm 시간 변화 ({title_team})")
plt.xlabel("분(min)")
plt.ylabel("기여도 정규값 (Ct_norm)")
plt.legend()
plt.grid(alpha=0.3)

plt.savefig(SAVE, dpi=200)
plt.show()

print("저장 완료:", SAVE)
