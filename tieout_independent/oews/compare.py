"""Compare page workers, workers_note, and People per Worker with an independent rebuild.
usage: compare.py <dist/index.html> <oews_rows.csv> <sae9919.pkl> <sae2124.pkl> <out_diffs.csv>"""
import sys, json, re, math, pandas as pd
html, rowsf, p1, p2, outf = sys.argv[1:6]
s = open(html, encoding="utf-8").read()
i = s.index("const D = ") + len("const D = ")
D, _ = json.JSONDecoder().raw_decode(s[i:])
Y = D["years"]
geos = [k for k in D["geo"]]
print("variant", D.get("variant"), "geo keys", len(geos), "years", Y[0], Y[-1])

r = pd.read_csv(rowsf, dtype=str)
def num(x):
    x = str(x).replace(",", "").strip()
    try: return float(x)
    except: return None
r["emp"] = r.tot_emp.map(num); r["rse"] = r.emp_prse.map(num)
lk = {(a.fips, int(a.year), a.occ): (a.emp, a.rse) for a in r.itertuples()}

def mine(f, y):
    codes = ["21-1011", "21-1014", "21-1023"] if y <= 2016 else ["21-1018", "21-1023"]
    parts = [lk.get((f, y, c)) for c in codes]
    if any(p is None or p[0] is None or math.isnan(p[0]) for p in parts):
        why = ["missing row" if p is None else ("**" if (p[0] is None or math.isnan(p[0])) else "ok") for p in parts]
        return None, None, dict(zip(codes, why))
    return sum(p[0] for p in parts), max(p[1] for p in parts if p[1] is not None), None

# NSDUH counts (own, from earlier checked tie-out pickles)
a = pd.read_pickle(p1); b = pd.read_pickle(p2)
sel = pd.concat([a[(a.outcome.isin(["ABODILAL", "UDPYILAL"])) & (a.agegrp == 0)], b[(b.outcome == "UD5IAANY") & (b.agegrp == 0)]])
sel = sel[~sel.pyearnm.str.contains("updated")]
sel["end"] = sel.pyearnm.str.extract(r"-(\d{4})")[0].astype(float)
sel = sel[sel.end.notna()]
name2f = {g["name"]: f for f, g in D["geo"].items()}; name2f["National"] = "US"; name2f["Total U.S."] = "US"
sud = {}
for x in sel.itertuples():
    f = name2f.get(x.stname)
    if f: sud[(f, int(x.end))] = x.est_total * 1000

diffs = []; n_w = n_wb = n_note = n_ppw = 0; withheld = []; ppw_maxrel = 0
for f in geos:
    g = D["geo"][f]
    for k, y in enumerate(Y):
        pw = g["workers"][k]; pn = g.get("workers_note", [None]*24)[k]
        mw, mn, why = mine(f, y)
        n_wb += 1
        if why: withheld.append((f, g["name"], y, why))
        if (pw is None) != (mw is None):
            diffs.append(("workers blank/not", f, g["name"], y, pw, mw, why))
        elif mw is not None:
            n_w += 1
            if abs(pw - mw) > 0.5: diffs.append(("workers value", f, g["name"], y, pw, mw, ""))
            n_note += 1
            if pn is None or abs(pn - mn) > 0.051: diffs.append(("workers_note", f, g["name"], y, pn, mn, ""))
        elif pn is not None:
            diffs.append(("workers_note on blank", f, g["name"], y, pn, None, ""))
        fl = g.get("workers_flag", [None]*24)[k]
        if fl: diffs.append(("workers_flag set", f, g["name"], y, fl, None, ""))
        # People per worker
        ps = g["sud_count"][k]; ms = sud.get((f, y))
        pp = None if ps is None or pw is None else ps / pw
        mp = None if ms is None or mw is None else ms / mw
        if (pp is None) != (mp is None):
            diffs.append(("ppw blank/not", f, g["name"], y, pp, mp, f"page sud={ps} mine sud={ms}"))
        elif mp is not None:
            n_ppw += 1
            rel = abs(pp - mp) / mp; ppw_maxrel = max(ppw_maxrel, rel)
            if round(pp, 1) != round(mp, 1) or rel > 1e-6:
                diffs.append(("ppw", f, g["name"], y, round(pp, 4), round(mp, 4), ""))
print("workers state-years compared (blank vs not):", n_wb)
print("workers values compared:", n_w, " workers_note compared:", n_note, " ppw compared:", n_ppw, " ppw max rel diff:", ppw_maxrel)
print("my non-blank state-years excl US:", sum(1 for f in geos if f != "US" for y in Y if mine(f, y)[0] is not None))
print("withheld state-years (mine):", len(withheld))
for w in withheld: print("  ", w)
# count of ** cells and missing rows among 51 states
stf = [f for f in geos if f != "US"]
star = r[(r.fips.isin(stf)) & (r.tot_emp.str.strip() == "**")]
print("** cells in 50+DC:", len(star), "years", star.year.min(), star.year.max())
print(star[["year", "fips", "occ"]].to_string())
print("DIFFS:", len(diffs))
for d in diffs: print(d)
pd.DataFrame(diffs, columns=["kind", "fips", "name", "year", "page", "mine", "note"]).to_csv(outf, index=False)
# US series
print("US workers page vs mine:")
for k, y in enumerate(Y): print(y, D["geo"]["US"]["workers"][k], mine("US", y)[0], D["geo"]["US"]["workers_note"][k], mine("US", y)[1])
