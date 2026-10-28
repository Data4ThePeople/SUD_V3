# usage: check_sas.py dist/index.html DRUGOUT OUTDIR
import sys, json, pandas as pd
h=open(sys.argv[1],encoding="utf-8").read()
i=h.index("const D = ")+len("const D = ")
D,_=json.JSONDecoder().raw_decode(h[i:])
json.dump(D,open(sys.argv[3]+"/page_D.json","w"))
Y=D["years"]; G=D["geo"]; print(Y[0],Y[-1],len(G))
d=pd.concat([pd.read_pickle(sys.argv[2]+"/s9919.pkl"),pd.read_pickle(sys.argv[2]+"/s2124.pkl")])
d=d[d.agegrp==0]
n2f={g["name"]:f for f,g in G.items()}; n2f["National"]="US"
def pick(variant):
    out={}
    for oc in ["ABODALC","UDYR5ALC"]:
        for _,r in d[d.outcome==oc].iterrows():
            w=r.pyearnm
            if "(" in w:
                if variant not in w: continue
                w=w.split(" ")[0]
            f=n2f.get(r.stname)
            if f is None: continue
            k=(f,int(w[5:]))
            assert k not in out; out[k]=r
    return out
mine=pick("published")
print("unmatched names:",set(d[d.outcome=="ABODALC"].stname)-set(n2f))
print("windows:",sorted({y for _,y in mine}), len({y for _,y in mine}))
fields=[("sud_alcohol_pct","bsae",100),("sud_alcohol_lo","low_sae",100),("sud_alcohol_hi","up_sae",100),
        ("sud_alcohol_count","est_total",1000),("sud_alcohol_count_lo","low_total",1000),("sud_alcohol_count_hi","up_total",1000)]
n=0; nn=0; diffs=[]; maxgap=0
for f,g in G.items():
    for i,y in enumerate(Y):
        r=mine.get((f,y))
        for k,c,m in fields:
            p=g[k][i]; n+=1
            if r is None:
                if p is not None: diffs.append((g["name"],y,k,p,None))
                continue
            nn+=1
            v=float(r[c])*m
            if "count" in k:
                if p is None or p!=round(v): diffs.append((g["name"],y,k,p,v))
            else:
                if p is None or abs(p-v)>5e-5: diffs.append((g["name"],y,k,p,v))
                else: maxgap=max(maxgap,abs(p-v))
print("cells",n,"non-blank compared",nn,"diffs",len(diffs),"max pct gap",maxgap)
for x in diffs[:50]: print(x)
print("page decimals sample:",G["06"]["sud_alcohol_pct"][:5], G["06"]["sud_alcohol_count"][:5])
blank=[y for y in Y if all(G[f]["sud_alcohol_pct"][Y.index(y)] is None for f in G)]
print("years blank everywhere:",blank)
# 2010-2011 published vs updated
upd=pick("updated"); i=Y.index(2011); a=b=0
for f,g in G.items():
    p=g["sud_alcohol_pct"][i]
    a+=abs(p-float(mine[(f,2011)].bsae)*100)<5e-5; b+=abs(p-float(upd[(f,2011)].bsae)*100)<5e-5
print("2011 matches published",a,"updated",b,"of",len(G))
for y in sorted({y for _,y in mine}):
    s=sum(float(mine[(f,y)].est_total) for f in G if f!="US"); nat=float(mine[("US",y)].est_total)
    print("sum",y,int(s),int(nat),int(s-nat))
# outname/measure labels
for oc in ["ABODALC","UDYR5ALC"]: print(oc, d[d.outcome==oc].outname.unique())
