# usage: load_sas.py RAWDIR OUTDIR
import sys, pandas as pd
R,O=sys.argv[1],sys.argv[2]
for f,n in [("NSDUH_99_19_state_saes_final.sas7bdat","s9919"),("state_saes_final_2124.sas7bdat","s2124")]:
    d=pd.read_sas(f"{R}/{f}",encoding="latin-1")
    d.columns=[c.lower() for c in d.columns]
    d.to_pickle(f"{O}/{n}.pkl"); print(n,d.shape); print(d.columns.tolist()); print(d.head(3).T)
    for c in ["outcome","pyearnm","agegrp"]:
        if c in d: print(c, sorted(d[c].astype(str).unique())[:80])
