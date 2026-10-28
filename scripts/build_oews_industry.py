"""Build data/clean/oews_industry_mix.csv: the national OEWS job mix inside NAICS 621420
(outpatient mental health and substance abuse centers) and 621330 (offices of mental health
practitioners), 2002-2024, from the unchanged BLS industry zips in data/raw/oews_industry.
OEWS does not publish 621112 (offices of mental health physicians) on its own.
Run: .venv/bin/python -I scripts/build_oews_industry.py   (from project root)
"""
import glob, io, re, zipfile
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NAICS = ["621420", "621330"]


def num(v):
    v = str(v).strip().replace(",", "")
    return float(v) if re.fullmatch(r"[0-9.]+", v) else None


def level(code):
    """SOC level from the code itself (older files have no group column). Detailed codes
    never end in 0."""
    if code == "00-0000":
        return "total"
    if code.endswith("-0000"):
        return "major"
    if code.endswith("00"):
        return "minor"
    return "broad" if code.endswith("0") else "detailed"


rows = []
for zp in sorted(glob.glob(str(ROOT / "data/raw/oews_industry/*.zip"))):
    z = zipfile.ZipFile(zp)
    name = next(n for n in z.namelist() if re.search(r"nat5d", n, re.I) and n.lower().endswith((".xls", ".xlsx")))
    year = int(re.search(r"(20\d\d)", name).group(1))
    d = pd.read_excel(io.BytesIO(z.read(name)), dtype=str)
    d.columns = [c.strip().lower() for c in d.columns]
    d = d[d.naics.str[:6].isin(NAICS)]
    for _, r in d.iterrows():
        rows.append(dict(year=year, naics=r["naics"][:6], own_code=r.get("own_code", ""),
                         occ_code=r["occ_code"], occ_title=str(r["occ_title"]).strip(),
                         level=level(r["occ_code"]),
                         employment=num(r["tot_emp"]), emp_flag="" if num(r["tot_emp"]) is not None else str(r["tot_emp"]).strip(),
                         rse=num(r["emp_prse"]), source_file=f"{Path(zp).name}/{name}"))
out = pd.DataFrame(rows)
out.to_csv(ROOT / "data/clean/oews_industry_mix.csv", index=False)
print(out.groupby(["year", "naics"]).size().unstack().to_string())
print(out.level.value_counts().to_string(), out.own_code.value_counts().to_string())
