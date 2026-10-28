import openpyxl, json, sys, re
T="/Users/ericpachman/PycharmProjects/SUD_V3/tieout_independent/"
D=json.load(open(T+"page_D.json")); Y=D["years"]
n2f={g['name']:f for f,g in D['geo'].items()}; n2f['Total U.S.']='US'
def find(fn, pat):
    wb=openpyxl.load_workbook(T+"raw/nsduh/"+fn,read_only=True)
    for sn in wb.sheetnames:
        ws=wb[sn]; rows=list(ws.iter_rows(values_only=True))
        title=str(rows[0][0]) if rows and rows[0] else ""
        if re.search(pat,title): return title,rows
    return None,None
jobs=[("2019NSDUHsaeExcelTabs.xlsx","2019NSDUHsaeTotals.xlsx",r"^Table \d+\. Substance Use Disorder in the Past Year",2019,100),
      ("2022-nsduh-sae-tables-percent.xlsx","2022-nsduh-sae-totals-tables.xlsx",r"^Table \d+\. Substance Use Disorder in the Past Year",2022,100),
      ("NSDUHsaeExcelTabs2013.xlsx","NSDUHsaeTotals2013.xlsx",r"Illicit Drugs or Alcohol",2013,None)]
tot=0;bad=[]
for pf,cf,pat,y,mult in jobs:
    i=Y.index(y)
    for fn,keys,scale in [(pf,["sud_pct","sud_lo","sud_hi"],"pct"),(cf,["sud_count","sud_count_lo","sud_count_hi"],"cnt")]:
        title,rows=find(fn,pat); print(fn,"->",title[:150])
        for r in rows:
            if not r or len(r)<5: continue
            nm=r[1] if isinstance(r[0],(int,float)) else r[0]
            f=n2f.get(str(nm).strip() if nm else None)
            if not f: continue
            vals=r[2:5] if isinstance(r[0],(int,float)) else r[1:4]
            for k,v in zip(keys,vals):
                if isinstance(v,str): v=float(v.replace(",","").replace("%",""))
                if scale=="pct": v=v*100 if v<1 else v; tol=0.006 if fn.endswith("2013.xlsx") else 0.0001
                else: v=v*1000; tol=0.5
                tot+=1
                if abs(D["geo"][f][k][i]-v)>tol: bad.append((fn,k,nm,y,D["geo"][f][k][i],v))
print("compared",tot,"bad",len(bad)); [print(b) for b in bad[:30]]
