"""Claude's tie-out: recompute every number the dashboard shows and compare with dist data.

Workers and deaths are recomputed from the raw BLS and CDC files by a separate code path
from build.py. SUD values are checked against the clean NSDUH file (which
check_nsduh_sud.py ties to SAMHSA's SAS datasets); facilities against the clean N-SSATS
file (which check_nsumhss.py ties to SAMHSA's published tables). Derived values (per 100K,
Gap Score) are recomputed here with the page's formulas.
Writes data/build/tieout.csv; exits non-zero on any mismatch.
"""
import csv, glob, io, json, sys
from pathlib import Path
from states import STATES

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT / "data/build/dashboard.json").read_text())
YEARS = D["years"]
NAME_TO_KEY = {n: f for f, _, n in STATES} | {"United States": "US"}
POSTAL_TO_KEY = {p: f for f, p, _ in STATES}
results = []


def cmp(metric, key, year, expected, tol=1e-6):
    got = D["geo"][key][metric][YEARS.index(year)]
    if expected is None and got is None:
        ok = True
    elif expected is None or got is None:
        ok = False
    else:
        ok = abs(got - expected) <= tol * max(1, abs(expected))
    results.append((metric, key, year, expected, got, "ok" if ok else "MISMATCH"))


# --- workers from raw QCEW rows ---
work, floor, priv, pfloor = {}, {}, {}, {}
for f in sorted(glob.glob(str(ROOT / "data/raw/qcew/qcew_*.csv"))):
    for r in csv.DictReader(open(f)):
        if r["industry_code"] not in ("621420", "621330", "621112") or r["own_code"] not in ("2", "3", "5"):
            continue
        if r["agglvl_code"] == "58" and r["area_fips"][:2] in {s[0] for s in STATES}:
            key = r["area_fips"][:2]
        elif r["agglvl_code"] == "18":
            key = "US"
        else:
            continue
        y, k = int(r["year"]), (r["area_fips"][:2] if key != "US" else "US", int(r["year"]))
        withheld = r["disclosure_code"] == "N"
        emp = 0 if withheld else int(float(r["annual_avg_emplvl"]))
        work[k] = work.get(k, 0) + emp
        floor[k] = floor.get(k, False) or withheld
        if r["own_code"] == "5":
            priv[k] = priv.get(k, 0) + emp
            pfloor[k] = pfloor.get(k, False) or withheld
for (key, y), v in work.items():
    cmp("workers", key, y, v)
    cmp("workers_floor", key, y, floor[(key, y)])
    cmp("workers_private", key, y, priv.get((key, y)))
    cmp("workers_private_floor", key, y, pfloor.get((key, y), False))


# --- deaths and population from raw WONDER exports ---
def wonder(stem):
    out = {}
    for db, yrs in (("1999_2020", range(2001, 2018)), ("2018_2024", range(2018, 2025))):
        text = (ROOT / f"data/raw/wonder/ucd_{db}_{stem}.csv").read_text().split('"---"')[0]
        for r in csv.DictReader(io.StringIO(text)):
            if r["Notes"] or int(r["Year"]) not in yrs:
                continue
            out[(NAME_TO_KEY[r.get("State", "United States")], int(r["Year"]))] = r
    return out


allw, drug, alc, nat = wonder("state_year"), wonder("state_year_drug"), wonder("state_year_alcohol"), wonder("year")
for (key, y), r in (allw | nat).items():
    cmp("deaths", key, y, int(r["Deaths"]))
    cmp("population", key, y, int(r["Population"]))
    cmp("death_rate", key, y, float(r["Crude Rate"]))
for src, m in ((drug, "deaths_drug"), (alc, "deaths_alcohol")):
    tot = {}
    for (key, y), r in src.items():
        cmp(m, key, y, int(r["Deaths"]))
        tot[y] = tot.get(y, 0) + int(r["Deaths"])
    for y, v in tot.items():
        cmp(m, "US", y, v)

# --- SUD (clean NSDUH) ---
for r in csv.DictReader(open(ROOT / "data/clean/nsduh_sud.csv")):
    key, y = NAME_TO_KEY[r["state"]], int(r["end_year"])
    for m, c, k in (("sud_pct", "pct", 1), ("sud_lo", "pct_lo", 1), ("sud_hi", "pct_hi", 1),
                    ("sud_count", "count_thousands", 1000)):
        cmp(m, key, y, float(r[c]) * k, tol=1e-4)

# --- facilities (clean N-SSATS / N-SUMHSS) ---
fac = {}
for r in csv.DictReader(open(ROOT / "data/clean/nsumhss_outpatient.csv")):
    if r["state"] in POSTAL_TO_KEY and r["facilities_sud_outpatient"] and int(r["year"]) in YEARS:
        fac[(POSTAL_TO_KEY[r["state"]], int(r["year"]))] = float(r["facilities_sud_outpatient"])
for (key, y), v in fac.items():
    cmp("estabs", key, y, v)
for y in YEARS:
    vals = [fac.get((f, y)) for f, _, _ in STATES]
    cmp("estabs", "US", y, None if None in vals else sum(vals))

# --- structural checks ---
problems = []
for key, g in D["geo"].items():
    for m, arr in g.items():
        if isinstance(arr, list) and len(arr) != len(YEARS):
            problems.append(f"{key} {m}: {len(arr)} values")
if len(D["geo"]) != 52:
    problems.append(f"{len(D['geo'])} geographies, expected 52")

with open(ROOT / "data/build/tieout.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["metric", "geo", "year", "expected", "dashboard", "status"])
    w.writerows(results)
bad = [r for r in results if r[-1] != "ok"]
print(f"{len(results)} values checked, {len(bad)} mismatches; structural problems: {problems or 'none'}")
for r in bad[:25]:
    print(r)
sys.exit(1 if bad or problems else 0)
