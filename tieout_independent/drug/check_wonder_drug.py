# usage: check_wonder_drug.py WONDERDIR OUTDIR
import sys, io, json, csv
W,O=sys.argv[1],sys.argv[2]
D=json.load(open(O+"/page_D.json")); Y=D["years"]; G=D["geo"]
def rows(fn):
    out=[]
    with open(W+"/"+fn) as fh:
        for r in csv.DictReader(fh):
            if r["Notes"]=="---" or (r.get("Notes") or "").startswith("---"): break
            if r["Notes"]: continue      # skip Total and note rows
            out.append(r)
    return out
src={}
for fn,lo,hi in [("ucd_1999_2020_state_year_drug.csv",2001,2017),("ucd_2018_2024_state_year_drug.csv",2018,2024)]:
    for r in rows(fn):
        y=int(r["Year"])
        if lo<=y<=hi: src[(r["State Code"],y)]=r
nat={}
for fn,lo,hi in [("ucd_1999_2020_year.csv",2001,2017),("ucd_2018_2024_year.csv",2018,2024)]:
    for r in rows(fn):
        y=int(r["Year"])
        if lo<=y<=hi: nat[y]=float(r["Population"])
# overlap 2018-2020 between databases
a={(r["State Code"],int(r["Year"])):r for r in rows("ucd_1999_2020_state_year_drug.csv")}
ov=[(k,a[k]["Deaths"],src[k]["Deaths"],a[k]["Population"],src[k]["Population"]) for k in src if 2018<=k[1]<=2020 and (a[k]["Deaths"]!=src[k]["Deaths"] or a[k]["Population"]!=src[k]["Population"])]
print("2018-2020 db overlap mismatches:",len(ov),ov[:5])
n=0; diffs=[]; unrel=[]; eq20=[]
for f,g in G.items():
    if f=="US": continue
    for i,y in enumerate(Y):
        r=src[(f,y)]; dth=float(r["Deaths"]); cr=r["Crude Rate"]
        n+=1
        if g["deaths_drug"][i]!=dth: diffs.append((g["name"],y,"deaths_drug",g["deaths_drug"][i],dth))
        n+=1
        if cr=="Unreliable":
            unrel.append((g["name"],y,int(dth),g["death_rate_drug"][i]))
            if g["death_rate_drug"][i] is not None: diffs.append((g["name"],y,"death_rate_drug",g["death_rate_drug"][i],"blank (Unreliable)"))
        else:
            p=g["death_rate_drug"][i]
            if p is None or abs(p-float(cr))>1e-9: diffs.append((g["name"],y,"death_rate_drug",p,float(cr)))
        if dth<=20 and cr!="Unreliable": eq20.append((g["name"],y,dth,cr))
        if dth==20: eq20.append(("exactly20",g["name"],y,cr))
us=G["US"]
for i,y in enumerate(Y):
    s=sum(float(src[(f,y)]["Deaths"]) for f in G if f!="US"); ps=sum(float(src[(f,y)]["Population"]) for f in G if f!="US")
    rate=round(s/nat[y]*1e5,4); n+=2
    if us["deaths_drug"][i]!=s: diffs.append(("US",y,"deaths_drug",us["deaths_drug"][i],s))
    if us["death_rate_drug"][i] is None or abs(us["death_rate_drug"][i]-rate)>1e-9: diffs.append(("US",y,"death_rate_drug",us["death_rate_drug"][i],rate))
    if ps!=nat[y]: print("state pop sum != national pop",y,ps,nat[y])
print("cells compared",n,"diffs",len(diffs)); [print(d) for d in diffs]
print("Unreliable rates in source:",unrel)
print("<=20 deaths without Unreliable flag, or exactly 20:",eq20)
mins=sorted((float(src[k]["Deaths"]),k) for k in src)[:10]; print("smallest drug death counts:",mins)
print("unflagged min deaths:",min(float(r["Deaths"]) for r in src.values() if r["Crude Rate"]!="Unreliable"))
