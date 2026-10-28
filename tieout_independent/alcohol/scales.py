# usage: scales.py OUTDIR
import sys, json
D=json.load(open(sys.argv[1]+"/page_D.json")); Y=D["years"]; G=D["geo"]
st=[f for f in G if f!="US"]; print("states",len(st))
def rep(name,key,rng,cond):
    v=[(G[f]["name"],y,G[f][key][i]) for f in st for i,y in enumerate(Y) if cond(y) and G[f][key][i] is not None]
    lo,hi=rng; b=[x for x in v if x[2]<lo]; a=[x for x in v if x[2]>hi]
    vals=sorted(x[2] for x in v)
    print(f"{name}: n={len(v)} below {lo}: {len(b)} ({100*len(b)/len(v):.1f}%), above {hi}: {len(a)} ({100*len(a)/len(v):.1f}%), min {vals[0]:.2f} max {vals[-1]:.2f}, p5 {vals[len(vals)//20]:.2f} p95 {vals[-len(vals)//20]:.2f}")
    if 0<len(a)<=15: print("  above:",a)
    if 0<len(b)<=15: print("  below:",b)
    return v
rep("AUD % 2001-2019 vs 3-11","sud_alcohol_pct",(3,11),lambda y:y<=2019)
rep("AUD % 2022-2024 vs 7-17","sud_alcohol_pct",(7,17),lambda y:y>=2022)
rep("alc death rate vs 0-25","death_rate_alcohol",(0,25),lambda y:True)
for y in [2001,2010,2019,2024]:
    i=Y.index(y); v=sorted(G[f]["death_rate_alcohol"][i] for f in st); print(" death rate",y,"min",v[0],"max",v[-1],"median",v[25])
# overlap claim: drug + alcohol > any SUD
n=0; bad=[]
for f in G:
    for i,y in enumerate(Y):
        a,d,s=G[f]["sud_alcohol_pct"][i],G[f]["sud_drug_pct"][i],G[f]["sud_pct"][i]
        if None in (a,d,s): continue
        n+=1
        if not a+d>s: bad.append((f,y,a,d,s))
        ac,dc,sc=G[f]["sud_alcohol_count"][i],G[f]["sud_drug_count"][i],G[f]["sud_count"][i]
        if not ac+dc>sc: bad.append(("count",f,y,ac,dc,sc))
print("overlap geo-windows",n,"violations",bad)
print("years with alcohol but no any-SUD:",[y for y in Y if G["US"]["sud_alcohol_pct"][Y.index(y)] is not None and G["US"]["sud_pct"][Y.index(y)] is None])
print("US deaths alc",G["US"]["deaths_alcohol"][-1],G["US"]["death_rate_alcohol"][-1])
