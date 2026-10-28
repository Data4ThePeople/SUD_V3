"""Rebuild OEWS treatment workers from raw BLS files.
usage: build.py <raw_oews dir> <out csv>"""
import sys, os, glob, re, pandas as pd, warnings
warnings.filterwarnings("ignore")
raw, outp = sys.argv[1], sys.argv[2]
CODES = ["21-1011", "21-1014", "21-1018", "21-1023"]
rows = []
for d in sorted(glob.glob(os.path.join(raw, "ex", "*"))):
    tag = os.path.basename(d)
    yy = int(re.search(r"(\d\d)(st|nat)$", tag).group(1)); y = 2000 + yy
    kind = "nat" if tag.endswith("nat") else "st"
    f = [x for x in os.listdir(d) if "dl" in x.lower() and not x.startswith("~")][0]
    df = pd.read_excel(os.path.join(d, f), dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    n0 = len(df)
    if "i_group" in df.columns:
        info = (df.i_group.value_counts().to_dict(), df.own_code.value_counts().to_dict())
        df = df[df.i_group.str.strip().str.lower() == "cross-industry"]
        print(y, kind, "i_group/own_code", info, file=sys.stderr)
    if kind == "st":
        df["fips"] = df["area"].str.strip().str.zfill(2)
    else:
        df["fips"] = "US"
    df["occ_code"] = df.occ_code.str.strip()
    sub = df[df.occ_code.isin(CODES)]
    # duplicates check
    dup = sub.duplicated(["fips", "occ_code"]).sum()
    if dup: print("DUPLICATES", y, kind, dup, file=sys.stderr)
    for _, r in sub.iterrows():
        rows.append(dict(year=y, fips=r.fips, occ=r.occ_code, tot_emp=str(r.tot_emp).strip(),
                         emp_prse=str(r.emp_prse).strip(), title=str(r.get("occ_title", r.get("occ_titl"))).strip()))
    print(y, kind, f, n0, "rows ->", len(sub), file=sys.stderr)
out = pd.DataFrame(rows)
out.to_csv(outp, index=False)
