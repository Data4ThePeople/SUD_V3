"""Source coverage: for each metric and year, how many of the 51 states have a published
value and how many have none. Workers are OEWS counselors and social workers, blank unless
every occupation is published.
Writes data/build/coverage.csv and prints a compact table."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
p = pd.read_csv(ROOT / "data/build/panel.csv")
st = p[p.geo != "United States"]
rows = []
for y, g in st.groupby("year"):
    rows.append(dict(
        year=y,
        sud_published=int(g.sud_pct.notna().sum()),
        facilities_published=int(g.estabs.notna().sum()),
        workers_published=int(g.oews.notna().sum()),
        people_per_worker=int(g.gap.notna().sum()),
        deaths_published=int(g.deaths.notna().sum()),
    ))
out = pd.DataFrame(rows)
out.to_csv(ROOT / "data/build/coverage.csv", index=False)
print(out.to_string(index=False))
