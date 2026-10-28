# usage: check_tables.py RAWDRUG RAWALC OUTDIR
import sys, json, openpyxl
RD,RA,O=sys.argv[1:4]
D=json.load(open(O+"/page_D.json")); Y=D["years"]; G=D["geo"]
n2f={g["name"]:f for f,g in G.items()}; n2f["Total U.S."]="US"; n2f["Total United States"]="US"; n2f["National"]="US"
J=[(RA,"NSDUHsaeExcelTab16-2011.xlsx","Table 16",2011,"pct"),
   (RA,"NSDUHsaeExcelTab16-2012.xlsx","Table 16",2012,"pct"),(RD,"NSDUHsaeTotals2012.xlsx","Table 16",2012,"cnt"),
   (RD,"NSDUHsaeExcelTabs2013.xlsx","Table 16",2013,"pct"),(RD,"NSDUHsaeTotals2013.xlsx","Table 16",2013,"cnt"),
   (RD,"NSDUHsaeExcelTabs2014.xlsx","Table 16",2014,"pct"),(RD,"NSDUHsaeTotals2014.xlsx","Table 16",2014,"cnt"),
   (RA,"NSDUHsaeTotals2015.xlsx","Table 10",2015,"cnt"),
   (RD,"NSDUHsaeExcelTabs2016.xlsx","Table 21",2016,"pct"),(RD,"NSDUHsaeTotals2016.xlsx","Table 21",2016,"cnt"),
   (RD,"NSDUHsaeExcelTabs2017.xlsx","Table 22",2017,"pct"),(RD,"NSDUHsaeTotals2017.xlsx","Table 22",2017,"cnt"),
   (RD,"NSDUHsaeExcelTabs2018.xlsx","Table 22",2018,"pct"),(RD,"NSDUHsaeTotals2018.xlsx","Table 22",2018,"cnt"),
   (RD,"2019NSDUHsaeExcelTabs.xlsx","Table 22",2019,"pct"),(RD,"2019NSDUHsaeTotals.xlsx","Table 22",2019,"cnt"),
   (RD,"2022-nsduh-sae-tables-percent.xlsx","Table 23",2022,"pct"),(RD,"2022-nsduh-sae-totals-tables.xlsx","Table 23",2022,"cnt"),
   (RD,"2023-nsduh-sae-tables-percent.xlsx","Table 25",2023,"pct"),(RD,"2023-nsduh-sae-totals-tables.xlsx","Table 25",2023,"cnt"),
   (RD,"2024-nsduh-sae-tables-percent.xlsx","Table 25",2024,"pct"),(RD,"2024-nsduh-sae-totals-tables.xlsx","Table 25",2024,"cnt")]
tot=0; bad=[]
for R,fn,sn,y,kind in J:
    ws=openpyxl.load_workbook(R+"/"+fn,read_only=True)[sn]; rows=list(ws.iter_rows(values_only=True))
    title=rows[0][0]; hdr=[r for r in rows[:8] if r and r[1] and "State" in str(r[1])]
    i=Y.index(y); seen=set(); maxgap=0
    keys=["sud_alcohol_pct","sud_alcohol_lo","sud_alcohol_hi"] if kind=="pct" else ["sud_alcohol_count","sud_alcohol_count_lo","sud_alcohol_count_hi"]
    for r in rows:
        if not r or r[1] is None: continue
        f=n2f.get(str(r[1]).strip())
        if f is None: continue
        seen.add(f)
        for k,v in zip(keys,r[2:5]):
            if isinstance(v,str): v=float(v.replace(",","").replace("%",""))
            p=G[f][k][i]; tot+=1
            if kind=="pct":
                v=v*100 if v<1 else v
                gap=abs(p-v); maxgap=max(maxgap,gap)
                if gap>0.005: bad.append((fn,G[f]["name"],y,k,p,v))
            else:
                v=v*1000
                if p!=v: bad.append((fn,G[f]["name"],y,k,p,v))
    print(f"{fn} [{sn}] -> {y}: {len(seen)} geos, max pct gap {maxgap:.2e} | {title[:100]} | hdr {hdr[0][1:5] if hdr else '?'}")
print("cells compared",tot,"diffs",len(bad))
for b in bad[:50]: print(b)
