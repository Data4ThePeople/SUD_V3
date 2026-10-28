"""Compare published N-SUMHSS 2024 Table SU48a (state x any outpatient) to data/clean/nsumhss_outpatient.csv. Args: extracted text file."""
import sys, re, pandas as pd
t = open(sys.argv[1]).read()
i = t.find('Table SU48a. Substance use treatment facilities, by type of care offered and state or jurisdiction: Number, 2024 \n')
j = t.find('Table SU48b', i)
blk = t[i:j]
names = {'District of Columbia': 'DC'}
import json
ab = dict(zip(['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'],
 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()))
pub = {}
for line in blk.split('\n'):
    m = re.match(r'^([A-Z][A-Za-z .]+?) ([\d,]+) ([\d,]+) ', line.strip() + ' ')
    if m and m.group(1).strip() in ab: pub[ab[m.group(1).strip()]] = (int(m.group(2).replace(',', '')), int(m.group(3).replace(',', '')))
    if m and m.group(1).strip() == 'Total': print('published Total row:', m.group(2), m.group(3))
d = pd.read_csv('data/clean/nsumhss_outpatient.csv'); d = d[d.year == 2024].set_index('state')
rows = [dict(state=s, pub_total=p[0], mine_total=d.loc[s, 'facilities_total'], pub_anyop=p[1], mine_anyop=d.loc[s, 'facilities_sud_outpatient']) for s, p in pub.items()]
r = pd.DataFrame(rows); r['d_total'] = r.mine_total - r.pub_total; r['d_op'] = r.mine_anyop - r.pub_anyop
print('states parsed', len(r)); print(r[(r.d_total != 0) | (r.d_op != 0)].to_string()); print(r[['pub_total','mine_total','pub_anyop','mine_anyop']].sum())
