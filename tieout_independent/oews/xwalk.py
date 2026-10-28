import sys, pandas as pd, warnings; warnings.filterwarnings("ignore")
for f in sys.argv[1:]:
    x = pd.read_excel(f, header=None, dtype=str)
    m = x.apply(lambda r: r.astype(str).str.contains(r"21-101[14]|21-1023|21-1018").any(), axis=1)
    print("==", f.split("/")[-1]); print(x[m].to_string())
