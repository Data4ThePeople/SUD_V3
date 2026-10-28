import sys, zipfile, io, pandas as pd
z = zipfile.ZipFile(sys.argv[1]); name = sys.argv[2]
df = pd.read_excel(io.BytesIO(z.read(name)), header=None, dtype=str)
for row in df.fillna('').values.tolist():
    s = ' | '.join(x for x in row if x)
    if any(k in s for k in ['**', '#', 'self-employ', 'footnote', 'Note']): print(s[:400])
