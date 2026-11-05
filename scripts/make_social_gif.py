"""Animated GIF for social posts: the page's four map views for 2024, one after another.

Screenshots dist/index.html (standalone, #m=<view>&y=2024) with headless Chrome, with the legend and
era rows held at a fixed height so the map does not jump between views, and transitions off so
each shot shows its finished state. Each view holds, then cuts to the next, and the loop repeats. Writes
posts/substance-use-treatment-viz/social/viz-four-views-2024.gif

    .venv/bin/python scripts/make_social_gif.py
"""
import subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "posts" / "substance-use-treatment-viz" / "social" / "viz-four-views-2024.gif"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VIEWS = ["sud", "estab", "gap", "death"]
YEAR = 2024
W, H, CROP = 1200, 1500, 1068   # crop ends just below the map
HOLD_MS = 3000
FIX = "*{transition:none!important;animation:none!important}#legend{height:96px;align-content:flex-start;box-sizing:border-box}#era{height:52px;box-sizing:border-box}"

tmp = Path(tempfile.mkdtemp())
page = tmp / "page.html"
page.write_text((ROOT / "dist/index.html").read_text().replace("</style>", FIX + "</style>", 1))

shots = []
for m in VIEWS:
    png = tmp / f"{m}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=4000", f"--screenshot={png}",
                    f"{page.as_uri()}#embed=0&m={m}&y={YEAR}"], check=True, capture_output=True)
    shots.append(Image.open(png).convert("RGB").crop((0, 0, W, CROP)))

frames, durations = shots, [HOLD_MS] * len(shots)

OUT.parent.mkdir(parents=True, exist_ok=True)
pal = [f.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
print(OUT, f"{OUT.stat().st_size / 1e6:.1f} MB", len(frames), "frames", sum(durations) / 1000, "s per loop")
