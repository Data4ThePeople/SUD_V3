# usage: peek2.py DRUGOUT
import sys, pandas as pd
O=sys.argv[1]
d=pd.read_pickle(f"{O}/s9919.pkl")
a=d[(d.outcome=="ABODALC")&(d.agegrp==0)]
print(a.pyearnm.value_counts().sort_index().to_string())
print(a[a.stname=="National"][["pyearnm","bsae","est_total","outname"]].to_string())
print(d[d.pyearnm.astype(str).str.startswith("2014-2015")].outcome.unique())
