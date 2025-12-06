import os
import json
import pandas as pd

match_dir = "/Users/user/PycharmProjects/lol_data_process/data/raw/match"

mapping = []

for file in os.listdir(match_dir):
    if not file.endswith(".json"):
        continue

    path = os.path.join(match_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔥 Case 1: 파일이 list 형태로 여러 match 포함
    if isinstance(data, list):
        matches = data
    else:
        matches = [data]

    # 🔥 모든 match 순회
    for match in matches:
        try:
            participants = match["info"]["participants"]
        except:
            continue

        for p in participants:
            mapping.append({
                "puuid": p["puuid"],
                "summonerName": p["summonerName"]
            })

# 중복 제거
mapping_df = pd.DataFrame(mapping).drop_duplicates("puuid")

mapping_df.to_csv("/Users/user/PycharmProjects/lol_data_process/data/processed/puuid_name_map.csv", index=False, encoding="utf-8-sig")
print("매핑 테이블 생성 완료 → puuid_name_map.csv")
