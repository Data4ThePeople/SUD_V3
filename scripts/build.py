"""Join the cleaned sources into data/build/panel.csv and data/build/dashboard.json.

One row per geography (51 states + United States) and year, 2001-2024.
Every value is either published by the source or a ratio of two published values.
Nothing is filled, interpolated or estimated. See DATASETS.md for each source.

Metrics
  sud_pct, sud_lo, sud_hi      NSDUH prevalence (%, age 12+), window assigned to its end year
  sud_count, _lo, _hi          NSDUH published count (people, age 12+)
  estabs                       N-SSATS / N-SUMHSS facilities offering outpatient SUD care
  estabs_per100k               estabs / WONDER population * 100,000
  workers                      QCEW annual average employment, NAICS 621420 + 621330 + 621112,
                               private + state + local; sum of disclosed cells
  workers_floor                True when any of those cells is withheld, so workers is a minimum
  workers_private(_floor)      the same, private ownership only (shown only where workers stand alone)
  gap                          sud_count / workers (people with SUD per worker); when workers_floor
                               is True the value is only a maximum, and the map shows it hatched gray
  deaths, death_rate           WONDER drug overdose + alcohol-induced, crude rate per 100,000
  deaths_drug, deaths_alcohol  the two parts, with their published crude rates
"""
import json
from pathlib import Path
import pandas as pd
from states import STATES, BY_NAME

ROOT = Path(__file__).resolve().parents[1]
YEARS = range(2001, 2025)
NAICS = ["621420", "621330", "621112"]
OWN = ["5", "2", "3"]
POSTAL_TO_NAME = {p: n for _, p, n in STATES}
GEOS = [n for _, _, n in STATES] + ["United States"]


def nsduh():
    d = pd.read_csv(ROOT / "data/clean/nsduh_sud.csv")
    k = 1000
    return pd.DataFrame({
        "geo": d.state, "year": d.end_year, "sud_window": d.window, "sud_dsm": d.dsm.astype(str),
        "sud_pct": d.pct, "sud_lo": d.pct_lo, "sud_hi": d.pct_hi,
        "sud_count": d.count_thousands * k, "sud_count_lo": d.count_lo * k, "sud_count_hi": d.count_hi * k,
    })


def facilities():
    d = pd.read_csv(ROOT / "data/clean/nsumhss_outpatient.csv")
    d = d[d.state.isin(POSTAL_TO_NAME)].assign(geo=lambda x: x.state.map(POSTAL_TO_NAME))
    st = d[["geo", "year", "facilities_sud_outpatient"]].rename(columns={"facilities_sud_outpatient": "estabs"})
    # national = 50 states + DC (territories left out to match the rest of the dashboard); a year
    # with no survey stays empty
    us = st.groupby("year").estabs.sum(min_count=51).reset_index().assign(geo="United States")
    return pd.concat([st, us])


def workers():
    q = pd.read_csv(ROOT / "data/clean/qcew.csv", dtype={"fips": str, "naics": str, "own": str})
    q = q[q.naics.isin(NAICS) & q.own.isin(OWN)]
    g = q.groupby(["state", "year"])
    out = pd.DataFrame({
        "workers": g.emp.sum(min_count=1),
        "workers_floor": g.emp_suppressed.any(),
        "workers_withheld_cells": g.emp_suppressed.sum(),
    }).reset_index().rename(columns={"state": "geo"})
    # private-only view, for when workers are shown on their own (not in the Gap Score)
    pq = q[q.own == "5"].groupby(["state", "year"])
    priv = pd.DataFrame({"workers_private": pq.emp.sum(min_count=1),
                         "workers_private_floor": pq.emp_suppressed.any()}).reset_index()
    out = out.merge(priv.rename(columns={"state": "geo"}), on=["geo", "year"], how="left")
    # breakdown by code for the cards (disclosed only)
    by = q.pivot_table(index=["state", "year"], columns="naics", values="emp", aggfunc="sum").reset_index()
    by = by.rename(columns={"state": "geo", **{c: f"workers_{c}" for c in NAICS}})
    return out.merge(by, on=["geo", "year"], how="left")


