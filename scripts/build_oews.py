"""Build data/clean/oews_counselors.csv from BLS OEWS state files (unchanged zips in data/raw/oews).
Run: .venv/bin/python -I scripts/build_oews.py   (from project root)
Reference period: Nov 2001, Nov 2002, May 2003 onward (file names oes01st/oes02st, then oesmYYst).
"""
import zipfile, io, re, os, pandas as pd
RAW = 'data/raw/oews'; OUT = 'data/clean'
FIPS = dict(zip('01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56 66 72 78'.split(),
 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY GU PR VI'.split()))
CODES = ['21-1011', '21-1014', '21-1018', '21-1023']
def read(zpath, kind):
    z = zipfile.ZipFile(zpath)
    name = [x for x in z.namelist() if kind in x.lower() and x.lower().endswith(('.xls', '.xlsx'))
            and '~$' not in x and 'field' not in x.lower()]
    if not name and kind == 'state':  # 2009 file is state_dl.xls
        name = [x for x in z.namelist() if x.lower().endswith(('.xls','.xlsx')) and 'field' not in x.lower()]
    df = pd.read_excel(io.BytesIO(z.read(name[0])), dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    return df, name[0]
def flag(v):
    v = str(v).strip()
    return '' if re.fullmatch(r'[0-9.,]+', v) else v
def num(v):
    v = str(v).strip().replace(',', '')
    return float(v) if re.fullmatch(r'[0-9.]+', v) else None
rows, nat = [], []
for y in range(2001, 2025):
    yy = f'{y%100:02d}'
    pre = f'oes{yy}' if y <= 2002 else f'oesm{yy}'
    st, sname = read(f'{RAW}/{pre}st.zip', 'state')
    if 'own_code' in st.columns:  # 2019+: keep cross-industry total rows only
        st = st[st['naics'].fillna('000000').isin(['000000'])]
    namecol = 'area_title' if 'area_title' in st.columns else 'state'
    sub = st[st['occ_code'].isin(CODES)]
    for _, r in sub.iterrows():
        rows.append(dict(year=y, ref_month='Nov' if y <= 2002 else 'May', state=FIPS[str(r['area']).zfill(2)], state_name=r[namecol],
                         soc=r['occ_code'], title=r['occ_title'].strip(), employment=num(r['tot_emp']),
                         rse=num(r['emp_prse']), flag=flag(r['tot_emp']) or ('' if num(r['emp_prse']) is not None else 'rse:' + flag(r['emp_prse'])),
                         source_file=f'{pre}st.zip/{sname}'))
    nt, nname = read(f'{RAW}/{pre}nat.zip', 'nat')
    if 'naics' in nt.columns:
        nt = nt[nt['naics'].fillna('000000').isin(['000000'])]
    for _, r in nt[nt['occ_code'].isin(CODES)].iterrows():
        nat.append(dict(year=y, soc=r['occ_code'], national_employment=num(r['tot_emp']), national_flag=flag(r['tot_emp'])))
df = pd.DataFrame(rows)
os.makedirs(OUT, exist_ok=True)
df.to_csv(f'{OUT}/oews_counselors.csv', index=False)
# state-to-national check, 50 states + DC only
s51 = df[~df.state.isin(['PR', 'GU', 'VI'])]
g = s51.groupby(['year', 'soc']).agg(state_sum=('employment', 'sum'), n_states_reported=('employment', 'count'),
                                     n_states_flagged=('flag', lambda f: (f != '').sum())).reset_index()
chk = g.merge(pd.DataFrame(nat), on=['year', 'soc'], how='outer')
chk['diff'] = chk.state_sum - chk.national_employment
chk['pct_diff'] = (100 * chk['diff'] / chk.national_employment).round(2)
chk.to_csv(f'{OUT}/oews_counselors_sumcheck.csv', index=False)
print(chk.to_string())
print(df.groupby(['year','soc']).title.first().to_string())
print(df[df.flag != ''].groupby(['year','soc','flag']).size().to_string())
