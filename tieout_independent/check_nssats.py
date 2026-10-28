import pandas as pd, glob, json
T="/Users/ericpachman/PycharmProjects/SUD_V3/tieout_independent/"
R=T+"raw/nssats/"
D=json.load(open(T+"page_D.json")); Y=D["years"]
ab2f={g["abbr"]:f for f,g in D["geo"].items() if f!="US"}
files={2002:"N-SSATS-2002*/**/*.dta",2003:"N-SSATS-2003*/**/*.dta",2004:"N-SSATS-2004*/**/*.dta",2012:"N-SSATS-2012*/**/*.dta",
       2013:"N-SSATS-2013*/**/*.dta",2019:"N-SSATS-2019*/**/*.dta",2020:"N-SSATS-2020*/**/*.csv",2021:"N-SUMHSS-2021*/**/*.csv",
       2022:"N-SUMHSS-2022*/**/*.csv",2023:"N-SUMHSS-2023*/**/*.csv",2024:"N-SUMHSS-2024*/**/*.csv"}
diffs=[];n=0;summary={}
for y,pat in files.items():
    p=glob.glob(R+"x_"+pat,recursive=True)[0]
    df=pd.read_stata(p,convert_categoricals=False) if p.endswith(".dta") else pd.read_csv(p,low_memory=False,dtype=str)
    df.columns=[c.upper() for c in df.columns]
    ct=df["CTYPE1"].astype(str).str.replace(r"\.0$","",regex=True)
    keep=ct=="1"
    if y==2021: keep&=df["TSU21_SU"].astype(str)=="1"
    if y>=2022: keep&=df["TSU_SU"].astype(str)=="1"
    if "LOCATIONSTATE" in df: st=df["LOCATIONSTATE"].map(ab2f)
    elif "STATE" in df: st=df["STATE"].map(ab2f)
    else: st=df["STFIPS"].astype(int).map(lambda x:f"{x:02d}")
    cnt=st[keep].value_counts()
    i=Y.index(y); tot=0
    for f,g in D["geo"].items():
        if f=="US": continue
        mine=float(cnt.get(f,0)); tot+=mine; n+=1
        if g["estabs"][i]!=mine: diffs.append(("estabs",g["name"],y,g["estabs"][i],mine))
    summary[y]=(int(tot),int(keep.sum()),D["geo"]["US"]["estabs"][i])
print("compared",n,"diffs",len(diffs))
for d in diffs: print(d)
print("year: my 51-state total, whole-file total incl territories, page US estabs"); [print(k,v) for k,v in summary.items()]
print("page 2001 estabs non-null:",[g["name"] for g in D["geo"].values() if g["estabs"][0] is not None])
# per100k / gap recompute
mism=0;m=0
for f,g in D["geo"].items():
    for i,y in enumerate(Y):
        e,pop=g["estabs"][i],g["population"][i]
        v=None if e is None or pop is None else e/pop*1e5
        m+=1
        if (v is None)!=(g["estabs_per100k"][i] is None) or (v is not None and abs(v-g["estabs_per100k"][i])>0.0001): mism+=1
        s,w=g["sud_count"][i],g["workers"][i]
        gv=None if s is None or w is None else s/w
        if (gv is None)!=(g["gap"][i] is None) or (gv is not None and abs(gv-g["gap"][i])>0.001): mism+=1;print("gap",g["name"],y,g["gap"][i],gv)
print("derived compared",m*2,"mismatch",mism)
