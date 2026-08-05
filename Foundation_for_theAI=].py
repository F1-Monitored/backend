"""
strategy_engine.py

Version 0.1.0
This module provides a set of functions to analyze and summarize race strategy data from previous dataframes.

Inputs
------
-laps_df 
-tyre_performance_df 

Typical usage
-------------
    Testing yaaa
    import pandas as pd
    from strategy_engine import build_strategy_report

    laps = pd.read_csv("silverstone_2024_R_laps.csv")
    report = build_strategy_report(laps, save_prefix="silverstone_2024_r")

"""
import json
import numpy as np
import pandas as pd


def file_to_df(name):
    data = pd.read_csv(name)
    return data

# 1. Pit stops

def extract_pit_stops(laps_df):
    """
    Taking data from pit stops and give out some basic info
    """
    df = laps_df.sort_values(["driver", "lap"]).copy()

    for col in ["stint", "lap", "position", "compound", "tyre_life"]:
        if col in df.columns:
            df[f"prev_{col}"] = df.groupby("driver")[col].shift(1)

    changed = df["stint"] != df["prev_stint"]
    out_laps = df[changed & df["prev_stint"].notna()].copy()
    out_laps["pit_stop_number"] = out_laps.groupby("driver").cumcount() + 1

    pit_stops = out_laps.rename(columns={
        "lap": "out_lap",
        "prev_lap": "in_lap",
        "position": "position_after",
        "prev_position": "position_before",
        "compound": "compound_after",
        "prev_compound": "compound_before",
        "stint": "stint_after",
        "prev_stint": "stint_before",
        "tyre_life": "tyre_life_after",
        "prev_tyre_life": "tyre_life_before",
    })

    pit_stops["net_position_change"] = (
        pit_stops["position_before"] - pit_stops["position_after"]
    )

    keep = [
        "driver", "team", "pit_stop_number", "in_lap", "out_lap",
        "stint_before", "stint_after",
        "compound_before", "compound_after",
        "tyre_life_before", "tyre_life_after",
        "position_before", "position_after", "net_position_change",
    ]
    keep = [c for c in keep if c in pit_stops.columns]

    return (
        pit_stops[keep]
        .sort_values(["driver", "pit_stop_number"])
        .reset_index(drop=True)
    )

# Feel free to clone and try better version to yourself bro^^

# 2. Stints


def build_stint_table(laps_df) :
    """Just a table from previous dataframes with some basic info about stints"""
    df = laps_df.dropna(subset=["stint"]).copy()

    agg = {
        "compound": ("compound", "first"),
        "start_lap": ("lap", "min"),
        "end_lap": ("lap", "max"),
        "lap_count": ("lap", "nunique"),
    }
    if "tyre_life" in df.columns:
        agg["tyre_life_start"] = ("tyre_life", "min")
        agg["tyre_life_end"] = ("tyre_life", "max")
    if "team" in df.columns:
        agg["team"] = ("team", "first")

    stints = (
        df.groupby(["driver", "stint"])
        .agg(**agg)
        .reset_index()
        .sort_values(["driver", "stint"])
        .reset_index(drop=True)
    )
    return stints


def compute_stint_pace(laps_df,exclude_pit_laps= True, min_laps_for_trend=3):
    """
    Basic tyre-performance fallback computed directly from lap times.

    For each driver-stint: average clean lap time, and a rough
    degradation trend (seconds/lap slope across the stint, via a simple
    linear fit). Excludes pit in/out laps by default since those lap
    times are compromised and would distort the trend.

    If you have a proper external tyre_performance_df (e.g. from
    telemetry or a dedicated model), pass it into build_strategy_report()
    instead — this is just a reasonable default when you don't.(This is AI explanation, you guy can take a view, it's really helpful)
    """
    df = laps_df.copy()
    if exclude_pit_laps and "is_pit_lap" in df.columns:
        df = df[~df["is_pit_lap"].fillna(False)]
    df = df.dropna(subset=["lap_time_sec", "stint"])

    records = []
    for (driver, stint), g in df.groupby(["driver", "stint"]):
        g = g.sort_values("lap")
        avg_lap_time = g["lap_time_sec"].mean()
        if len(g) >= min_laps_for_trend:
            x = np.arange(len(g))
            slope = float(np.polyfit(x, g["lap_time_sec"], 1)[0])
        else:
            slope = np.nan
        records.append({
            "driver": driver,
            "stint": stint,
            "clean_laps_used": len(g),
            "avg_lap_time_sec": avg_lap_time,
            "degradation_sec_per_lap": slope,
        })

    return pd.DataFrame(records)


