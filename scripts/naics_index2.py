import sys, re, pandas as pd
for f in sys.argv[1:]:
    df = pd.read_excel(f, dtype=str); code, desc = df.columns[0], df.columns[1]
    d = df[desc].fillna('')
    print('=====', f)
    for pat in [r'methadon|opioid|opiate|medication.assisted|buprenorph|narcotic', r'detox']:
        for _, r in df[d.str.contains(pat, case=False)].iterrows(): print('  ', r[code], '|', r[desc])
    for c in ['621330', '621112', '621420']:
        print('  --', c, len(df[df[code] == c]), 'entries')
        for _, r in df[df[code] == c].iterrows(): print('     ', r[desc])
