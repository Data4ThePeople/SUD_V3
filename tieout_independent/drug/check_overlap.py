# usage: check_overlap.py OUTDIR
import sys, pandas as pd
O=sys.argv[1]
d=pd.concat([pd.read_pickle(O+"/s9919.pkl"),pd.read_pickle(O+"/s2124.pkl")]); d=d[(d.agegrp==0)&(~d.pyearnm.str.contains("updated"))]
d=d[d.stname.isin(set(d.stname)-{"Northeast","Midwest","South","West"})]
sets=[("ABODILL","ABODALC","ABODILAL"),("UDPYILL","ABODALC","UDPYILAL"),("UD5ILANY","UDYR5ALC","UD5IAANY")]
n=0; fails=[]; minpp=(9,None); 
for dr,al,an in sets:
    p=d[d.outcome.isin([dr,al,an])].pivot_table(index=["pyearnm","stname"],columns="outcome",values=["bsae","est_total"])
    p=p.dropna()
    for (w,s),r in p.iterrows():
        n+=1
        gap=(r[("bsae",dr)]+r[("bsae",al)]-r[("bsae",an)])*100
        if not (gap>0 and r[("est_total",dr)]+r[("est_total",al)]>r[("est_total",an)] and r[("bsae",dr)]<=r[("bsae",an)] and r[("bsae",al)]<=r[("bsae",an)]):
            fails.append((w,s,r[("bsae",dr)],r[("bsae",al)],r[("bsae",an)]))
        if gap<minpp[0]: minpp=(gap,w,s)
    print(dr,al,an,"windows:",sorted(p.index.get_level_values(0).unique()))
print("state-windows tested",n,"failures",len(fails),"smallest overlap (pct points):",minpp)
for f in fails: print(f)
