import os
import fastf1
import pandas as pd

CACHE_DIR = "./fastf1_cache"

def enable_cache(cache_dir: str = CACHE_DIR) -> None:
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)


def build_lap_dataset(year,event,session_type) -> pd.DataFrame:
    #year: e.g. 2024
    #event: round number, or name/substring like "Monza"
    #session_type: 'FP1','FP2','FP3','Q','SQ','R' (race), 'S' (sprint) if yk, yk
    session = fastf1.get_session(year, event, session_type)
    session.load()
    laps = session.laps.copy()

    # Structure
    base_cols = {
        "Driver": "driver",
        "DriverNumber": "driver_number",
        "Team": "team",
        "LapNumber": "lap",
        "LapTime": "lap_time",
        "Position": "position",
        "Compound": "compound",
        "TyreLife": "tyre_life",
        "Stint": "stint",
        "FreshTyre": "fresh_tyre",
        "PitInTime": "pit_in_time",
        "PitOutTime": "pit_out_time",
        "TrackStatus": "track_status",
        "Deleted": "deleted",
        "Time": "race_time",  # cumulative session time when lap was completed
    }
    available = {k: v for k, v in base_cols.items() if k in laps.columns}
    df = laps[list(available.keys())].rename(columns=available)

    # lap time in seconds (float), much easier to work with than Timedelta
    df["lap_time_sec"] = df["lap_time"].dt.total_seconds()
    df["race_time_sec"] = df["race_time"].dt.total_seconds()

    df["lap"] = df["lap"].astype("Int64")
    df["is_pit_lap"] = df["pit_in_time"].notna() | df["pit_out_time"].notna()

    # The difference in finishing^^
    df = df.sort_values(["lap", "race_time_sec"]).reset_index(drop=True)

    leader_time = df.groupby("lap")["race_time_sec"].transform("min")
    df["gap_to_leader_sec"] = df["race_time_sec"] - leader_time

    df["interval_sec"] = (
        df.groupby("lap")["race_time_sec"]
        .diff()
        .fillna(0.0)
    )

    # cleaning yk
    ordered_cols = [
        "driver", "driver_number", "team", "lap",
        "position",
        "lap_time", "lap_time_sec",
        "race_time_sec", "gap_to_leader_sec", "interval_sec",
        "compound", "tyre_life", "stint", "fresh_tyre",
        "pit_in_time", "pit_out_time", "is_pit_lap",
        "track_status", "deleted",
    ]
    ordered_cols = [c for c in ordered_cols if c in df.columns]
    df = df[ordered_cols].sort_values(["lap", "position"], na_position="last").reset_index(drop=True)
    df.to_csv(f"{event.lower()}_{year}_{session_type}_laps.csv", index=False)


    return df


# Testing yaaa
def get_lap_for_all_drivers(df: pd.DataFrame, lap_number: int) -> pd.DataFrame:
    """Example filter: one lap, all drivers, ordered by position."""
    sub = df[df["lap"] == lap_number].copy()
    return sub.sort_values("position", na_position="last").reset_index(drop=True)


if __name__ == "__main__":
    enable_cache()
    build_lap_dataset(2024, "Silverstone", "R")




    
