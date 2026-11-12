"""Split change in average ABV 2002->2024 into mix vs within-type strength. Usage: python -I decompose.py recomputed.csv"""
import csv, sys
d = {int(r["year"]): r for r in csv.DictReader(open(sys.argv[1]))}
T = ["beer", "wine", "spirits"]
def vol(y): return {t: float(d[y][f"{t}_bev_pc"]) for t in T}
def abv(y): return {t: float(d[y][f"{t}_abv_tv"]) for t in T}
def avg(v, a): return sum(v[t]*a[t] for t in T) / sum(v.values())
a, b = 2002, 2024
print("avg tv", avg(vol(a), abv(a)), avg(vol(b), abv(b)))
print("2024 mix, 2002 ABVs (mix only):", avg(vol(b), abv(a)))
print("2002 mix, 2024 ABVs (strength only):", avg(vol(a), abv(b)))
for t in T: print(t, "vol share", vol(a)[t]/sum(vol(a).values()), vol(b)[t]/sum(vol(b).values()), "abv", abv(a)[t], abv(b)[t])
