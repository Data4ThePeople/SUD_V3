"""State-to-national check, run on every build.

For each source and year, sum the 51 states and compare with the publisher's own
national figure. A year with any suppressed state cell is 'partial' (reported with the
suppressed count), not pass or fail. Exact sources fail the build when a fully
disclosed year misses by more than rounding.
Writes data/build/validate_sums.csv and exits non-zero on any FAIL.
"""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
rows = []


def check(source, measure, year, states, national, n_suppressed, tol):
    s = states.sum()
    if pd.isna(national):
        status = "no national figure"
    elif n_suppressed:
        status = "partial"
    else:
        status = "pass" if abs(s - national) <= tol else "FAIL"
    rows.append(dict(source=source, measure=measure, year=year, state_sum=s, national=national,
                     diff=None if pd.isna(national) else s - national, suppressed_states=n_suppressed,
                     tolerance=tol, status=status))


def nsduh():
    for f, label in (("nsduh_sud.csv", "SUD count (thousands)"), ("nsduh_drug.csv", "drug use disorder count (thousands)"),
                     ("nsduh_alcohol.csv", "alcohol use disorder count (thousands)")):
        d = pd.read_csv(ROOT / "data/clean" / f)
        for year, g in d.groupby("end_year"):
            st, us = g[g.state != "United States"], g[g.state == "United States"]
            # model-based totals in thousands; SAMHSA says U.S. = sum of states, so only rounding differs
            check("NSDUH", label, year, st.count_thousands, us.count_thousands.iloc[0],
                  int(st.count_thousands.isna().sum()), 5)


def wonder():
    w = pd.read_csv(ROOT / "data/clean/wonder.csv")
    for (series, year), g in w.groupby(["series", "year"]):
        st, us = g[g.state != "United States"], g[g.state == "United States"]
        for col in ("deaths", "population"):
            nat = us[col].iloc[0] if len(us) else float("nan")
            check("WONDER", f"{series} {col}", year, st[col], nat, int(st.suppressed.sum()), 0)


def main():
    for fn in (nsduh, wonder):
        fn()
    out = pd.DataFrame(rows)
    (ROOT / "data/build").mkdir(parents=True, exist_ok=True)
    out.to_csv(ROOT / "data/build/validate_sums.csv", index=False)
    summary = out.groupby(["source", "status"]).size().unstack(fill_value=0)
    print(summary.to_string())
    fails = out[out.status == "FAIL"]
    if len(fails):
        print(fails.to_string(index=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
