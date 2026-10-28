import sys, re, pandas as pd
CODES = ['621420', '621330', '621112', '622210', '623220', '621493', '621111', '621399', '621910', '624190']
PAT = re.compile(r'methadone|opioid|medication.assisted|detox|drug|alcohol|substance|addict|chemical depend|narcotic|rehab', re.I)
for f in sys.argv[1:]:
    df = pd.read_excel(f, dtype=str)
    df.columns = [c.strip() for c in df.columns]
    code, desc = df.columns[0], df.columns[1]
    hit = df[df[desc].fillna('').str.contains(PAT) & df[code].fillna('').str.startswith('62')]
    print('=====', f, list(df.columns), len(df))
    for _, r in hit.sort_values(code).iterrows(): print(r[code], '|', r[desc])
