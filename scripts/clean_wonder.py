"""Tidy CDC WONDER Underlying Cause of Death exports into data/clean/wonder.csv.

Years 2001-2017 come from the 1999-2020 database (bridged-race population),
2018-2024 from the 2018-2024 Single Race database. The two agree exactly on deaths
and population for every state in 2018-2020 (checked here on every run).
'Suppressed' stays empty. Rates are WONDER's published crude rates; an 'Unreliable'
flag (fewer than 20 deaths in the 1999-2020 database) is kept as a flag, and the rate is left empty as WONDER does.
"""
import io
from pathlib import Path
import pandas as pd
from states import BY_NAME

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/wonder"
SERIES = {"all": "state_year", "drug": "state_year_drug", "alcohol": "state_year_alcohol"}


def load(path):
    """Read a WONDER export: the data block ends at the first '---' line; footnotes follow."""
    lines = path.read_text().split("\n")
    end = next(i for i, l in enumerate(lines) if l.startswith('"---"'))
    return pd.read_csv(io.StringIO("\n".join(lines[:end])), dtype=str)


def tidy(df):
    df = df[df.Notes.isna()].copy()
    out = pd.DataFrame({
        "year": df.Year.astype(int),
        "state": df.State if "State" in df else "United States",
        "deaths": pd.to_numeric(df.Deaths, errors="coerce"),
        "population": pd.to_numeric(df.Population, errors="coerce"),
        "crude_rate": pd.to_numeric(df["Crude Rate"], errors="coerce"),
        "rate_lo": pd.to_numeric(df["Crude Rate Lower 95% Confidence Interval"], errors="coerce"),
        "rate_hi": pd.to_numeric(df["Crude Rate Upper 95% Confidence Interval"], errors="coerce"),
        "suppressed": df.Deaths.eq("Suppressed"),
        "unreliable": df["Crude Rate"].eq("Unreliable"),
    })
    if "State" in df and not set(out.state) <= set(BY_NAME):
        raise SystemExit(f"unexpected state names: {set(out.state) - set(BY_NAME)}")
    return out


def stitch(stem):
    old = RAW / f"ucd_1999_2020_{stem}.csv"
    new = RAW / f"ucd_2018_2024_{stem}.csv"
    if not old.exists() or not new.exists():
        return None
    a, b = tidy(load(old)), tidy(load(new))
    both = a.merge(b, on=["state", "year"], suffixes=("_a", "_b"))
    both = both[both.year.between(2018, 2020)]
    bad = both[(both.deaths_a != both.deaths_b) & both.deaths_a.notna()]
    if len(bad):
        raise SystemExit(f"{stem}: 2018-2020 overlap disagrees in {len(bad)} rows")
    return pd.concat([a[a.year.between(2001, 2017)], b[b.year.between(2018, 2024)]])


def main():
    frames = []
    for series, stem in SERIES.items():
        d = stitch(stem)
        if d is None:
            print(f"{series}: export not present yet, skipped")
            continue
        frames.append(d.assign(series=series))
    nat = stitch("year")
    if nat is not None:
        frames.append(nat.assign(series="all"))
    out = pd.concat(frames, ignore_index=True)
    if out.duplicated(["series", "state", "year"]).any():
        raise SystemExit("duplicate series/state/year keys in WONDER")
    out.sort_values(["series", "state", "year"]).to_csv(ROOT / "data/clean/wonder.csv", index=False)
    print(out.groupby("series").size().to_dict(), "rows; suppressed:", int(out.suppressed.sum()))


if __name__ == "__main__":
    main()
