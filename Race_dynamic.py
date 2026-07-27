# To use it, you guy need to convert or open the file first, make it into a df in memory then use it, some function may require previous function to work faster ^^, tell me if any bug^^ or improvements avaible^^
# I think the func names are clear enough to understand tho=]
def file_to_df(name):
    import pandas as pd
    data = pd.read_csv(name)
    return data
def compute_position_changes(laps_df):
    df = laps_df.sort_values(["driver", "lap"]).copy()

    df["prev_position"] = df.groupby("driver")["position"].shift(1)
    df["position_change"] = df["prev_position"] - df["position"]

    if "is_pit_lap" in df.columns:
        df["prev_lap_pit"] = ( df.groupby("driver")["is_pit_lap"].shift(1).fillna(False).astype(bool) )
    else:
        df["prev_lap_pit"] = False

    return df.sort_values(["lap", "position"], na_position="last").reset_index(drop=True)
# ex:print(compute_position_changes(file_to_df('silverstone_2024_R_laps.csv')))

def detect_overtake_events(changes_df,include_pit_related: bool = False,):

    events = changes_df.dropna(subset=["position_change"]).copy()
    events = events[events["position_change"] != 0]

    if not include_pit_related and "is_pit_lap" in events.columns:
        events = events[~(events["is_pit_lap"].fillna(False) | events["prev_lap_pit"].fillna(False))]

    events["event_type"] = events["position_change"].apply(
        lambda x: "overtake_gain" if x > 0 else "overtake_loss"
    )

    keep = [
        "lap", "driver", "team", "prev_position", "position",
        "position_change", "event_type",
    ]
    keep = [c for c in keep if c in events.columns]

    return (
        events[keep]
        .sort_values(["lap", "position_change"], ascending=[True, False])
        .reset_index(drop=True)
    )
#if __name__=='__main__':
    #print(detect_overtake_events(compute_position_changes(file_to_df('silverstone_2024_R_laps.csv'))))
#test

def race_start_finish_summary(laps_df) :
    df = laps_df.dropna(subset=["position"]).copy()

    first_lap_idx = df.groupby("driver")["lap"].idxmin()
    last_lap_idx = df.groupby("driver")["lap"].idxmax()

    starts = df.loc[first_lap_idx, ["driver", "position"]].rename( columns={"position": "start_position_lap1"})
    finishes = df.loc[last_lap_idx, ["driver", "position"]].rename(columns={"position": "finish_position"})

    summary = starts.merge(finishes, on="driver")
    summary["start_position"] = summary["start_position_lap1"]

    summary["net_position_change"] = (summary["start_position"] - summary["finish_position"])
    laps_completed = df.groupby("driver")["lap"].nunique()
    summary["laps_completed"] = summary["driver"].map(laps_completed)

    return summary.sort_values("net_position_change", ascending=False).reset_index(drop=True)
def attach_overtake_counts(summary_df, overtake_events):
    df = summary_df.copy()

    gains = overtake_events.loc[ overtake_events["event_type"] == "overtake_gain"].groupby("driver").size()
    losses = overtake_events.loc[ overtake_events["event_type"] == "overtake_loss"].groupby("driver").size()

    df["positions_gained_events"] = df["driver"].map(gains).fillna(0).astype(int)
    df["positions_lost_events"] = df["driver"].map(losses).fillna(0).astype(int)

    return df
#if __name__=='__main__':
    #print(attach_overtake_counts(race_start_finish_summary(file_to_df('silverstone_2024_R_laps.csv')),detect_overtake_events(compute_position_changes(file_to_df('silverstone_2024_R_laps.csv')))))

def biggest_movers(summary_df, top_n: int = 5):
    #Returns the top net gainers and top net losers (start vs finish position)
    gainers = summary_df.sort_values("net_position_change", ascending=False).head(top_n)
    losers = summary_df.sort_values("net_position_change", ascending=True).head(top_n)
    return {
        "biggest_gainers": gainers.reset_index(drop=True),
        "biggest_losers": losers.reset_index(drop=True),
    }



def build_position_matrix(laps_df):
    
    return laps_df.pivot_table(index="lap", columns="driver", values="position")


def build_race_position_report(laps_df,top_n: int = 5,include_pit_related_overtakes: bool = False,save_prefix = None) :

    changes = compute_position_changes(laps_df)
    overtakes = detect_overtake_events( changes, include_pit_related=include_pit_related_overtakes)

    summary = race_start_finish_summary(laps_df)
    summary = attach_overtake_counts(summary, overtakes)

    movers = biggest_movers(summary, top_n=top_n)
    position_matrix = build_position_matrix(laps_df)

    report = {
        "position_changes": changes,
        "overtake_events": overtakes,
        "driver_summary": summary,
        "biggest_gainers": movers["biggest_gainers"],
        "biggest_losers": movers["biggest_losers"],
        "position_matrix": position_matrix,
    }

    if save_prefix:
        overtakes.to_csv(f"{save_prefix}_overtake_events.csv", index=False)
        summary.to_csv(f"{save_prefix}_driver_position_summary.csv", index=False)
        position_matrix.to_csv(f"{save_prefix}_position_matrix.csv")

    return report
