# usage: check_html.py RAWDIR OUTDIR
import sys, json, re, html
R,O=sys.argv[1],sys.argv[2]
D=json.load(open(O+"/page_D.json")); Y=D["years"]; G=D["geo"]
n2f={g["name"]:f for f,g in G.items()}; n2f["Total U.S."]="US"
def table(fn,cap):
    h=open(R+"/"+fn,encoding="latin-1").read()
    for t in re.findall(r"<table.*?</table>",h,flags=re.S):
        c=re.search(r"<caption>(.*?)</caption>",t,flags=re.S)
        if c and re.search(cap,re.sub("<[^>]+>","",c.group(1))):
            rows=[]
            for tr in re.findall(r"<tr.*?</tr>",t,flags=re.S):
                cells=[html.unescape(re.sub(r"<[^>]+>","",x)).strip() for x in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>",tr,flags=re.S)]
                rows.append(cells)
            return re.sub("<[^>]+>","",c.group(1)),rows
    return None,None
J=[("NSDUHsaeMainReport2010.htm",r"^Table B\.18 .*Illicit Drug Dependence or Abuse",2010,"pct"),
   ("NSDUHsaeCountTabs2010.htm",r"^Table 18\. .*Illicit Drug Dependence or Abuse",2010,"cnt"),
   ("NSDUHsaeCountTabs2011.htm",r"^Table 18 .*Illicit Drug Dependence or Abuse",2011,"cnt")]
tot=0;bad=[]
for fn,cap,y,kind in J:
    title,rows=table(fn,cap); i=Y.index(y); seen=set()
    keys=["sud_drug_pct","sud_drug_lo","sud_drug_hi"] if kind=="pct" else ["sud_drug_count","sud_drug_count_lo","sud_drug_count_hi"]
    print(fn,"|",html.unescape(title)[:120]); print("  sample rows:",[r for r in rows if r and r[0] in("Total U.S.","Alabama")][:2])
    for r in rows:
        if not r or r[0] not in n2f: continue
        f=n2f[r[0]]; seen.add(f)
        nums=[float(x.replace(",","")) for x in re.findall(r"[0-9][0-9,]*\.?[0-9]*"," ".join(r[1:3]))][:3] if "(" in r[2] else [float(x.replace(",","")) for x in r[1:4]]
        for k,v in zip(keys,nums):
            p=G[f][k][i]; tot+=1
            if kind=="pct":
                if abs(p-v)>0.005+1e-9: bad.append((fn,G[f]["name"],y,k,p,v))
            else:
                if p!=v*1000: bad.append((fn,G[f]["name"],y,k,p,v*1000))
    print("  geos",len(seen))
print("cells compared",tot,"diffs",len(bad))
for b in bad: print(b)
