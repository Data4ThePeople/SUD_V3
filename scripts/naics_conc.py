import sys, pandas as pd
for f in sys.argv[1:]:
    raw = pd.read_excel(f, dtype=str, header=None)
    hdr = raw.index[raw.apply(lambda r: r.astype(str).str.contains('NAICS', case=False).sum() >= 2, axis=1)][0]
    df = pd.read_excel(f, dtype=str, header=hdr)
    m = df[df.apply(lambda r: r.astype(str).str.contains(r'^62(1112|1330|1420)$|^62142|^62133|^621112', regex=True).any(), axis=1)]
    print('=====', f); print(m.iloc[:, :6].to_string())
