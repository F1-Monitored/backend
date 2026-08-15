"""
Fake_Ai.py=]

"""

import json
import pandas as pd

# Can change the input when integrate together in the future, but for now just hardcode the race info and file paths.
RACE_INFO_STATIC = {
    "event_name": "British Grand Prix",
    "circuit": "Silverstone Circuit",
    "season": 2024,
    "session": "Race",
}

FILES = {
    "laps": "Silverstone_2024_race_laps.csv",
    "pit_stops": "silverstone_2024_r_strategy_pit_stops.csv",
    "stints": "silverstone_2024_r_strategy_stints.csv",
    "driver_summary": "silverstone_2024_r_strategy_driver_strategy_summary.csv",
    "undercut_overcut": "silverstone_2024_r_strategy_undercut_overcut_events.csv",
    "tyre_performance": "silverstone_2024_tyre_performance.csv",
}

MASS_PIT_THRESHOLD = 4  # cars pitting on the same lap = likely rain/SC


def load_data(files=FILES):
    """Load every input CSV into a dict of DataFrames, with lowercase columns."""
    data = {}
    for key, path in files.items():
        df = pd.read_csv(path)
        df.columns = [c.strip().lower() for c in df.columns]
        data[key] = df
    return data


def get_race_info(laps):
    wet = laps[laps["compound"].isin(["INTERMEDIATE", "WET"])]
    if wet.empty:
        weather = {"conditions": "dry", "rain_window_laps": None}
    else:
        weather = {
            "conditions": "mixed (wet/dry transition)",
            "rain_window_laps": [int(wet["lap"].min()), int(wet["lap"].max())],
        }

    return {
        **RACE_INFO_STATIC,
        "total_laps": int(laps["lap"].max()),
        "drivers": sorted(laps["driver"].unique().tolist()),
        "teams": sorted(laps["team"].unique().tolist()),
        "compounds_used": sorted(laps["compound"].dropna().unique().tolist()),
        "weather": weather,
    }


def get_key_events(laps):
    clean = laps[laps["deleted"] != True]  # noqa: E712
    fastest = clean.loc[clean["lap_time_sec"].idxmin()]

    total_laps = int(laps["lap"].max())
    last_lap = laps.groupby("driver")["lap"].max()
    retirements = [
        {"driver": drv, "last_lap": int(lap)}
        for drv, lap in last_lap.items()
        if total_laps - lap >= 3
    ]

    pit_laps = laps[laps["is_pit_lap"] == True]  # noqa: E712
    pit_counts = pit_laps.groupby("lap")["driver"].count()
    mass_pit_laps = pit_counts[pit_counts >= MASS_PIT_THRESHOLD]
    mass_pit_windows = [
        {"lap": int(lap), "num_cars": int(count)} for lap, count in mass_pit_laps.items()
    ]

    leaders = laps[laps["position"] == 1].sort_values("lap")[["lap", "driver"]]
    lead_changes = []
    prev = None
    for _, row in leaders.iterrows():
        if prev is not None and row["driver"] != prev:
            lead_changes.append({"lap": int(row["lap"]), "from": prev, "to": row["driver"]})
        prev = row["driver"]

    return {
        "fastest_lap": {
            "driver": fastest["driver"],
            "lap": int(fastest["lap"]),
            "lap_time_sec": float(fastest["lap_time_sec"]),
            "compound": fastest["compound"],
        },
        "likely_retirements": retirements,
        "mass_pit_windows": mass_pit_windows,
        "lead_changes": lead_changes,
    }


def get_position_changes(laps):
    start = laps[laps["lap"] == laps["lap"].min()].set_index("driver")["position"]
    finish_rows = laps.loc[laps.groupby("driver")["lap"].idxmax()].set_index("driver")
    finish = finish_rows["position"]

    grid = []
    for driver in start.index:
        s, f = start.get(driver), finish.get(driver)
        change = int(s - f) if pd.notna(s) and pd.notna(f) else None
        grid.append(
            {
                "driver": driver,
                "start_position": int(s) if pd.notna(s) else None,
                "finish_position": int(f) if pd.notna(f) else None,
                "net_position_change": change,
            }
        )

    ranked = [r for r in grid if r["net_position_change"] is not None]
    gainers = sorted(ranked, key=lambda r: r["net_position_change"], reverse=True)[:5]
    losers = sorted(ranked, key=lambda r: r["net_position_change"])[:5]

    return {"grid": grid, "biggest_gainers": gainers, "biggest_losers": losers}


