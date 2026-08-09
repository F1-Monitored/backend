import pandas as pd
import numpy as np
import io
from pathlib import Path
from typing import Union, Dict, Any


class TyrePerformanceAnalyzer:
    """
    Core tyre analysis engine that works with DataFrames, CSV/JSON file paths,
    or raw in-memory byte streams (for API uploads).
    """

    def __init__(self, lap_df: pd.DataFrame, fuel_correction_per_lap: float = 0.035):
        self.df = lap_df.copy()
        self.fuel_correction = fuel_correction_per_lap
        self._normalize_columns()

    def _normalize_columns(self):
        """Maps snake_case or FastF1 columns to a standardized schema."""
        column_mapping = {
            "driver": "Driver",
            "team": "Team",
            "stint": "Stint",
            "compound": "Compound",
            "lap": "LapNumber",
            "lap_time_sec": "LapTimeSeconds",
            "pit_in_time": "PitInTime",
            "pit_out_time": "PitOutTime",
            "is_pit_lap": "IsPitLap",
            "track_status": "TrackStatus",
            "deleted": "Deleted"
        }
        self.df = self.df.rename(columns=column_mapping)

    def _get_clean_stint_laps(self, stint_df: pd.DataFrame) -> pd.DataFrame:
        """Filters out pit laps, track limit violations, and pace outliers."""
        clean = stint_df.dropna(subset=["LapTimeSeconds"]).copy()

        if "IsPitLap" in clean.columns:
            clean = clean[clean["IsPitLap"] == False]
        if "PitInTime" in clean.columns:
            clean = clean[clean["PitInTime"].isna()]
        if "PitOutTime" in clean.columns:
            clean = clean[clean["PitOutTime"].isna()]
        if "Deleted" in clean.columns:
            clean = clean[clean["Deleted"] == False]
        if "IsAccurate" in clean.columns:
            clean = clean[clean["IsAccurate"] == True]
        if "TrackStatus" in clean.columns:
            clean = clean[clean["TrackStatus"].astype(str) == "1"]

        if len(clean) >= 3:
            stint_median = clean["LapTimeSeconds"].median()
            clean = clean[clean["LapTimeSeconds"] <= stint_median * 1.07]

        return clean

    def process_stints(self) -> pd.DataFrame:
        """Runs stint-by-stint metric calculations."""
        results = []
        required_cols = ["Driver", "Stint", "LapNumber", "LapTimeSeconds"]
        missing = [col for col in required_cols if col not in self.df.columns]

        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")

        valid_df = self.df.dropna(subset=["Driver", "Stint"])
        grouped = valid_df.groupby(["Driver", "Stint"])

        for (driver, stint_num), stint_data in grouped:
            if stint_data.empty:
                continue

            team = stint_data["Team"].iloc[0] if "Team" in stint_data.columns else "Unknown"
            compound = stint_data["Compound"].iloc[0] if "Compound" in stint_data.columns else "Unknown"

            start_lap = int(stint_data["LapNumber"].min())
            end_lap = int(stint_data["LapNumber"].max())
            stint_length = end_lap - start_lap + 1

            clean_laps = self._get_clean_stint_laps(stint_data)

            if len(clean_laps) < 3:
                continue

            lap_times = clean_laps["LapTimeSeconds"].values
            lap_nums = clean_laps["LapNumber"].values

            avg_lap_time = float(np.mean(lap_times))
            fastest_lap = float(np.min(lap_times))
            slowest_lap = float(np.max(lap_times))

            sample_size = min(3, len(lap_times))
            first_n_avg = np.mean(lap_times[:sample_size])
            last_n_avg = np.mean(lap_times[-sample_size:])
            pace_drop_off = float(last_n_avg - first_n_avg)

            slope, _ = np.polyfit(lap_nums, lap_times, 1)
            raw_degradation = float(slope)
            fuel_adj_degradation = raw_degradation + self.fuel_correction
            pace_std_dev = float(np.std(lap_times))

            results.append({
                "Driver": driver,
                "Team": team,
                "Stint": int(stint_num),
                "Compound": compound,
                "Start Lap": start_lap,
                "End Lap": end_lap,
                "Stint Length": stint_length,
                "Clean Laps Evaluated": len(clean_laps),
                "Avg Lap Time": round(avg_lap_time, 3),
                "Fastest Lap": round(fastest_lap, 3),
                "Slowest Lap": round(slowest_lap, 3),
                "Pace Drop-off": round(pace_drop_off, 3),
                "Degradation Rate (s/lap)": round(raw_degradation, 4),
                "Fuel-Adj Deg Rate (s/lap)": round(fuel_adj_degradation, 4),
                "Pace Std Dev": round(pace_std_dev, 3),
            })

        return pd.DataFrame(results)

    @classmethod
    def process_file_bytes(cls, file_bytes: bytes, filename: str, fuel_correction: float = 0.035) -> pd.DataFrame:
        """
        Loads CSV/JSON file bytes directly into a DataFrame (ideal for APIs).
        """
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif filename.endswith(".json"):
            df = pd.read_json(io.BytesIO(file_bytes))
        else:
            raise ValueError("Unsupported file extension. Only CSV and JSON are supported.")

        analyzer = cls(df, fuel_correction_per_lap=fuel_correction)
        return analyzer.process_stints()

    # -----------------------------------------------------------------
    # METHOD 2: FOR LOCAL TESTING WITH HARDCODED FILE PATH
    # -----------------------------------------------------------------
    @classmethod
    def run_local_test(cls, file_path: Union[str, Path], output_prefix: str = "test_output") -> pd.DataFrame:
        """
        Helper method to run analysis locally using a hardcoded file path.
        Saves output CSV and JSON to disk.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path.resolve()}")

        print(f" Reading local file: {path.name}...")
        if path.suffix == ".csv":
            df = pd.read_csv(path)
        elif path.suffix == ".json":
            df = pd.read_json(path)
        else:
            raise ValueError("Unsupported file format. Only CSV or JSON supported.")

        analyzer = cls(df)
        result_df = analyzer.process_stints()

        # Export outputs
        csv_file = f"{output_prefix}_tyre_performance.csv"
        json_file = f"{output_prefix}_tyre_performance.json"

        result_df.to_csv(csv_file, index=False)
        result_df.to_json(json_file, orient="records", indent=4)

        print(f" Analysis Complete! Results saved to {csv_file} and {json_file}\n")
        return result_df

# =====================================================================
# LOCAL TESTING EXECUTION BLOCK
# =====================================================================
if __name__ == "__main__":
    # Hardcode your local file path here
    HARDCODED_FILE = "Silverstone_2024_race_laps.csv"

    try:
        # Run local test method
        summary_df = TyrePerformanceAnalyzer.run_local_test(
            file_path=HARDCODED_FILE,
            output_prefix="silverstone_2024"
        )

        # Print Preview
        print("--- Output Summary Preview ---")
        print(summary_df.head(10).to_string(index=False))

    except Exception as e:
        print(f"❌ Testing failed: {e}")