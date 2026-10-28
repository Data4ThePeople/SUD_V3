import sys, zipfile, io, re, pandas as pd
for f in sys.argv[1:]:
    z = zipfile.ZipFile(f)
    names = [n for n in z.namelist() if n.lower().endswith(('.tsv', '.csv', '.txt'))]
    for n in names:
        b = z.read(n)
        sep = '\t' if n.lower().endswith('.tsv') or b[:2000].count(b'\t') > b[:2000].count(b',') else ','
        df = pd.read_csv(io.BytesIO(b), sep=sep, dtype=str, nrows=3, encoding='latin-1')
        nrows = b.count(b'\n')
        cols = list(df.columns)
        key = [c for c in cols if re.search(r'^(STATE|STFIPS|LOC|OWNER|OWNERSHP|FOCUS|OTP|METH|CA_|OUTPAT|OP$|CTYPE|SRVC|TOTST|STAFF|SA_|MH_|TREAT|CLIENT|LAND)', c, re.I)]
        print(f.split('/')[-1], n, 'rows~', nrows, 'ncols', len(cols)); print('   ', key[:60])
