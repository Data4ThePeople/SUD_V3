import pandas as pd, json, io, sys
W="/Users/ericpachman/PycharmProjects/SUD_V3/data/raw/wonder/"
T="/Users/ericpachman/PycharmProjects/SUD_V3/tieout_independent/"
D=json.load(open(T+"page_D.json")); Y=D["years"]
def load(f, state=True):
    lines=open(W+f).read().split("\n")
    body=[]
    for l in lines:
        if l.startswith('"---'): break
        body.append(l)
    df=pd.read_csv(io.StringIO("\n".join(body)),dtype=str)
    df=df[df["Notes"].isna() | (df["Notes"]!="Total")] if state else df
    return df
def num(x):
    try: return float(x)
    except: return None
rows=[]; ncomp=0; diffs=[]
src={}
for kind,suf in [("all",""),("drug","_drug"),("alc","_alcohol")]:
    a=load(f"ucd_1999_2020_state_year{suf}.csv"); b=load(f"ucd_2018_2024_state_year{suf}.csv")
    for df,lo,hi in [(a,2001,2017),(b,2018,2024)]:
        for _,r in df.iterrows():
            if pd.isna(r.get("State Code")) or pd.isna(r.get("Year")): continue
            y=int(r["Year"]);
            if lo<=y<=hi: src[(kind,r["State Code"],y)]=r
    # overlap check
    for _,r in a.iterrows():
        if pd.isna(r.get("Year")) or pd.isna(r.get("State Code")): continue
        y=int(r["Year"])
        if 2018<=y<=2020:
            rb=b[(b["State Code"]==r["State Code"])&(b["Year"]==r["Year"])].iloc[0]
            if r["Deaths"]!=rb["Deaths"] or r["Population"]!=rb["Population"]:
                diffs.append(("overlap",kind,r["State"],y,r["Deaths"],rb["Deaths"],r["Population"],rb["Population"]))
# national
nat={}
for f,lo,hi in [("ucd_1999_2020_year.csv",2001,2017),("ucd_2018_2024_year.csv",2018,2024)]:
    d=load(f,False)
    for _,r in d.iterrows():
        if pd.isna(r.get("Year")): continue
        try: y=int(r["Year"])
        except: continue
        if lo<=y<=hi: nat[y]=r
def cmp(metric,geo,y,page,mine,tol=0):
    global ncomp
    ncomp+=1
    if page is None and mine is None: return
    if page is None or mine is None or abs(page-mine)>tol:
        diffs.append((metric,geo,y,page,mine))
for f,g in D["geo"].items():
    for i,y in enumerate(Y):
        if f=="US":
            r=nat[y]; ra=None
        else:
            r=src[("all",f,y)]
        cmp("deaths",g["name"],y,g["deaths"][i],num(r["Deaths"]))
        cmp("population",g["name"],y,g["population"][i],num(r["Population"]))
        cmp("death_rate",g["name"],y,g["death_rate"][i],num(r["Crude Rate"]),0.051)
        cmp("death_rate_lo",g["name"],y,g["death_rate_lo"][i],num(r["Crude Rate Lower 95% Confidence Interval"]),0.051)
        cmp("death_rate_hi",g["name"],y,g["death_rate_hi"][i],num(r["Crude Rate Upper 95% Confidence Interval"]),0.051)
        if f!="US":
            rd=src[("drug",f,y)]; ral=src[("alc",f,y)]
            cmp("deaths_drug",g["name"],y,g["deaths_drug"][i],num(rd["Deaths"]))
            cmp("deaths_alcohol",g["name"],y,g["deaths_alcohol"][i],num(ral["Deaths"]))
            cmp("death_rate_drug",g["name"],y,g["death_rate_drug"][i],num(rd["Crude Rate"]),0.051)
            cmp("death_rate_alcohol",g["name"],y,g["death_rate_alcohol"][i],num(ral["Crude Rate"]),0.051)
            if num(rd["Deaths"]) is None or num(ral["Deaths"]) is None: print("SUPP",f,y,rd["Deaths"],ral["Deaths"])
            if num(rd["Deaths"])+num(ral["Deaths"])!=num(r["Deaths"]): print("SUM MISMATCH",g["name"],y)
            if num(rd["Crude Rate"]) is None: print("unreliable drug rate",g["name"],y,rd["Crude Rate"],"page:",g["death_rate_drug"][i])
            if num(ral["Crude Rate"]) is None: print("unreliable alc rate",g["name"],y,ral["Crude Rate"],"page:",g["death_rate_alcohol"][i])
        else:
            for k in ["deaths_drug","deaths_alcohol","death_rate_drug","death_rate_alcohol"]:
                print("US",k,y,g[k][i]) if y in (2001,2024) else None
# state sum vs national
for y in Y:
    s=sum(num(src[("all",f,y)]["Deaths"]) for f in D["geo"] if f!="US"); p=sum(num(src[("all",f,y)]["Population"]) for f in D["geo"] if f!="US")
    if s!=num(nat[y]["Deaths"]) or p!=num(nat[y]["Population"]): print("state sum != nat",y,s,nat[y]["Deaths"],p,nat[y]["Population"])
print("compared",ncomp); print("diffs",len(diffs))
for d in diffs[:80]: print(d)
