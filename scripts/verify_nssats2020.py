"""Compare N-SSATS 2020 report Table 6.5a (total, any outpatient) and Table 6.2a (facilities 2011-2020) with nsumhss_outpatient.csv.
Arg: extracted text of 2020_NSSATS_FINAL.pdf"""
import sys, re, pandas as pd
L = open(sys.argv[1]).read().split('\n')
NAMES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
AB = dict(zip(NAMES, 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()))
def section(title, stop, ncols):
    # PDF text puts each table's first page body before its title, so scan from the previous table title to the stop title
    i1 = max(i for i, ln in enumerate(L) if ln.startswith(stop)) if False else None
    starts = [i for i, ln in enumerate(L) if ln.startswith(title)]; stops = [i for i, ln in enumerate(L) if ln.startswith(stop)]
    a = starts[0] - 120; b = stops[0]
    out = {}
    for ln in L[a:b]:
        if True:
            m = re.match(r'^(Total|[A-Z][A-Za-z .]+?)\s+((?:[\d,]+|-)(?:\s+(?:[\d,]+|-))+)\s*$', ln.strip())
            if m and (m.group(1) in AB or m.group(1) == 'Total') and len(m.group(2).split()) == ncols and m.group(1) not in out:
                out[m.group(1)] = [int(x.replace(',', '')) if x != '-' else 0 for x in m.group(2).split()]
    return out
d = pd.read_csv('data/clean/nsumhss_outpatient.csv')
t65 = section('Table 6.5a.', 'Table 6.5b.', 14)
print('6.5a Total row:', t65.get('Total', [None])[:2])
diffs = []
for n, v in t65.items():
    if n == 'Total': continue
    r = d[(d.year == 2020) & (d.state == AB[n])].iloc[0]
    if v[0] != r.facilities_total or v[1] != r.facilities_sud_outpatient: diffs.append((n, v[:2], r.facilities_total, r.facilities_sud_outpatient))
print('6.5a states parsed', len(t65) - 1, 'mismatches', diffs)
t62 = section('Table 6.2a.', 'Table 6.2b.', 12)
yrs = [2011, 2013, 2015, 2017, 2019, 2020]; diffs = []
for n, v in t62.items():
    if n == 'Total': continue
    for y, val in zip(yrs, v[:6]):
        r = d[(d.year == y) & (d.state == AB[n])].iloc[0]
        if val != r.facilities_total: diffs.append((n, y, val, r.facilities_total))
print('6.2a states parsed', len(t62) - ('Total' in t62), 'Total row', t62.get('Total', [])[:6], 'mismatches', diffs)
