"""Exploration: People with SUD per Worker and workers per 100K, by Medicaid expansion group.
Groups from KFF (data/raw/kff/medicaid_expansion.csv): expanded 2014-2015, expanded 2016 or later,
never expanded. Pooled ratios = group sum / group sum over states with both values that year.
Writes data/build/expansion_gap.csv and data/build/expansion_gap.html."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "data/build/dashboard.json").read_text()); Y = d["years"]
kff = {r["state"]: r for r in csv.DictReader(open(ROOT / "data/raw/kff/medicaid_expansion.csv"))}
GROUPS = [("2014-15", "Expanded 2014-2015", "#5aa9ff"), ("2016+", "Expanded 2016 or later", "#9aa1ab"), ("never", "Never expanded", "#f0954a")]


def group(g):
    r = kff[g["name"]]
    if r["status"] != "Adopted":
        return "never"
    return "2014-15" if int(r["implementation_date"].split("/")[-1]) <= 2015 else "2016+"


rows = []
for i, y in enumerate(Y):
    for c, _, _ in GROUPS:
        ok = [g for f, g in d["geo"].items() if f != "US" and group(g) == c and g["sud_count"][i] is not None and g["workers"][i]]
        n = sum(1 for f, g in d["geo"].items() if f != "US" and group(g) == c)
        if not ok:
            continue
        sud, wk, pop = (sum(g[k][i] for g in ok) for k in ("sud_count", "workers", "population"))
        rows.append(dict(year=y, group=c, states=len(ok), of=n, sud_per_worker=round(sud / wk, 1), workers_per_100k=round(wk / pop * 1e5, 1)))
with open(ROOT / "data/build/expansion_gap.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

BREAK_AFTER = {2001, 2014, 2019}  # SUD survey changes: do not draw the line across these


def panel(key, title, x0, ymax, step):
    W, H, m = 560, 330, dict(l=50, r=16, t=40, b=34)
    x = lambda yr: x0 + m["l"] + (yr - 2001) / 23 * (W - m["l"] - m["r"])
    yy = lambda v: H - m["b"] - v / ymax * (H - m["t"] - m["b"])
    s = f'<text x="{x0 + m["l"]}" y="20" class="t">{title}</text>'
    for v in range(0, ymax + 1, step):
        s += f'<line x1="{x0 + m["l"]}" x2="{x0 + W - m["r"]}" y1="{yy(v)}" y2="{yy(v)}" class="g"/><text x="{x0 + m["l"] - 6}" y="{yy(v) + 4}" class="a" text-anchor="end">{v}</text>'
    for yr in (2001, 2006, 2011, 2016, 2021, 2024):
        s += f'<text x="{x(yr)}" y="{H - 12}" class="a" text-anchor="middle">{yr}</text>'
    s += f'<line x1="{x(2014)}" x2="{x(2014)}" y1="{m["t"] - 6}" y2="{H - m["b"]}" class="e"/><text x="{x(2014) + 4}" y="{m["t"] - 8}" class="a">2014 expansion</text>'
    if key == "sud_per_worker":
        s += f'<rect x="{x(2019)}" y="{m["t"]}" width="{x(2022) - x(2019)}" height="{H - m["t"] - m["b"]}" fill="#8a919c" fill-opacity=".12"/><text x="{x(2019) + 4}" y="{m["t"] + 12}" class="a">survey redesign</text>'
    for c, _, col in GROUPS:
        pts = [(r["year"], r[key]) for r in rows if r["group"] == c]
        path, prev = "", None
        for yr, v in pts:
            join = prev is not None and (yr == prev + 1 or key == "workers_per_100k") and not (key == "sud_per_worker" and prev in BREAK_AFTER)
            path += ("L" if join else "M") + f"{x(yr):.1f},{yy(v):.1f}"; prev = yr
        s += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2.2"/>'
        yr, v = pts[-1]
        s += f'<circle cx="{x(yr)}" cy="{yy(v)}" r="3.5" fill="{col}"/><text x="{x(yr) - 6}" y="{yy(v) - 8}" class="v" text-anchor="end" fill="{col}">{v:.0f}</text>'
    return s


svg = panel("sud_per_worker", "People with SUD per worker", 0, 160, 40) + panel("workers_per_100k", "Treatment workers per 100,000 residents", 580, 200, 50)
legend = "".join(f'<span><i style="background:{col}"></i>{lab}</span>' for _, lab, col in GROUPS)
html = f"""<!doctype html><meta charset="utf-8"><style>
body{{background:#13161b;color:#eef0f3;font-family:Georgia,serif;margin:24px}}
h1{{font-size:22px;margin:0 0 4px}}p{{color:#b9bec6;font-size:14px;margin:0 0 10px;max-width:1080px}}
.t{{fill:#eef0f3;font:600 14px Georgia}}.a{{fill:#8a919c;font:11px ui-monospace,Menlo,monospace}}.v{{font:600 12px ui-monospace,Menlo,monospace}}
.g{{stroke:#2a3038}}.e{{stroke:#6a7280;stroke-dasharray:3 3}}
.lg span{{margin-right:18px;font:12px ui-monospace,Menlo,monospace;color:#b9bec6}}.lg i{{display:inline-block;width:14px;height:3px;margin-right:6px;vertical-align:middle}}
</style>
<h1>People with SUD per worker, by Medicaid expansion status</h1>
<p>States grouped by when they expanded Medicaid (KFF). Each line pools the states in the group. SUD estimates from 2022 use a redesigned survey and are not comparable with 2019 and earlier. 2002, 2015, 2020 and 2021 have no state SUD estimates.</p>
<div class="lg">{legend}</div>
<svg width="1140" height="330" viewBox="0 0 1140 330">{svg}</svg>"""
(ROOT / "data/build/expansion_gap.html").write_text(html)
print(f"{len(rows)} rows")
