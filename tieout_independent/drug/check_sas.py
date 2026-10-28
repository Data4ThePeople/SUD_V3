# usage: check_sas.py OUTDIR  (uses s9919.pkl, s2124.pkl, page_D.json in OUTDIR)
import sys, json, pandas as pd
O=sys.argv[1]
D=json.load(open(O+"/page_D.json")); Y=D["years"]; G=D["geo"]
d=pd.concat([pd.read_pickle(O+"/s9919.pkl"),pd.read_pickle(O+"/s2124.pkl")])
d=d[d.agegrp==0]
MEAS={"ABODILL":(2000,2014),"UDPYILL":(2015,2019),"UD5ILANY":(2021,2024)}
n2f={g["name"]:f for f,g in G.items()}; n2f["National"]="US"
def pick(variant):
    out={}
    for oc,(lo,hi) in MEAS.items():
        s=d[d.outcome==oc]
        for _,r in s.iterrows():
            w=r.pyearnm
            if "(" in w:
                if variant not in w: continue
                w=w.split(" ")[0]
            if len(w)!=9: continue
            if w=="2010-2011" and "(" not in r.pyearnm: pass
            end=int(w[5:])
            f=n2f.get(r.stname)
            if f is None: continue
            out[(f,end)]=r
    return out
mine=pick("published")
print("unmatched stnames:",set(d[d.outcome=="ABODILL"].stname)-set(n2f))
fields=[("sud_drug_pct","bsae",100),("sud_drug_lo","low_sae",100),("sud_drug_hi","up_sae",100),
        ("sud_drug_count","est_total",1000),("sud_drug_count_lo","low_total",1000),("sud_drug_count_hi","up_total",1000)]
n=0; diffs=[]; maxpct=0
for f,g in G.items():
    for i,y in enumerate(Y):
        r=mine.get((f,y))
        for k,c,m in fields:
            p=g[k][i]; n+=1
            if r is None:
                if p is not None: diffs.append((g["name"],y,k,p,None))
                continue
            v=float(r[c])*m
            if k.endswith("count") or "count" in k:
                if p is None or p!=round(v): diffs.append((g["name"],y,k,p,v))
            else:
                if p is None or abs(p-round(v,4))>1e-9:
                    diffs.append((g["name"],y,k,p,v))
                else: maxpct=max(maxpct,abs(p-v))
print("cells compared",n,"diffs",len(diffs),"max abs pct gap",maxpct)
for x in diffs[:60]: print(x)
blank=[y for y in Y if all(G[f]["sud_drug_pct"][Y.index(y)] is None for f in G)]
print("years blank for every geo:",blank)
filled=sorted({y for (f,y) in mine}); print("years with SAS windows:",filled)
# published vs updated 2010-2011
upd=pick("updated"); i=Y.index(2011); same_pub=same_upd=0
for f,g in G.items():
    p=g["sud_drug_pct"][i]
    same_pub+= abs(p-float(mine[(f,2011)].bsae)*100)<6e-5
    same_upd+= abs(p-float(upd[(f,2011)].bsae)*100)<6e-5
print("2011 matches published:",same_pub,"updated:",same_upd,"of",len(G))
nd=sum(abs(float(mine[(f,2011)].bsae)-float(upd[(f,2011)].bsae))>1e-9 for f in G); print("geos where published != updated:",nd)
# state sums vs national
for y in filled:
    s=sum(float(mine[(f,y)].est_total) for f in G if f!="US"); nat=float(mine[("US",y)].est_total)
    print("sum check",y,int(s),int(nat),int(s-nat))
