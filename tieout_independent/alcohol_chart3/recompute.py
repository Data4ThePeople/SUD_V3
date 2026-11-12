"""Independent recompute of chart 3 (beer to spirits) from NIAAA pcyr1970-2024_final.txt.
Usage: python -I recompute.py <path to data file>"""
import sys, csv, os

def num(s):
    s = s.strip()
    return None if s in ("", ".") else float(s)

rows = {}
with open(sys.argv[1], encoding="ascii") as f:
    for line in f:
        line = line.rstrip("\r\n")
        if not line[:4].isdigit():
            continue
        p = line.split()
        if len(p) != 14:
            continue
        yr, geo, typ = int(p[0]), int(p[1]), int(p[2])
        if geo != 99:
            continue
        rows[(yr, typ)] = dict(
            bev=num(p[3]), eth=num(p[4]), pop14=num(p[5]), pc14=num(p[6]),
            pop21=num(p[8]), abv=num(p[12]), eth_tv=num(p[13]))
        # Header layout says pop14 is cols 32-40; actual field is cols 33-41.
        assert line[32:41].strip() == p[5], (line, "pop14 position")

names = {1: "spirits", 2: "wine", 3: "beer", 4: "all"}
out = []
for y in range(2000, 2025):
    r = {t: rows[(y, t)] for t in (1, 2, 3, 4)}
    pop = r[4]["pop14"]
    for t in (1, 2, 3, 4):
        assert r[t]["pop14"] == pop
    gal = sum(r[t]["bev"] for t in (1, 2, 3))
    tv = {t: r[t]["eth_tv"] for t in (1, 2, 3)}
    tv_sum = sum(tv.values())
    fx = {t: r[t]["eth"] for t in (1, 2, 3)}
    d = dict(year=y, pop14=pop, bev_gal_pc=gal / pop,
             all_tv_row=r[4]["eth_tv"], tv_sum=tv_sum,
             avg_abv_tv=tv_sum / gal, avg_abv_fixed=sum(fx.values()) / gal,
             all_fixed_pc=r[4]["eth"] / pop, all_tv_pc=tv_sum / pop,
             all_pc14_file=r[4]["pc14"] / 1e4)
    for t in (1, 2, 3):
        d[f"{names[t]}_tv_pc"] = tv[t] / pop
        d[f"{names[t]}_fx_pc"] = fx[t] / pop
        d[f"{names[t]}_abv_tv"] = r[t]["abv"] / 1000
        d[f"{names[t]}_abv_implied_fixed"] = fx[t] / r[t]["bev"]
        d[f"{names[t]}_bev_pc"] = r[t]["bev"] / pop
        d[f"{names[t]}_share_tv"] = tv[t] / tv_sum
        d[f"{names[t]}_share_fx"] = fx[t] / sum(fx.values())
    out.append(d)

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "recomputed.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)

cols = ["year", "beer_tv_pc", "wine_tv_pc", "spirits_tv_pc", "all_tv_pc", "avg_abv_tv",
        "avg_abv_fixed", "bev_gal_pc", "beer_fx_pc", "wine_fx_pc", "spirits_fx_pc", "all_fixed_pc",
        "spirits_abv_tv", "beer_abv_tv", "wine_abv_tv", "all_tv_row", "tv_sum"]
print("\t".join(c[:12] for c in cols))
for d in out:
    print("\t".join(f"{d[c]:.4f}" if isinstance(d[c], float) and abs(d[c]) < 100 else str(d[c]) for c in cols))

# check file's own per capita field (all beverages, fixed) against eth/pop
for d in out:
    assert abs(d["all_fixed_pc"] - d["all_pc14_file"]) < 0.00006, d["year"]
print("per capita field check OK")
