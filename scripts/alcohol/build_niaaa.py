"""NIAAA apparent per capita ethanol consumption, national, all beverages and spirits.
Source: data/raw/niaaa/pcyr1970-2024_final.txt (report #124 data file, updated 04/09/2026).
Table 1 of the report #124 PDF is typed below only as a check: the file must match it to 2 decimals. Usage: python3 scripts/alcohol/build_niaaa.py"""
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
R = lambda *p: os.path.join(ROOT, *p)
BEV = {"1": "spirits", "2": "wine", "3": "beer", "4": "all"}
rows = {}
for line in open(R("data/raw/niaaa/pcyr1970-2024_final.txt")):
    if not line[:4].isdigit() or line.split()[1] != "99": continue
    f = line.split()  # year geo bev gallons ethanol pop14 pc14 dec14 pop21 pc21 dec21 source abv eth_tv
    assert len(f) == 14, line
    y, b = int(f[0]), BEV[f[2]]
    pop14 = float(f[5]); pc14 = int(f[6]) / 1e4; pc21 = int(f[9]) / 1e4
    abv = f[12] if f[12] != "." else ""; eth_tv = f[13] if f[13] != "." else ""
    rows[(y, b)] = dict(year=y, bev=b, pc14=pc14, pc21=pc21,
                        pc14_tv=round(float(eth_tv) / pop14, 4) if eth_tv else None,
                        abv_tv=int(abv) / 1000 if abv else None)
# Check values: report #124 Table 1, all beverages and spirits, 2000-2024 (ages 14+, fixed ABV)
T1_ALL = {2024: 2.42, 2023: 2.47, 2022: 2.50, 2021: 2.54, 2020: 2.44, 2019: 2.38, 2018: 2.36, 2017: 2.35, 2016: 2.35,
          2015: 2.33, 2014: 2.32, 2013: 2.33, 2012: 2.34, 2011: 2.29, 2010: 2.26, 2009: 2.29, 2008: 2.31, 2007: 2.31,
          2006: 2.28, 2005: 2.25, 2004: 2.23, 2003: 2.22, 2002: 2.20, 2001: 2.18, 2000: 2.19}
T1_SPI = {2024: 1.07, 2023: 1.07, 2022: 1.06, 2021: 1.03, 2020: 0.95, 2019: 0.89, 2018: 0.87, 2017: 0.85, 2016: 0.83,
          2015: 0.81, 2014: 0.80, 2013: 0.79, 2012: 0.78, 2011: 0.76, 2010: 0.74, 2009: 0.73, 2008: 0.73, 2007: 0.72,
          2006: 0.71, 2005: 0.70, 2004: 0.68, 2003: 0.67, 2002: 0.64, 2001: 0.64, 2000: 0.64}
diffs = [(y, b, t, rows[(y, b)]["pc14"]) for T, b in ((T1_ALL, "all"), (T1_SPI, "spirits")) for y, t in T.items()
         if (y, b) in rows and abs(rows[(y, b)]["pc14"] - t) > 0.0051]
print("report #124 Table 1 vs #124 data file, differences:", diffs)
assert not diffs
import csv
os.makedirs(R("data/build/alcohol"), exist_ok=True)
with open(R("data/build/alcohol/niaaa_national.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["year", "bev", "pc14", "pc21", "pc14_timevarying_abv", "abv_timevarying"])
    for y in range(2000, 2025):
        for b, T in (("all", T1_ALL), ("spirits", T1_SPI)):
            r = rows.get((y, b), {})
            w.writerow([y, b, r["pc14"], r["pc21"], r["pc14_tv"], r["abv_tv"]])
for y in (2002, 2003, 2018, 2019, 2021, 2023):
    print(y, {b: (rows[(y, b)]["pc14"], rows[(y, b)]["pc21"], rows[(y, b)]["pc14_tv"], rows[(y, b)]["abv_tv"]) for b in ("all", "spirits", "beer", "wine")})
avg = lambda k, b, ys: sum(rows[(y, b)][k] for y in ys) / len(ys)
for k in ("pc14", "pc21", "pc14_tv"):
    a, z = avg(k, "all", (2002, 2003)), avg(k, "all", (2018, 2019))
    print(f"all beverages {k}: 2002-03 {a:.3f} -> 2018-19 {z:.3f}  {100*(z/a-1):+.1f}%")
