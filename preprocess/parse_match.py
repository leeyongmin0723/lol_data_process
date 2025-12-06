import pandas as pd

def parse_match(match_json):
    """
    match.json → 플레이어 단위 기본 정보 파싱
    """

    # ⭐ JSON이 리스트라면 첫 요소 선택
    if isinstance(match_json, list):
        match_json = match_json[0]

    info = match_json["info"]
    participants = info["participants"]

    rows = []

    for p in participants:
        row = {
            "match_id": match_json["metadata"]["matchId"],
            "participant_id": p["participantId"],
            "teamId": p["teamId"],
            "puuid": p["puuid"],
            "champion": p["championName"],
            "lane": p["teamPosition"],     # TOP / JUNGLE / MIDDLE / BOTTOM / UTILITY
            "win": int(p["win"])
        }

        rows.append(row)

    return pd.DataFrame(rows)
