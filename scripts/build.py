"""Join the cleaned sources into data/build/panel.csv and data/build/dashboard.json.

The page's "treatment workers" are OEWS counselors and social workers (oews below).

One row per geography (51 states + United States) and year, 2001-2024.
Every value is either published by the source or a ratio of two published values.
Nothing is filled, interpolated or estimated. See DATASETS.md for each source.

Metrics
  sud_pct, sud_lo, sud_hi      NSDUH prevalence (%, age 12+), window assigned to its end year
  sud_count, _lo, _hi          NSDUH published count (people, age 12+)
  sud_drug_*, sud_alcohol_*    the same for SAMHSA's drug and alcohol use disorder measures
  estabs                       N-SSATS / N-SUMHSS facilities offering outpatient SUD care
  estabs_per100k               estabs / WONDER population * 100,000
  oews                         OEWS 21-1011 + 21-1014 (to 2016) or 21-1018 (2017 on) + 21-1023; blank
                               unless every part is published. This is "workers" on the page.
  gap                          sud_count / oews (people with SUD per treatment worker)
  deaths, death_rate           WONDER drug overdose + alcohol-induced, crude rate per 100,000
  deaths_drug, deaths_alcohol  the two parts, with their published crude rates
"""
import json
from pathlib import Path
import pandas as pd
from states import STATES, BY_NAME

ROOT = Path(__file__).resolve().parents[1]
YEARS = range(2001, 2025)
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


def nsduh_part(part):
    """Drug or alcohol use disorder (SAMHSA's own measure), for the Drug only / Alcohol only views."""
    d = pd.read_csv(ROOT / f"data/clean/nsduh_{part}.csv")
    k, p = 1000, f"sud_{part}"
    return pd.DataFrame({
        "geo": d.state, "year": d.end_year, f"{p}_pct": d.pct, f"{p}_lo": d.pct_lo, f"{p}_hi": d.pct_hi,
        f"{p}_count": d.count_thousands * k, f"{p}_count_lo": d.count_lo * k, f"{p}_count_hi": d.count_hi * k,
    })


def facilities():
    d = pd.read_csv(ROOT / "data/clean/nsumhss_outpatient.csv")
    d = d[d.state.isin(POSTAL_TO_NAME)].assign(geo=lambda x: x.state.map(POSTAL_TO_NAME))
    st = d[["geo", "year", "facilities_sud_outpatient"]].rename(columns={"facilities_sud_outpatient": "estabs"})
    # national = 50 states + DC (territories left out to match the rest of the dashboard); a year
    # with no survey stays empty
    us = st.groupby("year").estabs.sum(min_count=51).reset_index().assign(geo="United States")
    return pd.concat([st, us])


OEWS_PARTS = {"old": ["21-1011", "21-1014", "21-1023"], "new": ["21-1018", "21-1023"]}


def oews():
    """OEWS clinicians: substance abuse + mental health counselors (21-1011 + 21-1014 through
    2016; 21-1018, which BLS formed from those two, from 2017) plus mental health and
    substance abuse social workers (21-1023). Complete only when every part is published."""
    o = pd.read_csv(ROOT / "data/clean/oews_counselors.csv")
    o = o[o.state_name.isin(GEOS[:-1])].rename(columns={"state_name": "geo"})
    nat = pd.read_csv(ROOT / "data/clean/oews_counselors_sumcheck.csv")
    nat = pd.DataFrame({"geo": "United States", "year": nat.year, "soc": nat.soc,
                        "employment": nat.national_employment, "rse": nat.national_rse,
                        "flag": nat.national_flag})
    o = pd.concat([o[["geo", "year", "soc", "employment", "rse", "flag"]], nat])
    rows = []
    for (geo, year), g in o.groupby(["geo", "year"]):
        parts = OEWS_PARTS["new"] if year >= 2017 else OEWS_PARTS["old"]
        g = g.set_index("soc").reindex(parts)
        ok = g.employment.notna().all() and not g.flag.eq("**").any()
        rows.append(dict(geo=geo, year=year, oews=g.employment.sum() if ok else None,
                         oews_rse_max=g.rse.max() if ok and g.rse.notna().any() else None))
    return pd.DataFrame(rows)


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
    if v is None:
        return None
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
    for part in (nsduh(), nsduh_part("drug"), nsduh_part("alcohol"), facilities(), oews(), deaths()):
        if part.duplicated(["geo", "year"]).any():
            raise SystemExit("duplicate geo/year keys in a source")
        panel = panel.merge(part, on=["geo", "year"], how="left")
    if len(panel) != len(GEOS) * len(YEARS):
        raise SystemExit("join changed the row count")

    panel["estabs_per100k"] = panel.estabs / panel.population * 1e5
    panel["gap"] = panel.sud_count / panel.oews

    panel.to_csv(ROOT / "data/build/panel.csv", index=False)

    for name, meta in VARIANTS.items():
        write_variant(panel, name, meta)
    print(f"{len(panel)} rows")


