# usage: check_pdf_htm.py RAWDRUG RAWALC OUTDIR
import sys, json, re, html
from pypdf import PdfReader
RD,RA,O=sys.argv[1:4]
D=json.load(open(O+"/page_D.json")); Y=D["years"]; G=D["geo"]
n2f={g["name"]:f for f,g in G.items()}; n2f["Total U.S."]="US"
names=sorted(n2f,key=len,reverse=True)
def scan(lines,y,keys,mult,tol,label):
    i=Y.index(y); seen=set(); bad=[]; n=0
    for ln in lines:
        ln=ln.strip()
        for nm in names:
            if ln.startswith(nm+" ") or ln.startswith(nm+"\t"):
                f=n2f[nm]
                if f in seen: break
                nums=re.findall(r"\d[\d,]*\.?\d*",ln[len(nm):])
                if len(nums)<3: break
                seen.add(f)
                for k,v in zip(keys,nums[:3]):
                    v=float(v.replace(",",""))*mult; p=G[f][k][i]; n+=1
                    if abs(p-v)>tol: bad.append((label,G[f]["name"],y,k,p,v))
                break
    print(label,y,"geos",len(seen),"cells",n,"diffs",len(bad)); [print(b) for b in bad]
# 2014-2015 percent PDF
r=PdfReader(RA+"/NSDUHsaePercents2015.pdf")
txt=r.pages[19].extract_text()+"\n"+r.pages[20].extract_text()
assert "Table 10 Alcohol Use Disorder" in txt
scan(txt.splitlines(),2015,["sud_alcohol_pct","sud_alcohol_lo","sud_alcohol_hi"],1,0.005,"Percents2015.pdf T10")
# count tabs htm
for fn,y in [("NSDUHsaeCountTabs2010.htm",2010),("NSDUHsaeCountTabs2011.htm",2011)]:
    h=open(RD+"/"+fn,encoding="latin-1").read()
    a=h.index("Alcohol Dependence or Abuse in the Past Year,</em> by Age Group and State: Estimated")
    b=h.index("Table 17",a)
    seg=h[a:b]
    rows=re.findall(r"<tr.*?</tr>",seg,re.S)
    lines=[" ".join(html.unescape(re.sub(r"<[^>]+>"," ",c)).split()) for c in rows]
    print(lines[:3])
    scan(lines,y,["sud_alcohol_count","sud_alcohol_count_lo","sud_alcohol_count_hi"],1000,0,fn)
# 2009-2010 main report Table B.16 percentages
h=open(RD+"/NSDUHsaeMainReport2010.htm",encoding="latin-1").read()
a=[m.start() for m in re.finditer("Table B.16 &ndash; <em>Alcohol Dependence or Abuse",h)][-1]
b=h.index("Table B.17",a); seg=h[a:b]
rows=re.findall(r"<tr.*?</tr>",seg,re.S)
lines=[" ".join(html.unescape(re.sub(r"<[^>]+>"," ",c)).replace("%","").split()) for c in rows]
print(lines[:4])
scan(lines,2010,["sud_alcohol_pct","sud_alcohol_lo","sud_alcohol_hi"],1,0.005,"MainReport2010 B.16")
