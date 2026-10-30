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


# ---- by state: one thin line per state, colored by group, with the group median in bold ----
import statistics
states = []
for f, g in d["geo"].items():
    if f == "US":
        continue
    spw = [None if g["sud_count"][i] is None or not g["workers"][i] else round(g["sud_count"][i] / g["workers"][i], 1) for i in range(len(Y))]
    wpk = [None if not g["workers"][i] else round(g["workers"][i] / g["population"][i] * 1e5, 1) for i in range(len(Y))]
    states.append(dict(abbr=g["abbr"], name=g["name"], group=group(g), sud_per_worker=spw, workers_per_100k=wpk))
with open(ROOT / "data/build/expansion_gap_states.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["state", "group", "year", "sud_per_worker", "workers_per_100k"])
    for s in states:
        for i, y in enumerate(Y):
            w.writerow([s["abbr"], s["group"], y, s["sud_per_worker"][i], s["workers_per_100k"][i]])
med = {c: {k: [None if not [s[k][i] for s in states if s["group"] == c and s[k][i] is not None] else
               round(statistics.median([s[k][i] for s in states if s["group"] == c and s[k][i] is not None]), 1) for i in range(len(Y))]
           for k in ("sud_per_worker", "workers_per_100k")} for c, _, _ in GROUPS}
html2 = """<!doctype html><meta charset="utf-8"><title>Expansion gap by state</title><style>
body{background:#13161b;color:#eef0f3;font-family:Georgia,serif;margin:24px}
h1{font-size:22px;margin:0 0 4px}p{color:#b9bec6;font-size:14px;margin:0 0 10px;max-width:1100px}
.lg span{margin-right:18px;font:12px ui-monospace,Menlo,monospace;color:#b9bec6;cursor:pointer}.lg i{display:inline-block;width:14px;height:3px;margin-right:6px;vertical-align:middle}
svg text{font-family:ui-monospace,Menlo,monospace}
#tip{position:fixed;pointer-events:none;background:#0d0f12;border:1px solid #353c46;padding:6px 9px;font:12px ui-monospace,Menlo,monospace;border-radius:4px;display:none}
</style>
<h1>People with SUD per worker, by state and Medicaid expansion status</h1>
<p>One thin line per state, colored by when the state expanded Medicaid (KFF). Bold lines are the median state in each group. Hover a line to see the state; click a legend item to show one group. SUD estimates from 2022 use a redesigned survey and are not comparable with 2019 and earlier. 2002, 2015, 2020 and 2021 have no state SUD estimates. Gaps mean no published value.</p>
<div class="lg" id="lg"></div><svg id="c" width="1160" height="380"></svg><div id="tip"></div>
<script>
const Y = __Y__, S = __S__, MED = __MED__, G = __G__, BREAK = [2001, 2014, 2019];
const svg = document.getElementById("c"), tip = document.getElementById("tip"); let only = null;
function panel(key, title, x0, ymax, step) {
  const W = 570, H = 380, m = {l: 50, r: 34, t: 40, b: 34};
  const x = yr => x0 + m.l + (yr - 2001) / 23 * (W - m.l - m.r), yy = v => H - m.b - Math.min(v, ymax) / ymax * (H - m.t - m.b);
  let s = `<text x="${x0 + m.l}" y="20" fill="#eef0f3" font-size="14" font-family="Georgia" font-weight="600">${title}</text>`;
  for (let v = 0; v <= ymax; v += step) s += `<line x1="${x0 + m.l}" x2="${x0 + W - m.r}" y1="${yy(v)}" y2="${yy(v)}" stroke="#2a3038"/><text x="${x0 + m.l - 6}" y="${yy(v) + 4}" fill="#8a919c" font-size="11" text-anchor="end">${v}${v === ymax ? "+" : ""}</text>`;
  for (const yr of [2001, 2006, 2011, 2016, 2021, 2024]) s += `<text x="${x(yr)}" y="${H - 12}" fill="#8a919c" font-size="11" text-anchor="middle">${yr}</text>`;
  s += `<line x1="${x(2014)}" x2="${x(2014)}" y1="${m.t - 6}" y2="${H - m.b}" stroke="#6a7280" stroke-dasharray="3 3"/><text x="${x(2014) + 4}" y="${m.t - 8}" fill="#8a919c" font-size="11">2014 expansion</text>`;
  if (key === "sud_per_worker") s += `<rect x="${x(2019)}" y="${m.t}" width="${x(2022) - x(2019)}" height="${H - m.t - m.b}" fill="#8a919c" fill-opacity=".12"/>`;
  const path = arr => { let p = "", prev = null;
    arr.forEach((v, i) => { if (v == null) return; const yr = Y[i];
      const join = prev != null && (yr === prev + 1 || key === "workers_per_100k") && !(key === "sud_per_worker" && BREAK.includes(prev));
      p += (join ? "L" : "M") + x(yr).toFixed(1) + "," + yy(v).toFixed(1) + (join ? "" : "h0.01"); prev = yr; });
    return p; };
  for (const st of S) { const col = G[st.group][1], vis = !only || only === st.group;
    s += `<path d="${path(st[key])}" fill="none" stroke="${col}" stroke-width="1.1" stroke-opacity="${vis ? .45 : .05}" stroke-linecap="round" data-s="${st.abbr}"/>`;
    s += `<path d="${path(st[key])}" fill="none" stroke="transparent" stroke-width="8" data-h="${st.abbr}" data-k="${key}"/>`; }
  for (const [c, [lab, col]] of Object.entries(G)) { if (only && only !== c) continue;
    s += `<path d="${path(MED[c][key])}" fill="none" stroke="${col}" stroke-width="3.2" stroke-linecap="round"/>`;
    const v = MED[c][key][Y.length - 1]; s += `<text x="${x(2024) + 5}" y="${yy(v) + 4}" fill="${col}" font-size="11" font-weight="600">${Math.round(v)}</text>`; }
  return s;
}
function draw() {
  svg.innerHTML = panel("sud_per_worker", "People with SUD per worker", 0, 250, 50) + panel("workers_per_100k", "Treatment workers per 100,000 residents", 590, 350, 50);
  document.getElementById("lg").innerHTML = Object.entries(G).map(([c, [lab, col]]) => `<span data-g="${c}" style="opacity:${!only || only === c ? 1 : .4}"><i style="background:${col}"></i>${lab} (${S.filter(s => s.group === c).length})</span>`).join("") + (only ? '<span data-g="">show all</span>' : "");
  document.querySelectorAll("#lg span").forEach(e => e.onclick = () => { only = e.dataset.g || null; draw(); });
}
svg.addEventListener("mousemove", e => {
  const h = e.target.dataset.h; svg.querySelectorAll("path[data-s]").forEach(p => p.setAttribute("stroke-width", p.dataset.s === h ? 3 : 1.1));
  if (!h) { tip.style.display = "none"; return; }
  const st = S.find(s => s.abbr === h);
  const last = k => { for (let i = Y.length - 1; i >= 0; i--) if (st[k][i] != null) return Y[i] + ": " + Math.round(st[k][i]); return "no data"; };
  tip.innerHTML = `<b>${st.name}</b> · ${G[st.group][0]}<br>People with SUD per worker, ${last("sud_per_worker")}<br>Workers per 100K, ${last("workers_per_100k")}`;
  tip.style.display = "block"; tip.style.left = e.clientX + 14 + "px"; tip.style.top = e.clientY + 14 + "px";
});
draw();
</script>"""
for k, v in {"__Y__": Y, "__S__": states, "__MED__": med, "__G__": {c: [lab, col] for c, lab, col in GROUPS}}.items():
    html2 = html2.replace(k, json.dumps(v))
(ROOT / "data/build/expansion_gap_states.html").write_text(html2)
