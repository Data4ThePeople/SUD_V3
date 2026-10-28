import sys, zipfile, io, pandas as pd
out = sys.argv[1]
with open(out, 'w') as fo:
    for f in sys.argv[2:]:
        z = zipfile.ZipFile(f)
        n = [n for n in z.namelist() if n.lower().endswith(('.tsv', '.csv'))][0]
        b = z.read(n); sep = '\t' if n.lower().endswith('.tsv') else ','
        df = pd.read_csv(io.BytesIO(b), sep=sep, dtype=str, nrows=2, encoding='latin-1')
        fo.write(f.split('/')[-1][:14] + ' ' + ' '.join(df.columns) + '\n')
