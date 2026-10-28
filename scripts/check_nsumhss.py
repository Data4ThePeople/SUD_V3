"""State-to-national check for nsumhss_outpatient.csv. Compares (a) whole-file CTYPE1==1 count to the codebook's published
frequency, (b) 50+DC sum to whole-universe count (difference = territories). Run with -I."""
import sys, glob, re, zipfile, io, pandas as pd
sys.path.insert(0, 'scripts')
CB = {2000:10946,2002:11061,2003:10893,2004:10853,2005:10807,2006:11152,2008:10977,2009:10905,2010:10753,2011:11101,2012:11650,
      2013:11542,2014:11618,2015:11336,2016:11836,2017:11184,2018:12243,2019:13044,2020:13161,2021:14123,2022:14102,2023:12286,2024:13549}
st = pd.read_csv('data/clean/nsumhss_outpatient.csv')
s51 = st.groupby('year').facilities_sud_outpatient.sum()
rows = []
for z in sorted(glob.glob('data/raw/nssats/*-data-*.zip')):
    y = int(re.search(r'-(\d{4})-', z).group(1))
    zf = zipfile.ZipFile(z); n = [x for x in zf.namelist() if x.lower().endswith(('.tsv', '.csv'))][0]
    df = pd.read_csv(io.BytesIO(zf.read(n)), sep='\t' if n.lower().endswith('.tsv') else ',', dtype=str, encoding='latin-1', keep_default_na=False)
    df.columns = [c.upper() for c in df.columns]
    c1 = pd.to_numeric(df.CTYPE1, errors='coerce') == 1
    univ = c1.sum()
    if y >= 2021:
        f = 'TSU21_SU' if 'TSU21_SU' in df.columns else 'TSU_SU'
        univ = (c1 & (pd.to_numeric(df[f], errors='coerce') == 1)).sum()
    rows.append(dict(year=y, codebook_ctype1_yes_wholefile=CB.get(y), recomputed_wholefile=int(c1.sum()),
                     su_report_universe_incl_territories=int(univ), sum_50_dc=int(s51[y]), territories_diff=int(univ - s51[y])))
r = pd.DataFrame(rows); r['codebook_match'] = r.codebook_ctype1_yes_wholefile == r.recomputed_wholefile
r.to_csv('data/clean/nsumhss_outpatient_sumcheck.csv', index=False); print(r.to_string())
