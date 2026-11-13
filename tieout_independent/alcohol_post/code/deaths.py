import re, csv, sys
from pathlib import Path
H = Path(__file__).resolve().parent.parent
# 2000 US standard million, SEER code 201 (19 groups) -> CDC 11 groups
std19 = {}
for line in open(H/'raw/seer_stdpop_19ages.txt'):
    line=line.strip()
    if line.startswith('201'):
        std19[int(line[3:6])] = int(line[6:])
agg = {'1':[0],'1-4':[1],'5-14':[2,3],'15-24':[4,5],'25-34':[6,7],'35-44':[8,9],'45-54':[10,11],
       '55-64':[12,13],'65-74':[14,15],'75-84':[16,17],'85+':[18]}
W = {k: sum(std19[i] for i in v) for k,v in agg.items()}
assert sum(W.values())==1_000_000, sum(W.values())
LAB = {'< 1 year':'1','1-4 years':'1-4','5-14 years':'5-14','15-24 years':'15-24','25-34 years':'25-34',
       '35-44 years':'35-44','45-54 years':'45-54','55-64 years':'55-64','65-74 years':'65-74',
       '75-84 years':'75-84','85+ years':'85+'}
num = lambda s: float(s.replace(',',''))
def rows(t):
    return re.findall(r'<r>(.*?)</r>', t[t.find('<data-table'):], re.S)
# published
t = (H/'raw/d76_year_cause_aar.xml').read_text()
pub = {}; yr=None
for r in rows(t):
    cells = re.findall(r'<c ([^/]*)/>', r)
    labs = [re.search(r'l="([^"]*)"',c).group(1) for c in cells if 'l="' in c]
    vals = [re.search(r'v="([^"]*)"',c).group(1) for c in cells if ' v="' in ' '+c]
    if labs and re.fullmatch(r'\d{4}', labs[0]): yr=int(labs[0]); labs=labs[1:]
    if labs and labs[0]=='Alcohol-induced causes':
        pub[yr] = dict(deaths=num(vals[0]), pop=num(vals[1]), crude=num(vals[2]), aar=num(vals[3]))
# by age
t = (H/'raw/d76_year_age_cause.xml').read_text()
age = {}; yr=None; ag=None
for r in rows(t):
    cells = re.findall(r'<c ([^/]*)/>', r)
    labs = [re.search(r'l="([^"]*)"',c).group(1) for c in cells if 'l="' in c]
    vals = [re.search(r' v="([^"]*)"',' '+c).group(1) for c in cells if ' v="' in ' '+c]
    if labs and re.fullmatch(r'\d{4}', labs[0]): yr=int(labs[0]); labs=labs[1:]
    if labs and labs[0] in LAB or (labs and labs[0]=='Not Stated'): ag=labs[0]; labs=labs[1:]
    if labs and labs[0]=='Alcohol-induced causes' and ag in LAB:
        d = vals[0]; d = 0 if d.lower().startswith('supp') else num(d)
        age.setdefault(yr,{})[LAB[ag]] = (d, num(vals[1]))
def aar(dct):
    return sum(W[k]/1e6 * d/p*1e5 for k,(d,p) in dct.items())
# export 2018-2024
exp = {}; tot={}
for r in csv.DictReader(open('/Users/ericpachman/PycharmProjects/SUD_V3/data/raw/wonder/mcd_2018_2024_year_age_alcohol.csv')):
    if r['Notes']=='Total' and r['Year']:
        tot[int(r['Year'])]=(num(r['Deaths']),num(r['Population']))
    elif r['Year'] and r['Ten-Year Age Groups Code'] in W:
        d=r['Deaths']; d=0 if d=='Suppressed' else num(d)
        exp.setdefault(int(r['Year']),{})[r['Ten-Year Age Groups Code']]=(d,num(r['Population']))
out = {}
print('year deaths_pub crude_pub aar_pub | my_aar_d76 diff | exp_deaths exp_crude my_aar_exp')
maxd=0
for y in range(1999,2025):
    line=f'{y}'
    o={}
    if y in pub:
        p=pub[y]; m=aar(age[y]); maxd=max(maxd,abs(m-p['aar']))
        line+=f" {p['deaths']:.0f} {p['crude']:.3f} {p['aar']:.3f} | {m:.3f} {m-p['aar']:+.3f}"
        o=dict(crude=p['crude'], aar=p['aar'], deaths=p['deaths'], pop=p['pop'])
    if y in exp:
        d,pp=tot[y]; m=aar(exp[y])
        line+=f" | {d:.0f} {d/pp*1e5:.3f} {m:.3f}"
        if y not in pub: o=dict(crude=d/pp*1e5, aar=m, deaths=d, pop=pp)
    out[y]=o; print(line)
print('max |my D76 AAR - published| 1999-2020:', round(maxd,4))
print('weights', W)
import json; json.dump(out, open(H/'deaths_series.json','w'), indent=1)
a=lambda k,ys: sum(out[y][k] for y in ys)/len(ys)
for k in ['crude','aar']:
    b,e=a(k,[2002,2003]),a(k,[2018,2019]); print(k, round(b,3), round(e,3), f'{(e/b-1)*100:.2f}%')
# pooled deaths/pop
b=(out[2002]['deaths']+out[2003]['deaths'])/(out[2002]['pop']+out[2003]['pop']); e=(out[2018]['deaths']+out[2019]['deaths'])/(out[2018]['pop']+out[2019]['pop'])
print('pooled crude', f'{(e/b-1)*100:.2f}%')
print('single-year 2003->2019 crude', f"{(out[2019]['crude']/out[2003]['crude']-1)*100:.2f}%", 'aar', f"{(out[2019]['aar']/out[2003]['aar']-1)*100:.2f}%")
print('single-year 2002->2018 crude', f"{(out[2018]['crude']/out[2002]['crude']-1)*100:.2f}%", 'aar', f"{(out[2018]['aar']/out[2002]['aar']-1)*100:.2f}%")
# suppressed sensitivity
for y in range(2021,2025):
    sup={k:((9 if v[0]==0 and k in('5-14',) else v[0]),v[1]) for k,v in exp[y].items()}
    print(y,'supp=9 sens', round(aar(sup)-aar(exp[y]),4))
