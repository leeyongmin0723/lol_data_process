import pandas as pd
import os

INPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features.csv"
OUTPUT = "/Users/user/PycharmProjects/lol_data_process/data/processed/diff_features_lane.csv"

BOTTOM_POS = ["BOTTOM", "UTILITY"]

def main():
    df = pd.read_csv(INPUT)

    lane_rows = []

    for match_id, match_df in df.groupby("match_id"):

        for team_id, team_df in match_df.groupby("teamId"):

            # 1) TOP
            top_row = team_df[team_df["individualPosition"] == "TOP"]
            if len(top_row) == 1:
                row = top_row.iloc[0].copy()
                row["lane"] = "TOP"
                lane_rows.append(row)

            # 2) JUNGLE
            jg_row = team_df[team_df["individualPosition"] == "JUNGLE"]
            if len(jg_row) == 1:
                row = jg_row.iloc[0].copy()
                row["lane"] = "JUNGLE"
                lane_rows.append(row)

            # 3) MIDDLE
            mid_row = team_df[team_df["individualPosition"] == "MIDDLE"]
            if len(mid_row) == 1:
                row = mid_row.iloc[0].copy()
                row["lane"] = "MIDDLE"
                lane_rows.append(row)

            # 4) BOTTOM = BOTTOM + UTILITY
            bottom_players = team_df[team_df["individualPosition"].isin(BOTTOM_POS)]

            if len(bottom_players) == 2:

                # BOTTOM과 UTILITY 두 명의 row 합산
                combined = bottom_players.iloc[0].copy()

                for col in df.columns:
                    if col.endswith("_diff") and col in bottom_players:
                        combined[col] = bottom_players[col].sum()

                combined["lane"] = "BOTTOM"
                lane_rows.append(combined)

    lane_df = pd.DataFrame(lane_rows)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    lane_df.to_csv(OUTPUT, index=False)
    print("🎉 lane-level diff saved →", OUTPUT)


if __name__ == "__main__":
    main()
