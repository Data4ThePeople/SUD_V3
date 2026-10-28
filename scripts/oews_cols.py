import sys, zipfile, io, pandas as pd
for f in sys.argv[1:]:
    z = zipfile.ZipFile(f)
    for name in z.namelist():
        if name.lower().endswith(('.xls','.xlsx')) and 'field' not in name.lower() and '~$' not in name:
            print(f, list(pd.read_excel(io.BytesIO(z.read(name)), nrows=1).columns)[:8])
