import pandas as pd

def parse_timeline(timeline_json):
    """
    timeline.json → 10분 골드, cs, xp 등 프레임 기반 데이터 파싱
    """

    # ⭐ 리스트면 첫 요소 사용
    if isinstance(timeline_json, list):
        timeline_json = timeline_json[0]

    info = timeline_json["info"]
    frames = info["frames"]

    # 10분 프레임 (0부터 시작 → 9번째가 10분)
    if len(frames) <= 9:
        raise ValueError("timeline frames insufficient (no 10-minute frame).")

    frame10 = frames[9]["participantFrames"]

    rows = []

    for pid_str, pdata in frame10.items():
        pid = int(pid_str)

        row = {
            "participant_id": pid,
            "gold_10": pdata.get("totalGold", 0),
            "xp_10": pdata.get("xp", 0),
            "cs_10": pdata.get("minionsKilled", 0) + pdata.get("jungleMinionsKilled", 0)
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    return df