def deaths():
    w = pd.read_csv(ROOT / "data/clean/wonder.csv")
    parts = []
    for series, prefix in (("all", ""), ("drug", "_drug"), ("alcohol", "_alcohol")):
        x = w[w.series == series]
        cols = {"deaths": f"deaths{prefix}", "crude_rate": f"death_rate{prefix}"}
        if series == "all":
            cols.update(population="population", rate_lo="death_rate_lo", rate_hi="death_rate_hi")
        parts.append(x.rename(columns={"state": "geo", **cols})[["geo", "year", *cols.values()]])
    out = parts[0]
    for p in parts[1:]:
        out = out.merge(p, on=["geo", "year"], how="left")
    # WONDER's national export has the combined total only. The drug/alcohol split for the
    # U.S. is the sum of the 51 published state counts (none suppressed; the combined state
    # sum equals the national figure exactly, see validate_sums.py).
    st = out[out.geo != "United States"]
    for part in ("drug", "alcohol"):
        tot = st.groupby("year")[f"deaths_{part}"].sum(min_count=51)
        us = out.geo == "United States"
        out.loc[us, f"deaths_{part}"] = out.loc[us, "year"].map(tot)
        out.loc[us, f"death_rate_{part}"] = out.loc[us, f"deaths_{part}"] / out.loc[us, "population"] * 1e5
    return out


def jsonable(v):
    if isinstance(v, str):
        return v
    if pd.isna(v):
        return None
    if isinstance(v, (bool, pd.BooleanDtype().type)) or type(v).__name__ == "bool_":
        return bool(v)
    return round(float(v), 4)


def main():
    base = pd.DataFrame([(g, y) for g in GEOS for y in YEARS], columns=["geo", "year"])
    panel = base
    for part in (nsduh(), facilities(), workers(), deaths()):
        if part.duplicated(["geo", "year"]).any():
            raise SystemExit("duplicate geo/year keys in a source")
        panel = panel.merge(part, on=["geo", "year"], how="left")
    if len(panel) != len(GEOS) * len(YEARS):
        raise SystemExit("join changed the row count")

    panel["estabs_per100k"] = panel.estabs / panel.population * 1e5
    panel["gap"] = panel.sud_count / panel.workers
    for c in ("workers_floor", "workers_private_floor"):
        panel[c] = panel[c].fillna(False).astype(bool)

    panel.to_csv(ROOT / "data/build/panel.csv", index=False)

    fips = {n: f for f, _, n in STATES}
    postal = {n: p for _, p, n in STATES}
    keep = ["sud_pct", "sud_lo", "sud_hi", "sud_count", "sud_count_lo", "sud_count_hi", "sud_dsm",
            "estabs", "estabs_per100k", "workers", "workers_floor", "workers_withheld_cells",
            "workers_private", "workers_private_floor",
            *[f"workers_{c}" for c in NAICS], "gap", "population",
            "deaths", "death_rate", "death_rate_lo", "death_rate_hi",
            "deaths_drug", "death_rate_drug", "deaths_alcohol", "death_rate_alcohol"]
    data = {}
    for geo, g in panel.groupby("geo"):
        g = g.sort_values("year")
        key = "US" if geo == "United States" else fips[geo]
        data[key] = {"name": geo, "abbr": postal.get(geo, "US"), **{c: [jsonable(v) for v in g[c]] for c in keep}}
    out = {"years": list(YEARS), "geo": data,
           "paths": json.loads((ROOT / "data/build/state_paths.json").read_text())}
    (ROOT / "data/build/dashboard.json").write_text(json.dumps(out, separators=(",", ":")))
    print(f"{len(panel)} rows; dashboard.json {len(json.dumps(out)) // 1024} KB")


if __name__ == "__main__":
    main()
