import sys, glob, os, pandas as pd
for d in sorted(glob.glob(os.path.join(sys.argv[1], "ex", "*"))):
    f = [x for x in os.listdir(d) if "dl" in x.lower()][0]
    df = pd.read_excel(os.path.join(d, f), dtype=str, nrows=3)
    print(os.path.basename(d), list(df.columns))
