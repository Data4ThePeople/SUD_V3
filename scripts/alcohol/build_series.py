"""Alcohol data for thought: national alcohol-induced death rates (crude and age-adjusted)
and NSDUH alcohol measures, one CSV. Usage: python3 scripts/alcohol/build_series.py"""
import csv, re, os
import pandas as pd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
R = lambda *p: os.path.join(ROOT, *p)

# US 2000 standard population, 11 age groups (NCHS, per 1,000,000)
STD = {"< 1 year": 13818, "1-4 years": 55317, "5-14 years": 145565, "15-24 years": 138646,
       "25-34 years": 135573, "35-44 years": 162613, "45-54 years": 134834, "55-64 years": 87247,
       "65-74 years": 66037, "75-84 years": 44842, "85+ years": 15508}
assert sum(STD.values()) == 1_000_000

def cells(r):
    return [(a or b).replace("&lt;", "<") for a, b in re.findall(r'<c (?:l|c)="([^"]*)"|<c v="([^"]*)"', r)]
num = lambda s: float(s.replace(",", ""))

# 1) CDC's own crude and age-adjusted rates, 1999-2020 (D76 API)
t = open(R("data/raw/wonder_api/aar.xml"), errors="ignore").read()
cdc, year = {}, None
for r in re.findall(r"<r>(.*?)</r>", t, re.S):
    c = cells(r)
    if re.fullmatch(r"\d{4}", c[0]): year, c = int(c[0]), c[1:]
    if c and c[0] == "Alcohol-induced causes":
        cdc[year] = dict(deaths=int(num(c[1])), pop=int(num(c[2])), crude=num(c[3]), aar=num(c[4]))

# 2) age-specific deaths and population -> our own age-adjusted rate
def aar(groups):  # groups: {age: (deaths, pop)}
    return sum(STD[a] / 1e6 * d / p * 1e5 for a, (d, p) in groups.items())

ages = {}
SUPP = []
t = open(R("data/raw/wonder_api/age.xml"), errors="ignore").read()
year = cause = None
for r in re.findall(r"<r>(.*?)</r>", t, re.S):
    c = cells(r)
    if re.fullmatch(r"\d{4}", c[0]): year, c = int(c[0]), c[1:]
    if c and c[0].endswith("causes"): cause, c = c[0], c[1:]
    if cause == "Alcohol-induced causes" and c and c[0] in STD:
        ages.setdefault(("D76", year), {})[c[0]] = (num(c[1]), num(c[2]))
with open(R("data/raw/wonder/mcd_2018_2024_year_age_alcohol.csv")) as f:
    for row in csv.DictReader(f):
        if row["Ten-Year Age Groups"] in STD and row["Year"]:
            dd = row["Deaths"]
            if dd == "Suppressed":  # 1-9 deaths; counted as 0, bound checked below
                SUPP.append((int(row["Year"]), row["Ten-Year Age Groups"], num(row["Population"]))); dd = "0"
            ages.setdefault(("D158", int(row["Year"])), {})[row["Ten-Year Age Groups"]] = (num(dd), num(row["Population"]))

def full(groups):  # zero-death groups are absent from D76; their contribution is 0
    return {a: groups.get(a, (0, 1)) for a in STD}

out = {}
for (db, y), g in sorted(ages.items()):
    d = sum(v[0] for v in g.values())
    p = sum(v[1] for v in full(g).values() if v[1] > 1)
    out.setdefault(y, {})[db] = dict(deaths=d, aar=aar(full(g)), crude=d / p * 1e5 if db == "D158" else None)

for y, a, p in SUPP: print('suppressed', y, a, 'max AAR effect if 9 deaths:', round(STD[a] / 1e6 * 9 / p * 1e5, 4))
# check method against CDC's published AAR
diffs = [(y, round(out[y]["D76"]["aar"], 2), cdc[y]["aar"]) for y in cdc if "D76" in out.get(y, {})]
bad = [x for x in diffs if abs(x[1] - x[2]) > 0.051]
print("our AAR vs CDC AAR, 1999-2020: max diff", max(abs(a - b) for _, a, b in diffs), "bad", bad)
for y in (2018, 2019, 2020):
    print(y, "D158 our AAR", round(out[y]["D158"]["aar"], 2), "CDC D76", cdc[y]["aar"],
          "deaths", out[y]["D158"]["deaths"], cdc[y]["deaths"])

rows = []
for y in range(1999, 2025):
    if y <= 2020:
        rows.append(dict(year=y, deaths=cdc[y]["deaths"], crude=cdc[y]["crude"], age_adjusted=cdc[y]["aar"], source="CDC WONDER D76, CDC's rates"))
    else:
        o = out[y]["D158"]
        rows.append(dict(year=y, deaths=int(o["deaths"]), crude=round(o["crude"], 1), age_adjusted=round(o["aar"], 1),
                         source="CDC WONDER Multiple Cause 2018-2024 (underlying cause filter), age-adjusted by us (2000 US standard)"))
deaths = pd.DataFrame(rows)

# 3) NSDUH national: past-month use, binge, AUD (12+), from the SAE files
sae = []
for f, outs in [("data/raw/nsduh/sae_dataset_1999-2019/NSDUH_99_19_state_saes_final.sas7bdat", ["ALCMON", "BNGALC", "ABODALC"]),
                ("data/raw/nsduh/sae_dataset_2021-2024/state_saes_final_2124.sas7bdat", ["ALCMON", "BNGDRK", "UDYR5ALC"])]:
    d = pd.read_sas(R(f), encoding="latin1")
    d = d[(d.outcome.isin(outs)) & (d.agegrp == 0) & (d.stname.str.strip() == "National")].copy()
    # 2-year windows only, 2002-2003 on (2002 is SAMHSA's new baseline); 2010-2011 "(published)" as in the map
    d["pyearnm"] = d.pyearnm.str.replace(" (published)", "", regex=False)
    d = d[d.pyearnm.str.fullmatch(r"\d{4}-\d{4}") & (d.pyearnm.str[:4].astype(int) >= 2002)]
    for _, r in d.iterrows():
        sae.append(dict(window=r.pyearnm.strip(), end_year=int(str(r.pyearnm).strip()[-4:]), outcome=r.outcome,
                        pct=round(r.BSAE * 100, 2), lo=round(r.low_sae * 100, 2), hi=round(r.up_sae * 100, 2),
                        outname=r.outname.strip()))
sae = pd.DataFrame(sae).sort_values(["outcome", "end_year"])
os.makedirs(R("data/build/alcohol"), exist_ok=True)
deaths.to_csv(R("data/build/alcohol/deaths_national.csv"), index=False)
sae.to_csv(R("data/build/alcohol/nsduh_national.csv"), index=False)
print(deaths.to_string(index=False)); print(sae.to_string(index=False))
