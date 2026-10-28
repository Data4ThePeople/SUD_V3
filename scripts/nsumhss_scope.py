import glob, re, zipfile, io, pandas as pd
for z in sorted(glob.glob('data/raw/nssats/N-SUMHSS-*-data-*.zip')):
    zf = zipfile.ZipFile(z); n = [x for x in zf.namelist() if x.lower().endswith('.csv')][0]
    df = pd.read_csv(io.BytesIO(zf.read(n)), dtype=str, keep_default_na=False); df.columns = [c.upper() for c in df.columns]
    f = 'TSU21_SU' if 'TSU21_SU' in df.columns else 'TSU_SU'
    d = df[pd.to_numeric(df.CTYPE1, errors='coerce') == 1]
    print(z.split('/')[-1][:13], 'CTYPE1==1 by', f, 'x INSU x INMH x TSU_MH');
    mh = [c for c in df.columns if c.startswith('TSU') and c.endswith('_MH')][0]
    print(d.groupby([f, 'INSU', 'INMH', mh]).size().to_string())
    print(' TREATMT_SU among CTYPE1==1 & not TSU1:', d[d[f] != '1'].TREATMT_SU.value_counts().to_dict())
