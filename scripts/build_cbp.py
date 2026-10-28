"""Build data/clean/cbp_621420.csv (+ _lfo, _sumcheck) from Census CBP state and U.S. files in data/raw/cbp.
Run: .venv/bin/python -I scripts/build_cbp.py
Employment is mid-March; CBP excludes most government employees, self-employed, private households, railroads, ag production.
"""
import zipfile, io, os, pandas as pd
RAW, OUT = 'data/raw/cbp', 'data/clean'
FIPS = dict(zip('01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56'.split(),
 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()))
def load(path):
    if path.endswith('.zip'):
        z = zipfile.ZipFile(path); name = z.namelist()[0]
        b = z.read(name)
    else:
        name = os.path.basename(path); b = open(path, 'rb').read()
    df = pd.read_csv(io.BytesIO(b), dtype=str, keep_default_na=False, encoding='latin-1')
    df.columns = [c.lower() for c in df.columns]
    return df[df.naics == '621420'].copy(), name
rows, lfo_rows, nat = [], [], []
for y in range(2001, 2024):
    yy = f'{y%100:02d}'
    st, sname = load(f'{RAW}/cbp{yy}st.zip')
    if 'lfo' not in st.columns: st['lfo'] = '-'
    for _, r in st.iterrows():
        if r.fipstate not in FIPS: continue
        rec = dict(year=y, state=FIPS[r.fipstate], fips=r.fipstate, lfo=r.lfo, establishments=int(r.est),
                   employment=int(r.emp), empflag=r.get('empflag', ''), emp_noise_flag=r.get('emp_nf', ''),
                   annual_payroll_k=int(r.ap), source_file=f'cbp{yy}st.zip/{sname}')
        (rows if r.lfo == '-' else lfo_rows).append(rec)
    usp = f'{RAW}/cbp{yy}us.zip' if os.path.exists(f'{RAW}/cbp{yy}us.zip') else f'{RAW}/cbp{yy}us.txt'
    us, _ = load(usp)
    if 'lfo' in us.columns: us = us[us.lfo == '-']
    u = us.iloc[0]
    nat.append(dict(year=y, us_establishments=int(u.est), us_employment=int(u.emp),
                    us_empflag=u.get('empflag', ''), us_emp_noise_flag=u.get('emp_nf', '')))
os.makedirs(OUT, exist_ok=True)
df = pd.DataFrame(rows)
# flag meaning: employment withheld (D/S) means 0 is NOT a real zero
df['employment_withheld'] = (df.empflag != '') | df.emp_noise_flag.isin(['D', 'S', 'N'])
df.to_csv(f'{OUT}/cbp_621420.csv', index=False)
pd.DataFrame(lfo_rows).to_csv(f'{OUT}/cbp_621420_lfo.csv', index=False)
g = df.groupby('year').agg(n_states=('state', 'nunique'), state_sum_est=('establishments', 'sum'),
                           state_sum_emp=('employment', 'sum'), n_emp_withheld=('employment_withheld', 'sum')).reset_index()
chk = g.merge(pd.DataFrame(nat), on='year')
chk['est_diff'] = chk.state_sum_est - chk.us_establishments
chk['emp_diff'] = chk.state_sum_emp - chk.us_employment
chk['emp_pct_diff'] = (100 * chk.emp_diff / chk.us_employment).round(2)
chk.to_csv(f'{OUT}/cbp_621420_sumcheck.csv', index=False)
print(chk.to_string())
print(df[df.employment_withheld][['year', 'state', 'establishments', 'empflag', 'emp_noise_flag']].to_string())
l = pd.DataFrame(lfo_rows)
if len(l): print(l.groupby(['year', 'lfo']).establishments.sum().unstack().to_string())