# 3. Pit stop timeline (pit stops + stint pace context)


def pit_stop_timeline(pit_stops_df, stints_df):
    """Pit stops enriched with the pace/degradation of the stint that just ended."""
    pace_cols = [c for c in ["avg_lap_time_sec", "degradation_sec_per_lap"] if c in stints_df.columns]
    if not pace_cols:
        return pit_stops_df.copy()

    prior_stint_pace = stints_df[["driver", "stint"] + pace_cols].rename(
        columns={
            "stint": "stint_before",
            **{c: f"prev_stint_{c}" for c in pace_cols},
        }
    )
    return pit_stops_df.merge(prior_stint_pace, on=["driver", "stint_before"], how="left")


# 4. Per-driver strategy summary


def _strategy_label(num_stops: int) -> str:
    labels = {0: "no_stop", 1: "one_stop", 2: "two_stop"}
    return labels.get(num_stops, f"{num_stops}_stop")


def driver_strategy_summary(laps_df,pit_stops_df,stints_df):
    """
   Summarizing a driver's race strategy in a single row.
    """
    rows = []
    valid_laps = laps_df.dropna(subset=["position"])

    for driver, d_laps in valid_laps.groupby("driver"):
        d_pits = pit_stops_df[pit_stops_df["driver"] == driver]
        d_stints = stints_df[stints_df["driver"] == driver].sort_values("stint")

        start_position = d_laps.loc[d_laps["lap"].idxmin(), "position"]
        finish_position = d_laps.loc[d_laps["lap"].idxmax(), "position"]

        rows.append({
            "driver": driver,
            "team": d_laps["team"].iloc[0] if "team" in d_laps.columns else None,
            "num_pit_stops": len(d_pits),
            "strategy_label": _strategy_label(len(d_pits)),
            "compound_sequence": "-".join(d_stints["compound"].astype(str)),
            "stint_lap_counts": "-".join(d_stints["lap_count"].astype(str)),
            "start_position": start_position,
            "finish_position": finish_position,
            "net_race_position_change": start_position - finish_position,
            "net_position_change_from_stops": (
                d_pits["net_position_change"].sum() if len(d_pits) else 0
            ),
        })

    return (
        pd.DataFrame(rows)
        .sort_values("finish_position", na_position="last")
        .reset_index(drop=True)
    )

# 5. Basic undercut / overcut detector


