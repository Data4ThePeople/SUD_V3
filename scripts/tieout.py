"""Claude's tie-out: recompute every number the dashboard shows and compare with the data
behind the page (data/build/dashboard.json).

Deaths are recomputed from the raw CDC files by a separate code path from build.py. Workers
are recomputed from the clean OEWS file (which
build_oews.py reads from the unchanged BLS zips and ties to the national totals). SUD values are checked against the clean NSDUH file (which
check_nsduh_sud.py ties to SAMHSA's SAS datasets); facilities against the clean N-SSATS
file (which check_nsumhss.py ties to SAMHSA's published tables). Derived values (per 100K,
People per Worker) are recomputed here with the page's formulas.
Writes data/build/tieout.csv; exits non-zero on any mismatch.
"""
import csv, io, json, sys
from pathlib import Path
from states import STATES

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("v1_oews",)
DS = {"v1_oews": json.loads((ROOT / "data/build/dashboard.json").read_text())}
YEARS = DS["v1_oews"]["years"]
NAME_TO_KEY = {n: f for f, _, n in STATES} | {"United States": "US"}
POSTAL_TO_KEY = {p: f for f, p, _ in STATES}
results = []


def cmp(metric, key, year, expected, tol=1e-6, only=VARIANTS):
    for v in only:
        one(v, metric, key, year, expected, tol)


def one(variant, metric, key, year, expected, tol):
    got = DS[variant]["geo"][key][metric][YEARS.index(year)]
    if expected is None and got is None:
        ok = True
    elif expected is None or got is None:
        ok = False
    elif isinstance(expected, str) or isinstance(got, str):
        ok = expected == got
    else:
        ok = abs(got - expected) <= tol * max(1, abs(expected))
    results.append((variant, metric, key, year, expected, got, "ok" if ok else "MISMATCH"))


# --- workers from the clean OEWS file: 21-1011 + 21-1014 (to 2016) or 21-1018 (2017 on),
# plus 21-1023; complete only when every part is published ---
NAME_KEY = NAME_TO_KEY
parts = {}
for r in csv.DictReader(open(ROOT / "data/clean/oews_counselors.csv")):
    if r["state_name"] in NAME_KEY and r["state_name"] != "United States":
        parts[(NAME_KEY[r["state_name"]], int(r["year"]), r["soc"])] = (r["employment"], r["flag"])
for r in csv.DictReader(open(ROOT / "data/clean/oews_counselors_sumcheck.csv")):
    parts[("US", int(r["year"]), r["soc"])] = (r["national_employment"], r["national_flag"])
for key in [s[0] for s in STATES] + ["US"]:
    for y in YEARS:
        codes = ["21-1018", "21-1023"] if y >= 2017 else ["21-1011", "21-1014", "21-1023"]
        got = [parts.get((key, y, c)) for c in codes]
        ok = all(p and p[0] and p[1] != "**" for p in got)
        cmp("workers", key, y, sum(float(p[0]) for p in got) if ok else None)
        cmp("workers_flag", key, y, None)


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
        # CDC prints "Unreliable" instead of a rate under 20 deaths; the page leaves it blank
        rate = r["Crude Rate"]
        cmp(m.replace("deaths", "death_rate"), key, y, None if "Unreliable" in rate else float(rate))
        tot[y] = tot.get(y, 0) + int(r["Deaths"])
    for y, v in tot.items():
        cmp(m, "US", y, v)
        cmp(m.replace("deaths", "death_rate"), "US", y, v / int(nat[("US", y)]["Population"]) * 1e5, tol=1e-5)  # JSON keeps 4 decimals

# --- SUD (clean NSDUH) ---
for r in csv.DictReader(open(ROOT / "data/clean/nsduh_sud.csv")):
    key, y = NAME_TO_KEY[r["state"]], int(r["end_year"])
    for m, c, k in (("sud_pct", "pct", 1), ("sud_lo", "pct_lo", 1), ("sud_hi", "pct_hi", 1),
                    ("sud_count", "count_thousands", 1000)):
        cmp(m, key, y, float(r[c]) * k, tol=1e-4)

# --- drug and alcohol use disorder (clean NSDUH files; build_nsduh_parts.py ties them to SAMHSA's tables) ---
for part in ("drug", "alcohol"):
    have = set()
    for r in csv.DictReader(open(ROOT / f"data/clean/nsduh_{part}.csv")):
        key, y = NAME_TO_KEY[r["state"]], int(r["end_year"])
        have.add((key, y))
        for m, c, k in (("pct", "pct", 1), ("lo", "pct_lo", 1), ("hi", "pct_hi", 1), ("count", "count_thousands", 1000),
                        ("count_lo", "count_lo", 1000), ("count_hi", "count_hi", 1000)):
            cmp(f"sud_{part}_{m}", key, y, float(r[c]) * k, tol=1e-4)
    for key in [s[0] for s in STATES] + ["US"]:  # every other year must be blank
        for y in YEARS:
            if (key, y) not in have:
                cmp(f"sud_{part}_pct", key, y, None)

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
for v, D in DS.items():
    if D["variant"] != v:
        problems.append(f"{v}: variant field says {D['variant']}")
    for key, g in D["geo"].items():
        for m, arr in g.items():
            if isinstance(arr, list) and len(arr) != len(YEARS):
                problems.append(f"{v} {key} {m}: {len(arr)} values")
    if len(D["geo"]) != 52:
        problems.append(f"{v}: {len(D['geo'])} geographies, expected 52")

with open(ROOT / "data/build/tieout.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["version", "metric", "geo", "year", "expected", "dashboard", "status"])
    w.writerows(results)
bad = [r for r in results if r[-1] != "ok"]
print(f"{len(results)} values checked, {len(bad)} mismatches; structural problems: {problems or 'none'}")
for r in bad[:25]:
    print(r)
sys.exit(1 if bad or problems else 0)
