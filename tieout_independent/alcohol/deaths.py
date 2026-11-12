"""Independent death-rate series. Weights: NCHS Healthy People 2010 Statistical Notes No. 20 (Klein & Schoenborn, 2001),
Table 2 Distribution #1, https://www.cdc.gov/nchs/data/statnt/statnt20.pdf"""
import csv, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
W = {"< 1 year":0.013818,"1-4 years":0.055317,"5-14 years":0.145565,"15-24 years":0.138646,"25-34 years":0.135573,
     "35-44 years":0.162613,"45-54 years":0.134834,"55-64 years":0.087247,"65-74 years":0.066037,"75-84 years":0.044842,"85+ years":0.015508}
assert abs(sum(W.values())-1) < 1e-5
num = lambda s: float(s.replace(",", ""))

def aar(rows):  # rows: {age: (deaths, pop)}
    return sum(W[a] * d / p * 1e5 for a, (d, p) in rows.items() if a in W)

out = {}
# D76 API: year table
x = (HERE/"raw/d76_year.xml").read_text()
for y, d, p, cr, aa in re.findall(r'<r><c l="(\d{4})"/><c v="([\d,]+)"/><c v="([\d,]+)"/><c v="([\d.]+)"/><c v="([\d.]+)"/></r>', x):
    out[int(y)] = dict(src="D76 API", deaths=int(num(d)), pop=int(num(p)), crude_pub=float(cr), aar_pub=float(aa))
# D76 API: year x age, recompute AAR (missing under-15 rows = suppressed/zero, treated as 0)
x = (HERE/"raw/d76_year_age.xml").read_text()
tab = x[x.find("<data-table"):x.find("</data-table>")]
yr=None; ages={}
for row in re.findall(r"<r>(.*?)</r>", tab):
    cells = re.findall(r'<c ([^/]*)/>', row)
    m = re.match(r'l="(\d{4})"', cells[0])
    if m: yr=int(m.group(1)); cells=cells[1:]
    lab = re.match(r'l="([^"]*)"', cells[0])
    if not lab or yr is None: continue
    vals = [re.search(r'v="([^"]*)"', c) for c in cells[1:3]]
    if not all(vals) or lab.group(1) not in W: continue
    ages.setdefault(yr, {})[lab.group(1)] = (num(vals[0].group(1)), num(vals[1].group(1)))
for y, r in ages.items():
    out[y]["aar_mine_d76age"] = aar(r)
# D158 export (2018-2024)
d158 = {}
with open(HERE.parent.parent/"data/raw/wonder/mcd_2018_2024_year_age_alcohol.csv") as f:
    for r in csv.DictReader(f):
        if not r["Year"] or r["Notes"] == "Total": continue
        if r["Notes"] and not r["Year"]: continue
        a=r["Ten-Year Age Groups"]; d=r["Deaths"]; p=r["Population"]
        if a not in W: continue
        d158.setdefault(int(r["Year"]), {})[a] = (0.0 if d=="Suppressed" else num(d), num(p))
    f.seek(0)
    tot = {int(r["Year"]):(int(r["Deaths"]),int(r["Population"])) for r in csv.DictReader(f) if r["Notes"]=="Total" and r["Year"]}
for y, r in d158.items():
    o = out.setdefault(y, dict(src="D158 export"))
    o["d158_deaths"], o["d158_pop"] = tot[y]
    o["d158_crude_mine"] = tot[y][0]/tot[y][1]*1e5
    o["d158_aar_mine"] = aar(r)
    o["d158_aar_if_supp_9"] = aar({a:(d if d>0 or a not in ("5-14 years",) else 9, p) for a,(d,p) in r.items()})
NCHS = {2021:14.4, 2022:13.5}  # NVSR 73-8 Table 6; NVSR 74-4 text
NCHS_T6 = {1999:7.1,2000:7.0,2001:7.0,2002:6.9,2003:7.0,2004:7.0,2005:7.0,2006:7.0,2007:7.2,2008:7.4,2009:7.4,2010:7.6,2011:7.7,2012:8.0,
           2013:8.2,2014:8.5,2015:9.1,2016:9.5,2017:9.6,2018:9.9,2019:10.4,2020:13.1}
NCHS.update(NCHS_T6)
with open(HERE/"deaths_independent.csv","w",newline="") as f:
    cols=["year","crude_plotted","aar_plotted","nchs_published_aar","d76_deaths","d76_crude","d76_aar","aar_mine_d76age","d158_deaths","d158_crude_mine","d158_aar_mine","d158_aar_if_supp_9"]
    w=csv.writer(f); w.writerow(cols)
    for y in sorted(out):
        o=out[y]
        crude = o.get("crude_pub") if y<=2020 else o["d158_crude_mine"]
        aa = o.get("aar_pub") if y<=2020 else o["d158_aar_mine"]
        row=[y, round(crude,2), round(aa,2), NCHS.get(y,""), o.get("deaths",""), o.get("crude_pub",""), o.get("aar_pub",""),
             round(o["aar_mine_d76age"],3) if "aar_mine_d76age" in o else "", o.get("d158_deaths",""),
             round(o["d158_crude_mine"],3) if "d158_crude_mine" in o else "", round(o["d158_aar_mine"],3) if "d158_aar_mine" in o else "",
             round(o["d158_aar_if_supp_9"],3) if "d158_aar_if_supp_9" in o else ""]
        w.writerow(row); print(*row, sep="\t")
# chart-2 death averages
a = lambda ys: sum(out[y]["aar_pub"] for y in ys)/2
early, late = a([2002,2003]), a([2018,2019])
print("AAR avg 2002-03 %.3f, 2018-19 %.3f, change %.2f%%" % (early, late, (late/early-1)*100))
r1 = (NCHS[2018]+NCHS[2019])/2/((NCHS[2002]+NCHS[2003])/2)-1
print("using 1-decimal published: %.2f%%" % (r1*100))