def detect_undercut_overcut(pit_stops_df,laps_df,position_window= 2,lookahead_laps= 5,):
    """
    Just a basic attempt to detect undercut/overcut events from pit stop and lap data. It looks for rival drivers who were within
     a certain position window before the pit stop,
     and checks if the pitting driver gained or lost position relative to them after both have completed their pit stops.(LOL, this automatic ai explanation is so fcking good)
    """
    if pit_stops_df.empty:
        return pd.DataFrame()

    laps_by_driver = {
        d: g.sort_values("lap").set_index("lap")
        for d, g in laps_df.groupby("driver")
    }

    events = []
    for _, stop in pit_stops_df.iterrows():
        driver = stop["driver"]
        in_lap, out_lap = stop["in_lap"], stop["out_lap"]
        pos_before = stop["position_before"]

        if pd.isna(in_lap) or pd.isna(pos_before):
            continue

        in_lap_field = laps_df[laps_df["lap"] == in_lap]
        rivals = in_lap_field[
            (in_lap_field["driver"] != driver)
            & in_lap_field["position"].between(
                pos_before - position_window, pos_before + position_window
            )
        ]

        for _, rival_row in rivals.iterrows():
            rival = rival_row["driver"]
            rival_pos_before = rival_row["position"]

            rival_stops = pit_stops_df[
                (pit_stops_df["driver"] == rival)
                & (pit_stops_df["in_lap"] >= in_lap)
                & (pit_stops_df["in_lap"] <= in_lap + lookahead_laps)
            ]
            if rival_stops.empty:
                continue  # rival didn't pit nearby -> not a clean read

            rival_out_lap = rival_stops.iloc[0]["out_lap"]
            check_lap = max(out_lap, rival_out_lap)

            driver_pos_after = laps_by_driver.get(driver, pd.DataFrame()).reindex([check_lap])
            rival_pos_after = laps_by_driver.get(rival, pd.DataFrame()).reindex([check_lap])
            if driver_pos_after.empty or rival_pos_after.empty:
                continue
            driver_after = driver_pos_after["position"].iloc[0]
            rival_after = rival_pos_after["position"].iloc[0]
            if pd.isna(driver_after) or pd.isna(rival_after):
                continue

            event_type = "undercut_attempt" if out_lap <= rival_out_lap else "overcut_attempt"
            was_ahead_before = pos_before < rival_pos_before
            is_ahead_after = driver_after < rival_after
            success = (not was_ahead_before) and is_ahead_after

            events.append({
                "driver": driver, "rival": rival,
                "event_type": event_type,
                "in_lap": in_lap, "out_lap": out_lap, "rival_out_lap": rival_out_lap,
                "position_before": pos_before, "rival_position_before": rival_pos_before,
                "check_lap": check_lap,
                "position_after": driver_after, "rival_position_after": rival_after,
                "success": bool(success),
            })

    return pd.DataFrame(events).drop_duplicates().reset_index(drop=True)


# 6. Export to JSON

def export_strategy_json(report, path: str):
    payload = {name: df.to_dict(orient="records") for name, df in report.items()}
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, default=str)



# 7. Arranging everything together in a single function for convenience


def build_strategy_report(laps_df,tyre_performance_df = None,position_window= 2,lookahead_laps = 5,save_prefix: str = None):
    """
   Give me a laps_df and I will give you a full strategy report with pit stops, stints, stint pace, pit stop timeline, driver strategy summary, and undercut/overcut events.
   What a good sentence to illustrate this=]
    """
    pit_stops = extract_pit_stops(laps_df)
    stints = build_stint_table(laps_df)
    pace = compute_stint_pace(laps_df)
    stints = stints.merge(pace, on=["driver", "stint"], how="left")

    if tyre_performance_df is not None:
        stints = stints.merge(
            tyre_performance_df, on=["driver", "stint"], how="left", suffixes=("", "_ext")
        )

    timeline = pit_stop_timeline(pit_stops, stints)
    summary = driver_strategy_summary(laps_df, pit_stops, stints)
    undercuts = detect_undercut_overcut(
        pit_stops, laps_df, position_window=position_window, lookahead_laps=lookahead_laps
    )

    report = {
        "pit_stops": pit_stops,
        "stints": stints,
        "pit_stop_timeline": timeline,
        "driver_strategy_summary": summary,
        "undercut_overcut_events": undercuts,
    }

    if save_prefix:
        for name, df in report.items():
            df.to_csv(f"{save_prefix}_{name}.csv", index=False)
        export_strategy_json(report, f"{save_prefix}_strategy_report.json")

    return report

#Testing yaaaaaaaaaaa

if __name__ == "__main__":
    laps = file_to_df("silverstone_2024_R_laps.csv")

    report = build_strategy_report(laps, save_prefix="silverstone_2024_r_strategy")

#    print(report["driver_strategy_summary"])
#    print()
#    print(report["pit_stops"])
#    print()
#    print(report["undercut_overcut_events"])