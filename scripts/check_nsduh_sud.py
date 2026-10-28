"""Checks on data/clean/nsduh_sud.csv.

1. Every window has 51 states + United States, no blank pct or count.
2. Cross-check each window against SAMHSA's SAE SAS datasets (1999-2019, 2021-2024):
   pct to 2 decimals and counts exactly.
3. Sum of the 51 state counts vs the published national count.

Run with: .venv/bin/python -I scripts/check_nsduh_sud.py
"""
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "nsduh"
c = pd.read_csv(ROOT / "data" / "clean" / "nsduh_sud.csv", dtype={"window": str})

# 1
g = c.groupby("window")
assert (g.size() == 52).all(), g.size()
assert not c[["pct", "pct_lo", "pct_hi", "count_thousands", "count_lo", "count_hi"]].isna().any().any()
print("1. all windows have 52 rows and no blanks:", sorted(c.window.unique()))

# 2
frames = []
for f, outcomes in [("sae_dataset_1999-2019/NSDUH_99_19_state_saes_final.sas7bdat", ["ABODILAL", "UDPYILAL"]),
                    ("sae_dataset_2021-2024/state_saes_final_2124.sas7bdat", ["UD5IAANY"])]:
    d = pd.read_sas(RAW / f, encoding="latin1")
    d.columns = [x.lower() for x in d.columns]
    d = d[d.outcome.isin(outcomes) & (d.agegrp == 0)].copy()
    frames.append(d)
s = pd.concat(frames)
s["window"] = s.pyearnm.str.replace(" (published)", "", regex=False)
s = s[~s.pyearnm.str.contains("updated")]
s["state"] = s.stname.replace({"National": "United States"})
m = c.merge(s[["window", "state", "bsae", "low_sae", "up_sae", "est_total", "low_total", "up_total"]],
            on=["window", "state"], how="left")
assert m.bsae.notna().all(), m[m.bsae.isna()][["window", "state"]]
bad = []
for _, r in m.iterrows():
    for a, b in [("pct", "bsae"), ("pct_lo", "low_sae"), ("pct_hi", "up_sae")]:
        if round(r[a], 2) != round(r[b] * 100, 2) and abs(r[a] - r[b] * 100) > 0.0051:
            bad.append((r.window, r.state, a, r[a], r[b] * 100))
    for a, b in [("count_thousands", "est_total"), ("count_lo", "low_total"), ("count_hi", "up_total")]:
        if r[a] != r[b]:
            bad.append((r.window, r.state, a, r[a], r[b]))
print(f"2. table vs SAS dataset mismatches: {len(bad)}")
for b in bad:
    print("   ", b)

# 3
print("3. sum of 51 state counts vs national count (thousands)")
print(f"   {'window':10} {'sum_states':>10} {'national':>9} {'diff':>5}")
for w, gw in c.groupby("window"):
    st = gw[gw.state != "United States"].count_thousands.sum()
    us = gw[gw.state == "United States"].count_thousands.iloc[0]
    print(f"   {w:10} {st:>10.0f} {us:>9.0f} {st - us:>5.0f}")
