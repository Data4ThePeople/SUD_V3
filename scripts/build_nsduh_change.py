"""Build data/clean/nsduh_change.csv: SAMHSA's own tests of change in state estimates, ages 12+,
from the unchanged change tables in data/raw/nsduh_change/.

  2008-2009 vs 2018-2019  alcohol use disorder (DSM-IV)        2019NSDUHsaeLongTermCHG.htm, Table 9
  2022-2023 vs 2023-2024  substance use disorder (DSM-5)       2024-nsduh-sae-change-tables.htm, Table 21
                          alcohol use disorder (DSM-5)                                       Table 22
                          drug use disorder (DSM-5)                                          Table 24

SAMHSA marks a change significant at the .05 level with "a" and at .10 with "b". We use .05
only (Eric, 2026-10-28): a state is "increased" or "decreased" only with an "a" marker, and the
p value printed in the table must agree (< 0.05). Nothing is computed beyond the direction.
Run with: .venv/bin/python -I scripts/build_nsduh_change.py
"""
import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I leaves the script folder off the path
from build_nsduh_sud import KEEP, TableGrab, norm_state

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/nsduh_change"
OUT = ROOT / "data/clean/nsduh_change.csv"
TABLES = [  # (file, table number, part, from window, to window)
    ("2019NSDUHsaeLongTermCHG.htm", 9, "alcohol", "2008-2009", "2018-2019"),
    ("2024-nsduh-sae-change-tables.htm", 21, "all", "2022-2023", "2023-2024"),
    ("2024-nsduh-sae-change-tables.htm", 22, "alcohol", "2022-2023", "2023-2024"),
    ("2024-nsduh-sae-change-tables.htm", 24, "drug", "2022-2023", "2023-2024"),
]


def cell(v):
    m = re.fullmatch(r"([\d.]+)\s*([ab]?)", v.replace("‑", "-").strip())
    assert m, v
    return float(m.group(1)), m.group(2)


rows = []
for fname, num, part, w0, w1 in TABLES:
    p = TableGrab()
    p.feed((RAW / fname).read_text(encoding="utf-8", errors="replace"))
    t = next(t for t in p.tables if re.match(rf"Table {num}\b", re.sub(r"\s+", " ", t["caption"]).strip()))
    hdr = [h.replace("‑", "-").replace("- ", "-") for h in t["rows"][0]]
    assert hdr[1:4] == [f"12+ ({w0})", f"12+ ({w1})", "12+ (P Value)"], hdr[:4]
    seen = set()
    for r in t["rows"][1:]:
        s = norm_state(r[0])
        if s not in KEEP:
            continue
        (v0, m0), (v1, m1), (pv, _) = cell(r[1]), cell(r[2]), cell(r[3])
        assert m1 == "", r  # SAMHSA puts the marker on the earlier estimate
        if m0 == "a":
            assert pv < 0.05, r
        else:
            assert pv >= 0.05 or m0 == "", r
        change = ("increased" if v1 > v0 else "decreased") if m0 == "a" else "no significant change"
        rows.append(dict(part=part, window_from=w0, window_to=w1, state=s, pct_from=v0, pct_to=v1,
                         p_value=pv, marker=m0, change=change, source=f"{fname} Table {num}, 12+ columns"))
        seen.add(s)
    assert seen == KEEP, (fname, num, KEEP - seen)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {OUT} ({len(rows)} rows)")
