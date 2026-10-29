"""Sensitivity: % change from deaths/population (unrounded) vs from printed 1-decimal crude rates."""
import csv, sys
wdir = sys.argv[1]
for f in ["ucd_2018_2024_state_year.csv", "ucd_2018_2024_state_year_drug.csv", "ucd_2018_2024_state_year_alcohol.csv"]:
    d = {}
    for r in csv.DictReader(open(f"{wdir}/{f}", newline="")):
        if r.get("State Code") and r.get("Year Code", "").strip() in ("2019", "2024"):
            d[(r["State"], int(r["Year Code"]))] = (float(r["Deaths"]), float(r["Population"]), float(r["Crude Rate"]))
    states = sorted({k[0] for k in d}); flips = []; maxd = (0, None)
    for s in states:
        a, b = d[(s, 2019)], d[(s, 2024)]
        p1 = (b[2] - a[2]) / a[2] * 100
        p2 = ((b[0] / b[1]) / (a[0] / a[1]) - 1) * 100
        if (p1 > 0) != (p2 > 0) or (p1 == 0) != (p2 == 0) or round(p1) != round(p2): flips.append((s, round(p1, 2), round(p2, 2)))
        if abs(p1 - p2) > maxd[0]: maxd = (abs(p1 - p2), s)
    print(f, "max abs diff (pts):", round(maxd[0], 2), maxd[1], "| displayed-integer or sign differences:", flips)