def get_tyre_analysis(tyre_perf):
    tyre_perf = tyre_perf.copy()
    tyre_perf.columns = [c.strip().lower().replace(" ", "_") for c in tyre_perf.columns]
    deg_col = next(c for c in tyre_perf.columns if "degradation" in c)

    summary = (
        tyre_perf.groupby("compound")[deg_col]
        .mean()
        .round(4)
        .rename("avg_degradation_sec_per_lap")
        .to_dict()
    )
    return {"compound_degradation_summary": summary}


def get_pit_strategy(pit_stops, stints, driver_summary):
    return {
        "total_pit_stops": int(len(pit_stops)),
        "avg_pit_stops_per_driver": round(len(pit_stops) / driver_summary["driver"].nunique(), 2),
        "strategy_label_distribution": driver_summary["strategy_label"].value_counts().to_dict(),
        "driver_strategies": driver_summary.to_dict(orient="records"),
    }


def get_undercut_overcut(uo):
    if uo.empty:
        return {}
    success = uo[uo["success"] == True] 
    return {
        "total_attempts": int(len(uo)),
        "total_successful": int(len(success)),
        "success_rate_pct": round(len(success) / len(uo) * 100, 1),
    }


def get_insights(race_info, key_events, position_changes, tyre_analysis, pit_strategy, undercut_overcut):
    insights = []

    w = race_info["weather"]
    if w["rain_window_laps"]:
        s, e = w["rain_window_laps"]
        insights.append(f"Changing weather between laps {s}-{e} forced strategy changes across the field.")

    if key_events["lead_changes"]:
        last = key_events["lead_changes"][-1]
        insights.append(
            f"The lead changed {len(key_events['lead_changes'])} time(s); "
            f"{last['to']} took the lead for good on lap {last['lap']}."
        )

    for r in key_events["likely_retirements"]:
        insights.append(f"{r['driver']} likely retired after lap {r['last_lap']}.")

    if key_events["mass_pit_windows"]:
        laps_str = ", ".join(str(w["lap"]) for w in key_events["mass_pit_windows"])
        insights.append(f"Mass pit-stop activity on lap(s) {laps_str}, consistent with a weather change or SC/VSC.")

    gainers = position_changes["biggest_gainers"]
    if gainers and gainers[0]["net_position_change"] > 0:
        g = gainers[0]
        insights.append(f"{g['driver']} was the biggest mover: P{g['start_position']} -> P{g['finish_position']}.")

    deg = tyre_analysis["compound_degradation_summary"]
    if deg:
        best = min(deg.items(), key=lambda kv: kv[1])
        insights.append(f"{best[0].title()} tyres degraded the least, at {best[1]} s/lap.")

    if undercut_overcut:
        insights.append(
            f"Undercut/overcut attempts succeeded {undercut_overcut['success_rate_pct']}% of the time "
            f"({undercut_overcut['total_successful']}/{undercut_overcut['total_attempts']})."
        )

    return insights


def generate_context(files=FILES):
    data = load_data(files)

    race_info = get_race_info(data["laps"])
    key_events = get_key_events(data["laps"])
    position_changes = get_position_changes(data["laps"])
    tyre_analysis = get_tyre_analysis(data["tyre_performance"])
    pit_strategy = get_pit_strategy(data["pit_stops"], data["stints"], data["driver_summary"])
    undercut_overcut = get_undercut_overcut(data["undercut_overcut"])
    insights = get_insights(
        race_info, key_events, position_changes, tyre_analysis, pit_strategy, undercut_overcut
    )

    return {
        "race_info": race_info,
        "key_events": key_events,
        "position_changes": position_changes,
        "tyre_analysis": tyre_analysis,
        "pit_strategy": pit_strategy,
        "undercut_overcut": undercut_overcut,
        "strategy_insights": insights,
    }


if __name__ == "__main__":
    context = generate_context()
    with open("race_context.json", "w") as f:
        json.dump(context, f, indent=2, default=str)
    print("Wrote race_context.json")
    print(json.dumps(context["strategy_insights"], indent=2))