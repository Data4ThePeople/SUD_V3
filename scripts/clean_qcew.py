"""Tidy QCEW rows for the 51 states and the U.S. total.

Output data/clean/qcew.csv: year, fips, state, naics, own, estabs, emp, emp_suppressed, estabs_suppressed.
Suppression rules (from the raw files, see DATASETS.md):
  - disclosure_code 'N' means employment is withheld; BLS writes 0 in its place. emp -> empty.
  - An establishment count of 0 on a row that exists means the count was withheld too
    (every N row in 2001-2003, and a few later ones). estabs -> empty.
  - A state with no row for a code/ownership has no such establishments that year (BLS omits empty cells).
No value is filled or estimated.
"""
import glob
from pathlib import Path
import pandas as pd
from states import BY_FIPS

ROOT = Path(__file__).resolve().parents[1]


def load_raw():
    frames = []
    for f in sorted(glob.glob(str(ROOT / "data/raw/qcew/qcew_*.csv"))):
        d = pd.read_csv(f, dtype=str)
        d["estab_raw"] = d["annual_avg_estabs"] if "annual_avg_estabs" in d else d["annual_avg_estabs_count"]
        frames.append(d)
    return pd.concat(frames, ignore_index=True)


def main():
    df = load_raw()
    keep = (df.agglvl_code == "18") | ((df.agglvl_code == "58") & df.area_fips.str[:2].isin(BY_FIPS))
    df = df[keep].copy()
    df["fips"] = df.area_fips.str[:2].where(df.agglvl_code == "58", "US")
    df["state"] = df.fips.map(lambda f: BY_FIPS[f][1] if f in BY_FIPS else "United States")
    df["emp_suppressed"] = df.disclosure_code.eq("N")
    est = pd.to_numeric(df.estab_raw)
    df["estabs_suppressed"] = est.eq(0)
    df["estabs"] = est.mask(df.estabs_suppressed)
    df["emp"] = pd.to_numeric(df.annual_avg_emplvl).mask(df.emp_suppressed)
    out = df.rename(columns={"industry_code": "naics", "own_code": "own"})[
        ["year", "fips", "state", "naics", "own", "estabs", "emp", "emp_suppressed", "estabs_suppressed"]]
    out["year"] = out.year.astype(int)
    if out.duplicated(["year", "fips", "naics", "own"]).any():
        raise SystemExit("duplicate year/fips/naics/own keys in QCEW")
    out.sort_values(["naics", "own", "year", "fips"]).to_csv(ROOT / "data/clean/qcew.csv", index=False)
    print(len(out), "rows written")


if __name__ == "__main__":
    main()
