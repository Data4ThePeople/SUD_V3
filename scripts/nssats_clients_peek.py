"""Check whether outpatient client-count variables are exact counts or size categories, by year (PUF files). Run with -I."""
import glob, re, zipfile, io, pandas as pd
for z in sorted(glob.glob('data/raw/nssats/*-data-*.zip')):
    y = re.search(r'-(\d{4})-', z).group(1)
    zf = zipfile.ZipFile(z); n = [x for x in zf.namelist() if x.lower().endswith(('.tsv', '.csv'))][0]
    df = pd.read_csv(io.BytesIO(zf.read(n)), sep='\t' if n.lower().endswith('.tsv') else ',', dtype=str, encoding='latin-1', keep_default_na=False)
    df.columns = [c.upper() for c in df.columns]
    for c in [c for c in df.columns if re.fullmatch(r'T_CLIOP(_[A-Z])?', c)]:
        v = pd.to_numeric(df[c], errors='coerce'); v = v[v >= 0]
        print(y, c, 'n_valid', len(v), 'n_unique', v.nunique(), 'max', v.max(), 'sum', v.sum())
