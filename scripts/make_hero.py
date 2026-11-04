"""Hero image for the visualization post: the 2024 People with SUD per Worker map, as the page draws it.

Writes data/build/hero.html and renders it to
posts/substance-use-treatment-viz/images/substance-use-treatment-viz-hero-1680x1080.png
with headless Chrome. Colors and the 25 to 200+ scale are the page's own (template.html, RAMPS.gap and
METRICS.gap.dom for 2022 on).
"""
import json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "substance-use-treatment-viz"
IMG = ROOT / "posts" / SLUG / "images"
YEAR = 2024
RAMP = ["#fdebd8", "#f9c999", "#f3a35d", "#e47f2c", "#bf5f15", "#8f430a"]
LO, HI = 25, 200

D = json.loads((ROOT / "data/build/dashboard.json").read_text())
PATHS = json.loads((ROOT / "data/build/state_paths.json").read_text())
i = D["years"].index(YEAR)


def gap(g):
    s, w = g["sud_count"][i], g["workers"][i]
    return None if s is None or w is None or g["workers_flag"][i] else s / w


def color(v):  # same linear interpolation as the page's rampColor
    t = max(0, min(1, (v - LO) / (HI - LO))) * (len(RAMP) - 1)
    k = min(int(t), len(RAMP) - 2)
    f = t - k
    a, b = (tuple(int(h[j:j + 2], 16) for j in (1, 3, 5)) for h in RAMP[k:k + 2])
    return "rgb(%d,%d,%d)" % tuple(round(x + (y - x) * f) for x, y in zip(a, b))


us = gap(D["geo"]["US"])
vals = {f: gap(D["geo"][f]) for f in PATHS}
assert all(v is not None for v in vals.values()), "every state has a 2024 value"
hi_st = max(vals, key=vals.get)
lo_st = min(vals, key=vals.get)
shapes = "".join(f'<path d="{d}" fill="{color(vals[f])}"/>' for f, d in PATHS.items())
grad = ",".join(RAMP)

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1680px;height:1080px;background:#13161b;color:#eef0f3;font-family:Georgia,"Times New Roman",serif;overflow:hidden}}
.mono{{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
.cap{{position:absolute;left:150px;top:150px;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#b9bec6}}
svg{{position:absolute;left:120px;top:215px;width:940px}}
svg path{{stroke:#13161b;stroke-width:.8}}
.leg{{position:absolute;left:230px;top:850px;width:620px}}
.leg .bar{{height:18px;border-radius:2px;background:linear-gradient(90deg,{grad})}}
.leg .ends{{display:flex;justify-content:space-between;font-size:20px;color:#b9bec6;margin-top:10px}}
.leg .lab{{display:flex;justify-content:space-between;font-size:18px;color:#7f8792;margin-bottom:10px}}
.side{{position:absolute;left:1110px;top:250px;width:470px}}
h1{{font-size:62px;line-height:1.05;margin:0;font-weight:700}}
h1 span{{display:block;color:#f0a29a}}
.big{{font-size:120px;font-weight:700;color:#f0954a;margin:70px 0 6px;line-height:1}}
.what{{font-size:27px;line-height:1.35;color:#d6d9de}}
.range{{font-size:22px;line-height:1.5;color:#9aa1ab;margin-top:34px}}
.foot{{position:absolute;left:1110px;top:900px;font-size:17px;color:#7f8792}}
</style></head><body>
<div class="cap mono">People with SUD per treatment worker, {YEAR}</div>
<svg viewBox="0 0 975 610">{shapes}</svg>
<div class="leg mono"><div class="lab"><span>Fewer per worker</span><span>More per worker</span></div><div class="bar"></div>
<div class="ends"><span>{LO}</span><span>{HI}+</span></div></div>
<div class="side"><h1>Substance Use Treatment<span>State by State</span></h1>
<div class="big mono">{round(us)}</div>
<div class="what">people with a substance use disorder for each treatment worker in the U.S., {YEAR}</div>
<div class="range">{D["geo"][hi_st]["name"]}: {round(vals[hi_st])} &nbsp;·&nbsp; {D["geo"][lo_st]["name"]}: {round(vals[lo_st])}</div></div>
<div class="foot mono">Data 4 The People &nbsp;·&nbsp; Sources: SAMHSA, BLS</div>
</body></html>"""

out = ROOT / "data/build/hero.html"
out.write_text(html)
png = IMG / f"{SLUG}-hero-1680x1080.png"
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1680,1080",
                f"--screenshot={png}", out.as_uri()], check=True, capture_output=True)
shutil.copy(png, IMG / f"{SLUG}-hero-source.png")
print(png, "US", round(us), hi_st, round(vals[hi_st]), lo_st, round(vals[lo_st]))
