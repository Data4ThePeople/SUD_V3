# usage: peek.py DRUGOUT
import sys, pandas as pd
O=sys.argv[1]
for n in ["s9919","s2124"]:
    d=pd.read_pickle(f"{O}/{n}.pkl")
    print(n, d.columns.tolist())
    a=d[d.outcome.astype(str).str.contains("ALC")]
    print(a.groupby(["outcome","agegrp"]).pyearnm.unique().to_string())
    for c in ["outname","outcome_desc","label"]:
        if c in d: print(a.drop_duplicates("outcome")[["outcome",c]].to_string())
