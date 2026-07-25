import fastf1
import pandas as pd
from pathlib import Path

# ========================= CONFIG =========================
YEAR = 2024
GRAND_PRIX = "Silverstone"   # British GP

# Setup cache
cache_dir = Path("cache")
cache_dir.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(cache_dir))

print(f"Loading {YEAR} {GRAND_PRIX} Race...\n")
# =======================================================

session = fastf1.get_session(YEAR, GRAND_PRIX, "R")
session.load()                    # ← No quiet=True

results = session.results

# Build the required schema
df = pd.DataFrame({
    "driver_code": results["Abbreviation"],
    "driver_name": results["FullName"],
    "team": results["TeamName"],
    "grid_position": results["GridPosition"].astype("Int64"),   # handles NaN better
    "finish_position": results["Position"].astype("Int64"),
    "race_time_status": results["Time"].astype(str)
})

# Replace NaT with proper status (DNF, DSQ, etc.)
mask = df["race_time_status"] == "NaT"
df.loc[mask, "race_time_status"] = results.loc[mask, "Status"]

# Optional: nicer time formatting (uncomment if you want)
# df["race_time_status"] = df["race_time_status"].str.replace(r'^0 days ', '', regex=True)

print("Preview of results:")
print(df[["driver_code", "driver_name", "team", "finish_position", "race_time_status"]].head(10))

# Export
df.to_csv("silverstone_2024_basic_results.csv", index=False)
df.to_json("silverstone_2024_basic_results.json", orient="records", indent=4)

print("\n✅ Files exported successfully!")
print(f"Total drivers: {len(df)}")
