"""Summarize the national OEWS job mix in NAICS 621420 and 621330 into broad groups, and
compare the industry totals with QCEW. Reads data/clean/oews_industry_mix.csv and
data/clean/qcew.csv; writes data/build/oews_mix_summary.csv.
Any group with a withheld part is left blank for that year, not filled.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
V1 = ["21-1011", "21-1014", "21-1018", "21-1023"]
d = pd.read_csv(ROOT / "data/clean/oews_industry_mix.csv", dtype={"own_code": str, "naics": str})
q = pd.read_csv(ROOT / "data/clean/qcew.csv", dtype={"naics": str, "own": str})
q = q[(q.fips == "US") & q.naics.isin(["621420", "621330"])]

rows = []
for (y, n), g in d.groupby(["year", "naics"]):
    det, maj = g[g.level == "detailed"].set_index("occ_code"), g[g.level == "major"].set_index("occ_code")

    def s(codes, frame):
        x = frame.reindex([c for c in codes if c in frame.index]).employment
        return None if x.isna().any() else x.sum()

    total = g[g.level == "total"].employment.iloc[0]
    v1 = s([c for c in V1 if c in det.index], det)
    cs = maj.employment.get("21-0000")
    psych = s([c for c in det.index if c.startswith("19-303")], det)
    out = dict(year=y, naics=n, oews_scope="private only" if (g.own_code == "5").all() else "all ownerships (file has no ownership code)",
               oews_total=total,
               counselors_and_mhsa_social_workers=v1,
               other_community_social_service=None if cs is None or v1 is None else cs - v1,
               psychologists=psych,
               healthcare_practitioners=maj.employment.get("29-0000"),
               healthcare_support=maj.employment.get("31-0000"),
               office_admin_support=maj.employment.get("43-0000"),
               management=maj.employment.get("11-0000"))
    parts = [v for k, v in out.items() if k not in ("year", "naics", "oews_scope", "oews_total")]
    out["all_other"] = None if any(v is None or pd.isna(v) for v in parts) else total - sum(parts)
    qq = q[q.year == y]
    out["qcew_private"] = qq[(qq.naics == n) & (qq.own == "5")].emp.sum(min_count=1)
    out["qcew_all_own"] = qq[qq.naics == n].emp.sum(min_count=1)
    rows.append(out)
o = pd.DataFrame(rows)
o.to_csv(ROOT / "data/build/oews_mix_summary.csv", index=False)
pd.set_option("display.width", 250)
for n in ("621420", "621330"):
    x = o[o.naics == n].set_index("year").drop(columns="naics")
    x["v1_share_pct"] = (x.counselors_and_mhsa_social_workers / x.oews_total * 100).round(1)
    print(n); print(x.drop(columns="oews_scope").round(0).to_string()); print(x.oews_scope.value_counts().to_string())
