# usage: check_wonder_alcohol.py WONDERDIR OUTDIR
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
for fn,lo,hi in [("ucd_1999_2020_state_year_alcohol.csv",2001,2017),("ucd_2018_2024_state_year_alcohol.csv",2018,2024)]:
    for r in rows(fn):
        y=int(r["Year"])
        if lo<=y<=hi: src[(r["State Code"],y)]=r
nat={}
for fn,lo,hi in [("ucd_1999_2020_year.csv",2001,2017),("ucd_2018_2024_year.csv",2018,2024)]:
    for r in rows(fn):
        y=int(r["Year"])
        if lo<=y<=hi: nat[y]=float(r["Population"])
# overlap 2018-2020 between databases
a={(r["State Code"],int(r["Year"])):r for r in rows("ucd_1999_2020_state_year_alcohol.csv")}
ov=[(k,a[k]["Deaths"],src[k]["Deaths"],a[k]["Population"],src[k]["Population"]) for k in src if 2018<=k[1]<=2020 and (a[k]["Deaths"]!=src[k]["Deaths"] or a[k]["Population"]!=src[k]["Population"])]
print("2018-2020 db overlap mismatches:",len(ov),ov[:5])
n=0; diffs=[]; unrel=[]; eq20=[]
for f,g in G.items():
    if f=="US": continue
    for i,y in enumerate(Y):
        r=src[(f,y)]; dth=float(r["Deaths"]); cr=r["Crude Rate"]
        n+=1
        if g["deaths_alcohol"][i]!=dth: diffs.append((g["name"],y,"deaths_alcohol",g["deaths_alcohol"][i],dth))
        n+=1
        if cr=="Unreliable":
            unrel.append((g["name"],y,int(dth),g["death_rate_alcohol"][i]))
            if g["death_rate_alcohol"][i] is not None: diffs.append((g["name"],y,"death_rate_alcohol",g["death_rate_alcohol"][i],"blank (Unreliable)"))
        else:
            p=g["death_rate_alcohol"][i]
            if p is None or abs(p-float(cr))>1e-9: diffs.append((g["name"],y,"death_rate_alcohol",p,float(cr)))
        if dth<=20 and cr!="Unreliable": eq20.append((g["name"],y,dth,cr))
        if dth==20: eq20.append(("exactly20",g["name"],y,cr))
us=G["US"]
for i,y in enumerate(Y):
    s=sum(float(src[(f,y)]["Deaths"]) for f in G if f!="US"); ps=sum(float(src[(f,y)]["Population"]) for f in G if f!="US")
    rate=round(s/nat[y]*1e5,4); n+=2
    if us["deaths_alcohol"][i]!=s: diffs.append(("US",y,"deaths_alcohol",us["deaths_alcohol"][i],s))
    if us["death_rate_alcohol"][i] is None or abs(us["death_rate_alcohol"][i]-rate)>1e-9: diffs.append(("US",y,"death_rate_alcohol",us["death_rate_alcohol"][i],rate))
    if ps!=nat[y]: print("state pop sum != national pop",y,ps,nat[y])
print("cells compared",n,"diffs",len(diffs)); [print(d) for d in diffs]
print("Unreliable rates in source:",unrel)
print("<=20 deaths without Unreliable flag, or exactly 20:",eq20)
mins=sorted((float(src[k]["Deaths"]),k) for k in src)[:10]; print("smallest alcohol death counts:",mins)
print("unflagged min deaths:",min(float(r["Deaths"]) for r in src.values() if r["Crude Rate"]!="Unreliable"))
# combined = drug + alcohol per state-year, and 2018-2024 'flag' column check
comb={}; drug={}
for fn,lo,hi,dd in [("ucd_1999_2020_state_year.csv",2001,2017,comb),("ucd_2018_2024_state_year.csv",2018,2024,comb),("ucd_1999_2020_state_year_drug.csv",2001,2017,drug),("ucd_2018_2024_state_year_drug.csv",2018,2024,drug)]:
    for r in rows(fn):
        y=int(r["Year"])
        if lo<=y<=hi: dd[(r["State Code"],y)]=float(r["Deaths"])
bad=[k for k in src if comb[k]!=drug[k]+float(src[k]["Deaths"])]; print("combined != drug+alcohol:",len(bad),"of",len(src))
print("suppressed alcohol cells:",[k for k,r in src.items() if not r["Deaths"].isdigit()])
print("2018-2024 columns:",list(rows("ucd_2018_2024_state_year_alcohol.csv")[0].keys()))
print("non-numeric rates:",[(k,r["Crude Rate"]) for k,r in src.items() if not r["Crude Rate"].replace(".","").isdigit()])
