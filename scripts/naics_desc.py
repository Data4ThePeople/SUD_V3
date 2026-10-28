import sys, re, pandas as pd
for f in sys.argv[1:]:
    df = pd.read_excel(f, dtype=str); print('=====', f, list(df.columns))
    for _, r in df.iterrows():
        if str(r.iloc[1]).strip().rstrip('T') in ('621420', '621330', '621112') or str(r.iloc[1]).strip() in ('621420','621330','621112'):
            print(r.iloc[1], '|', r.iloc[2], '|', r.iloc[3]); print()
