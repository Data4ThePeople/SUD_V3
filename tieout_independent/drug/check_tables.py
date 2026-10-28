# usage: check_tables.py RAWDIR OUTDIR
import sys, json, openpyxl
R,O=sys.argv[1],sys.argv[2]
D=json.load(open(O+"/page_D.json")); Y=D["years"]; G=D["geo"]
n2f={g["name"]:f for f,g in G.items()}; n2f["Total U.S."]="US"
J=[("NSDUHsaeExcelTab18-2011.xlsx","Table 18",2011,"pct"),
   ("NSDUHsaeExcelTab18-2012.xlsx","Table 18",2012,"pct"),("NSDUHsaeTotals2012.xlsx","Table 18",2012,"cnt"),
   ("NSDUHsaeExcelTabs2013.xlsx","Table 18",2013,"pct"),("NSDUHsaeTotals2013.xlsx","Table 18",2013,"cnt"),
   ("NSDUHsaeExcelTabs2014.xlsx","Table 18",2014,"pct"),("NSDUHsaeTotals2014.xlsx","Table 18",2014,"cnt"),
   ("NSDUHsaeExcelTabs2016.xlsx","Table 19",2016,"pct"),("NSDUHsaeTotals2016.xlsx","Table 19",2016,"cnt"),
   ("NSDUHsaeExcelTabs2017.xlsx","Table 20",2017,"pct"),("NSDUHsaeTotals2017.xlsx","Table 20",2017,"cnt"),
   ("NSDUHsaeExcelTabs2018.xlsx","Table 20",2018,"pct"),("NSDUHsaeTotals2018.xlsx","Table 20",2018,"cnt"),
   ("2019NSDUHsaeExcelTabs.xlsx","Table 20",2019,"pct"),("2019NSDUHsaeTotals.xlsx","Table 20",2019,"cnt"),
   ("2022-nsduh-sae-tables-percent.xlsx","Table 25",2022,"pct"),("2022-nsduh-sae-totals-tables.xlsx","Table 25",2022,"cnt"),
   ("2023-nsduh-sae-tables-percent.xlsx","Table 27",2023,"pct"),("2023-nsduh-sae-totals-tables.xlsx","Table 27",2023,"cnt"),
   ("2024-nsduh-sae-tables-percent.xlsx","Table 27",2024,"pct"),("2024-nsduh-sae-totals-tables.xlsx","Table 27",2024,"cnt")]
tot=0; bad=[]
for fn,sn,y,kind in J:
    ws=openpyxl.load_workbook(R+"/"+fn,read_only=True)[sn]; rows=list(ws.iter_rows(values_only=True))
    title=rows[0][0]; i=Y.index(y); seen=set(); maxgap=0
    keys=["sud_drug_pct","sud_drug_lo","sud_drug_hi"] if kind=="pct" else ["sud_drug_count","sud_drug_count_lo","sud_drug_count_hi"]
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
                if gap>0.00005+1e-9: bad.append((fn,G[f]["name"],y,k,p,v))
            else:
                v=v*1000
                if p!=v: bad.append((fn,G[f]["name"],y,k,p,v))
    print(f"{fn} [{sn}] -> {y}: {len(seen)} geos, max pct gap {maxgap:.2e} | {title[:90]}")
print("cells compared",tot,"diffs",len(bad))
for b in bad[:50]: print(b)
