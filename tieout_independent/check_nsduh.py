import pandas as pd, json
T="/Users/ericpachman/PycharmProjects/SUD_V3/tieout_independent/"
D=json.load(open(T+"page_D.json")); Y=D["years"]
a=pd.read_pickle(T+"out/sae9919.pkl"); b=pd.read_pickle(T+"out/sae2124.pkl")
sel=pd.concat([a[(a.outcome.isin(["ABODILAL","UDPYILAL"]))&(a.agegrp==0)], b[(b.outcome=="UD5IAANY")&(b.agegrp==0)]])
sel=sel[~sel.pyearnm.str.contains("updated")]
print(sorted(sel.pyearnm.unique()))
sel["end"]=sel.pyearnm.str.extract(r"-(\d{4})")[0].astype(float)
sel=sel[sel.end.notna()]
print(sel.groupby('pyearnm').size())
name2f={g["name"]:f for f,g in D["geo"].items()}
name2f["National"]="US"; name2f["Total U.S."]="US"
unk=set(sel.stname)-set(name2f); print("unmatched names",unk)
diffs=[];n=0
have=set()
for _,r in sel.iterrows():
    f=name2f.get(r.stname)
    if f is None: continue
    y=int(r.end); i=Y.index(y) if y in Y else None
    if i is None: print("window outside page years",r.pyearnm); continue
    have.add((f,y)); g=D["geo"][f]
    for k,v,tol in [("sud_pct",r.BSAE*100,0.00051),("sud_lo",r.low_sae*100,0.00051),("sud_hi",r.up_sae*100,0.00051),
                    ("sud_count",r.est_total*1000,0.5),("sud_count_lo",r.low_total*1000,0.5),("sud_count_hi",r.up_total*1000,0.5)]:
        n+=1; p=g[k][i]
        if p is None or abs(p-v)>tol: diffs.append((k,g["name"],y,r.pyearnm,p,round(v,5)))
    dsm="5" if r.outcome=="UD5IAANY" else "IV"
    if g["sud_dsm"][i]!=dsm: diffs.append(("dsm",g["name"],y,g["sud_dsm"][i],dsm))
# page values where no window
for f,g in D["geo"].items():
    for i,y in enumerate(Y):
        if (f,y) not in have:
            vals=[g[k][i] for k in ["sud_pct","sud_lo","sud_hi","sud_count","sud_count_lo","sud_count_hi","sud_dsm"]]
            if any(v is not None for v in vals): diffs.append(("page has value w/o window",g["name"],y,vals))
blank=sorted({y for f,g in D["geo"].items() for i,y in enumerate(Y) if g["sud_pct"][i] is None})
print("page blank years",blank)
print("compared",n,"diffs",len(diffs))
for d in diffs[:60]: print(d)
# national: is it design-based? compare national rows exist
print("---- non-2010 or >0.005 diffs")
for d in diffs:
    if d[0] in("sud_pct","sud_lo","sud_hi") and d[2]==2010 and abs(d[4]-d[5])<=0.0051: continue
    print(d)
