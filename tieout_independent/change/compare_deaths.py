"""Recompute 2019->2024 crude death-rate % change from WONDER exports; compare with page."""
import csv, json, sys
wdir, pagejson = sys.argv[1], sys.argv[2]
P = json.load(open(pagejson)); yi = {y: i for i, y in enumerate(P["years"])}
def load(f):
    out = {}
    with open(f"{wdir}/{f}", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("State Code") or not r.get("Year Code"): continue
            yc = r["Year Code"].strip()
            if yc not in ("2019", "2024"): continue
            rate = r["Crude Rate"].strip()
            out[(r["State Code"].strip(), int(yc))] = (r["Deaths"].strip(), rate, r["Notes"].strip())
    return out
fmtPct = lambda v: ("+" if v > 0 else "-" if v < 0 else "") + str(int(abs(v) + 0.5)) + "%"   # JS Math.round on abs, positive
res = {}; tot = diffs = 0
for part, f, key in [("all", "ucd_2018_2024_state_year.csv", "death_rate"), ("drug", "ucd_2018_2024_state_year_drug.csv", "death_rate_drug"), ("alcohol", "ucd_2018_2024_state_year_alcohol.csv", "death_rate_alcohol")]:
    W = load(f); rows = []; nodata = []
    for k, g in P["geo"].items():
        if k == "US": continue
        a, b = W.get((k, 2019)), W.get((k, 2024))
        def num(x):
            try: return float(x[1])
            except Exception: return None
        ra, rb = num(a) if a else None, num(b) if b else None
        pa, pb = g[key][yi[2019]], g[key][yi[2024]]
        for mine, pg, y in ((ra, pa, 2019), (rb, pb, 2024)):
            tot += 1
            if mine != pg: diffs += 1; print("RATE DIFF", part, g["name"], y, "page", pg, "wonder", mine)
        if ra is None or rb is None: nodata.append((g["name"], a, b)); continue
        mypct = (rb - ra) / ra * 100
        pgpct = None if pa is None or pb is None else (pb - pa) / pa * 100
        tot += 1
        if pgpct is None or abs(pgpct - mypct) > 1e-9: diffs += 1; print("PCT DIFF", part, g["name"], pgpct, mypct)
        rows.append((g["name"], ra, rb, mypct))
    rows.sort(key=lambda r: -r[3])
    rose = sum(r[3] > 0 for r in rows); fell = sum(r[3] < 0 for r in rows); same = sum(r[3] == 0 for r in rows)
    beyond = [(r[0], round(r[3], 1)) for r in rows if abs(r[3]) > 60]
    res[part] = dict(ranking_line=f"highest first · {rose} rose · {fell} fell" + (f" · {same} unchanged" if same else "") + (f" · {len(nodata)} with no data" if nodata else ""),
                     nodata=nodata, top5=[(r[0], r[1], r[2], round(r[3], 2), fmtPct(r[3])) for r in rows[:5]],
                     bottom5=[(r[0], r[1], r[2], round(r[3], 2), fmtPct(r[3])) for r in rows[-5:]],
                     beyond_60=beyond, near_half=[(r[0], r[3]) for r in rows if abs(abs(r[3]) % 1 - 0.5) < 0.01])
    with open(f"death_change_{part}.csv", "w") as fh:
        fh.write("state,rate_2019,rate_2024,pct_change,display\n")
        for r in rows: fh.write(f"{r[0]},{r[1]},{r[2]},{r[3]:.4f},{fmtPct(r[3])}\n")
print("rate/pct values compared:", tot, "differences:", diffs)
print(json.dumps(res, indent=1))
