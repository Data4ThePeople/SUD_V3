import pandas as pd, json, os
T="/Users/ericpachman/PycharmProjects/SUD_V3/tieout_independent/"
D=json.load(open(T+"page_D.json")); Y=D["years"]
N=["621420","621330","621112"]; OWN=["5","2","3"]
frames=[]
for y in Y:
    for n in N:
        p=T+f"raw/qcew/api_{y}_{n}.csv" if y>=2014 else T+f"raw/qcew/zip_{y}_{n}.csv"
        df=pd.read_csv(p,dtype=str)
        df=df[df.area_fips.str.endswith("000")&df.own_code.isin(OWN+["1"])]
        df["year"]=y; df["naics"]=n; frames.append(df)
q=pd.concat(frames)
q["emp"]=q.annual_avg_emplvl.astype(float)
q["est"]=q.annual_avg_estabs.fillna(q.get("annual_avg_estabs_count")).astype(float)
q["N"]=q.disclosure_code.fillna("")=="N"
q.to_pickle(T+"out/qcew.pkl")
fips={f for f in D["geo"] if f!="US"}
diffs=[];n=0
def comp(k,name,y,page,mine,tol=0):
    global n; n+=1
    if (page is None)!=(mine is None) or (page is not None and abs(page-mine)>tol): diffs.append((k,name,y,page,mine))
for f,g in D["geo"].items():
    area="US000" if f=="US" else f+"000"
    for i,y in enumerate(Y):
        s=q[(q.area_fips==area)&(q.year==y)&(q.own_code.isin(OWN))]
        pub=s[~s.N]; wh=s[s.N]
        tot=pub.emp.sum(); floor=len(wh)>0
        sp=s[s.own_code=="5"]; ptot=sp[~sp.N].emp.sum(); pfloor=bool(sp.N.any())
        comp("workers",g["name"],y,g["workers"][i],tot)
        comp("workers_floor",g["name"],y,g["workers_floor"][i],floor)
        comp("workers_withheld_cells",g["name"],y,g["workers_withheld_cells"][i],float(len(wh)))
        comp("workers_private",g["name"],y,g["workers_private"][i],ptot)
        comp("workers_private_floor",g["name"],y,g["workers_private_floor"][i],pfloor)
        for nn in N:
            comp("workers_"+nn,g["name"],y,g["workers_"+nn][i],pub[pub.naics==nn].emp.sum())
print("compared",n,"diffs",len(diffs))
from collections import Counter
print(Counter((d[0]) for d in diffs))
for d in diffs[:60]: print(d)
