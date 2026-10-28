import sys, zipfile, io, pandas as pd
for f in sys.argv[1:]:
    z = zipfile.ZipFile(f)
    n = [x for x in z.namelist() if ('state' in x.lower() or 'national' in x.lower() or 'nat' in x.lower()) and x.lower().endswith(('.xls','.xlsx')) and '~$' not in x and 'field' not in x.lower()]
    for name in n:
        b = io.BytesIO(z.read(name))
        df = pd.read_excel(b, nrows=5, header=None, dtype=str)
        print(f, name); print(df.iloc[:5, :12].to_string())