# Treatment workers on the page: OEWS counselors and social workers (Eric, 2026-10-28).
VARIANTS = {
    "v1_oews": dict(
        workers=lambda p: p.oews,
        flag=lambda p: pd.Series([None] * len(p), index=p.index),
        note=lambda p: p.oews_rse_max,
    ),
}


def change_tests(fips):
    """SAMHSA's own tests of change (data/clean/nsduh_change.csv), keyed by comparison, part and
    geography: [from %, to %, p value, result]. Nothing is computed here."""
    d = pd.read_csv(ROOT / "data/clean/nsduh_change.csv")
    out = {}
    for r in d.itertuples():
        comp = "alc10" if r.window_from == "2008-2009" else "sud1"
        key = "US" if r.state == "United States" else fips[r.state]
        out.setdefault(comp, {}).setdefault(r.part, {})[key] = [r.pct_from, r.pct_to, r.p_value, r.change]
    for comp, parts in out.items():
        for part, geos in parts.items():
            if len(geos) != 52:
                raise SystemExit(f"change {comp} {part}: {len(geos)} geographies, expected 52")
    return out


def write_variant(panel, name, meta):
    p = panel.copy()
    p["v_workers"] = meta["workers"](p)
    p["v_flag"] = meta["flag"](p)
    p["v_note"] = meta["note"](p)
    fips = {n: f for f, _, n in STATES}
    postal = {n: p for _, p, n in STATES}
    keep = {"sud_pct": "sud_pct", "sud_lo": "sud_lo", "sud_hi": "sud_hi", "sud_count": "sud_count",
            "sud_count_lo": "sud_count_lo", "sud_count_hi": "sud_count_hi", "sud_dsm": "sud_dsm",
            **{f"sud_{pt}_{c}": f"sud_{pt}_{c}" for pt in ("drug", "alcohol")
               for c in ("pct", "lo", "hi", "count", "count_lo", "count_hi")},
            "estabs": "estabs", "population": "population", "v_workers": "workers",
            "v_flag": "workers_flag", "v_note": "workers_note", "deaths": "deaths",
            "death_rate": "death_rate", "death_rate_lo": "death_rate_lo", "death_rate_hi": "death_rate_hi",
            "deaths_drug": "deaths_drug", "death_rate_drug": "death_rate_drug",
            "deaths_alcohol": "deaths_alcohol", "death_rate_alcohol": "death_rate_alcohol"}
    data = {}
    for geo, g in p.groupby("geo"):
        g = g.sort_values("year")
        key = "US" if geo == "United States" else fips[geo]
        data[key] = {"name": geo, "abbr": postal.get(geo, "US"),
                     **{out: [jsonable(v) for v in g[src]] for src, out in keep.items()}}
    out = {"variant": name, "years": list(YEARS), "geo": data, "change": change_tests(fips),
           "paths": json.loads((ROOT / "data/build/state_paths.json").read_text())}
    (ROOT / "data/build/dashboard.json").write_text(json.dumps(out, separators=(",", ":")))
    print(f"dashboard.json {len(json.dumps(out)) // 1024} KB")


if __name__ == "__main__":
    main()
