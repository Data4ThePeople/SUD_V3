"""Build data/clean/nsumhss_outpatient.csv from SAMHSA N-SSATS (2000, 2002-2020) and N-SUMHSS (2021-2024) public-use files.
Run: .venv/bin/python -I scripts/build_nsumhss.py
Facility universe per year:
  N-SSATS: every PUF record (the PUF holds the facilities 'included in report': treatment or detox, respondents).
  N-SUMHSS: TSU21_SU (2021) / TSU_SU (2022+) == 1  ('Inclusion/exclusion flag for substance use report' = Treatment/detoxification).
  Alt column facilities_sud_outpatient_incl_mh_list (2021+): adds facilities listed only on the mental health inventory
  (TSU flag missing) that answered TREATMT_SU==1 and CTYPE1==1. SAMHSA's SU report excludes them. Equals the main column before 2021.
Outpatient: CTYPE1 == 1  ('Does this facility offer OUTPATIENT substance abuse/use services' / 'Any outpatient substance use care offered').
Ownership: OWNERSHP 1 private for-profit, 2 private non-profit, 3 state govt, 4 local/county/community govt, 5 tribal govt, 6 federal govt.
OTP: OTP == 1 (facility operates a SAMHSA-certified opioid treatment program); not asked in 2000.
50 states + DC only; territories dropped.
"""
import zipfile, io, glob, os, re, pandas as pd
RAW, OUT = 'data/raw/nssats', 'data/clean'
FIPS = dict(zip('01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56'.split(),
 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()))
ST51 = set(FIPS.values())
OWN = {1: 'own_private_forprofit', 2: 'own_private_nonprofit', 3: 'own_state_govt', 4: 'own_local_govt', 5: 'own_tribal_govt', 6: 'own_federal_govt'}
def load(zpath):
    z = zipfile.ZipFile(zpath)
    n = [x for x in z.namelist() if x.lower().endswith(('.tsv', '.csv'))][0]
    b = z.read(n); sep = '\t' if n.lower().endswith('.tsv') else ','
    df = pd.read_csv(io.BytesIO(b), sep=sep, dtype=str, encoding='latin-1', keep_default_na=False)
    df.columns = [c.strip().upper() for c in df.columns]
    return df, f'{os.path.basename(zpath)}/{n}'
def num(s): return pd.to_numeric(s, errors='coerce')
rows, notes = [], []
for zpath in sorted(glob.glob(f'{RAW}/*-data-*.zip')):
    year = int(re.search(r'-(\d{4})-', zpath).group(1))
    df, src = load(zpath)
    survey = 'N-SUMHSS' if year >= 2021 else 'N-SSATS'
    n_file = len(df)
    if survey == 'N-SUMHSS':
        flag = 'TSU21_SU' if 'TSU21_SU' in df.columns else 'TSU_SU'
        # alt universe: also count MH-list facilities (INSU missing) that answered the SU module and offer SU outpatient care
        df['alt'] = (num(df[flag]) == 1) | (df[flag].str.strip().isin(['M', '', '.']) & (num(df['TREATMT_SU']) == 1))
        df = df[df.alt]
        df['core'] = num(df[flag]) == 1
        universe = f'{flag}==1'
        df['ST'] = df['LOCATIONSTATE'].str.strip()
    else:
        universe = 'all PUF records'
        df['core'] = True
        if 'STATE' in df.columns and df['STATE'].str.strip().str.len().eq(2).all() and not df['STATE'].str.strip().str.isdigit().all():
            df['ST'] = df['STATE'].str.strip()
        else:
            df['ST'] = df['STFIPS'].str.strip().str.zfill(2).map(FIPS)
    n_univ = int(df.core.sum())
    terr = df[~df.ST.isin(ST51)].ST.value_counts().to_dict()
    df = df[df.ST.isin(ST51)].copy()
    df['op'] = num(df['CTYPE1']) == 1
    df['own'] = num(df['OWNERSHP'])
    df['otp'] = num(df['OTP']) == 1 if 'OTP' in df.columns else pd.NA
    for st in sorted(ST51):
        dd = df[df.ST == st]; d = dd[dd.core]; o = d[d.op]
        r = dict(year=year, survey=survey, state=st, facilities_total=len(d), facilities_sud_outpatient=int(o.op.sum()),
                 facilities_sud_outpatient_incl_mh_list=int(dd.op.sum()) if survey == 'N-SUMHSS' else int(o.op.sum()))
        for k, name in OWN.items(): r[name] = int((o.own == k).sum())
        r['own_missing'] = int((~o.own.isin(list(OWN))).sum())
        r['outpatient_otp'] = int(o.otp.sum()) if 'OTP' in df.columns else None
        r['facilities_otp_any_setting'] = int(d.otp.sum()) if 'OTP' in df.columns else None
        r['source_file'] = src
        r['variable_definition'] = f'universe: {universe}; outpatient: CTYPE1==1; ownership: OWNERSHP; OTP: ' + ('OTP==1' if 'OTP' in df.columns else 'not asked')
        rows.append(r)
    notes.append(dict(year=year, survey=survey, puf_rows=n_file, universe_rows=n_univ, territory_rows=sum(terr.values()), territories=str(terr),
                      ctype1_missing_in_51=int(num(df['CTYPE1']).isna().sum()), own_values=str(sorted(df.own.dropna().unique().tolist()))))
# 2001: no N-SSATS was conducted (reference date moved from Oct 1, 2000 to Mar 29, 2002). Rows kept, values left empty.
for st in sorted(ST51):
    rows.append(dict(year=2001, survey='none', state=st, source_file='', variable_definition='survey not conducted in 2001'))
os.makedirs(OUT, exist_ok=True)
out = pd.DataFrame(rows).sort_values(['year', 'state'])
for c in out.columns:
    if c.startswith(('facilities', 'own_', 'outpatient')): out[c] = out[c].astype('Int64')
out.to_csv(f'{OUT}/nsumhss_outpatient.csv', index=False)
nt = pd.DataFrame(notes).sort_values('year'); nt.to_csv(f'{OUT}/nsumhss_outpatient_filelog.csv', index=False)
print(nt.to_string())
print(out.groupby('year')[['facilities_total', 'facilities_sud_outpatient', 'own_private_forprofit', 'own_private_nonprofit', 'own_state_govt', 'own_local_govt', 'own_tribal_govt', 'own_federal_govt', 'own_missing', 'outpatient_otp']].sum().to_string())
