"""Animated GIF of chart 02 (alcohol-induced death rate, 1999-2024) for social posts.

Both lines draw in from 1999 to 2024 over about 8 seconds, then the finished chart holds for about 5.
Same data, colors, titles and labels as chart 02 in make_charts.py. Labels show only published
yearly values, never in-between ones.

    .venv/bin/python scripts/alcohol/animate_deaths.py [seconds] [hold_seconds]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(ROOT, "posts", "alcohol-deaths-data-for-thought", "social")
SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
HOLD = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
FRAME_MS = 80
WIDTH_PX = 1200
BG, TXT, MUTED, GRID = "#181A1B", "#BBBDC0", "#7f8792", "#2c2f32"
DEATH = "#f0954a"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TXT, "axes.labelcolor": TXT,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": GRID})

d = pd.read_csv(os.path.join(ROOT, "data/build/alcohol/deaths_national.csv")).sort_values("year")
X = d.year.to_numpy(float); CR = d.crude.to_numpy(); AA = d.age_adjusted.to_numpy()
MARK = (1999, 2019, 2021, 2024)
OFFS = {1999: (0, -20), 2019: (-16, 8)}

fig, ax = plt.subplots(figsize=(12, 7.2), dpi=WIDTH_PX / 12)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.07, right=0.82, top=0.80, bottom=0.20)
ax.set_ylim(0, 18); ax.set_xlim(1998.5, 2024.5)
ax.set_xticks(range(2000, 2025, 4))
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
ax.tick_params(length=0, labelsize=11)
fig.text(0.04, 0.93, "Alcohol-induced deaths per 100,000 people, U.S., 1999-2024", fontsize=19, fontweight="bold", color="#e6e7e9")
fig.text(0.04, 0.875, "The age-adjusted rate removes the effect of an older population. It rose too.", fontsize=13, color=TXT)
fig.text(0.04, 0.035, "Source: CDC WONDER, alcohol-induced as the underlying cause of death. Age-adjusted to the 2000 U.S. standard population;\n"
         "1999-2020 as published by CDC, 2021-2024 computed by Data 4 The People from CDC's age-group counts.\n"
         "Alcohol-induced causes include alcoholic liver disease and alcohol poisoning. They do not include\n"
         "drunk-driving crashes or other injuries where alcohol played a part.",
         fontsize=10.5, color=MUTED, ha="left", va="bottom", linespacing=1.5)
fig.text(0.96, 0.035, "Built by Data 4 The People", fontsize=10.5, color=MUTED, ha="right", va="bottom")

crude_line, = ax.plot([], [], color=MUTED, lw=1.6)
aa_line, = ax.plot([], [], color=DEATH, lw=2.6)
dots = {}
for y in MARK:
    v = float(d.set_index("year").age_adjusted[y])
    dot, = ax.plot(y, v, "o", ms=7, color=DEATH, mec=BG, mew=2, visible=False)
    lab = ax.annotate(f"{v:.1f}", (y, v), xytext=OFFS.get(y, (0, 10)), textcoords="offset points",
                      ha="right" if y == 2019 else "center", fontsize=12, color=TXT, visible=False)
    dots[y] = (dot, lab)
crude_lab = ax.text(2024.4, CR[-1], "Crude rate", color=TXT, fontsize=12, va="center", visible=False)
aa_lab = ax.text(2024.4, AA[-1], "Age-adjusted rate", color=TXT, fontsize=12, va="center", fontweight="bold", visible=False)
clock = ax.text(0.03, 0.93, "", transform=ax.transAxes, color=TXT, fontsize=18, fontweight="bold", ha="left", va="center")


def draw(cursor, final=False):
    keep = X <= cursor
    xs = list(X[keep]); c_ys = list(CR[keep]); a_ys = list(AA[keep])
    if xs and xs[-1] < cursor:  # line tip between years; no label sits on it
        xs.append(cursor); c_ys.append(float(np.interp(cursor, X, CR))); a_ys.append(float(np.interp(cursor, X, AA)))
    crude_line.set_data(xs, c_ys); aa_line.set_data(xs, a_ys)
    for y, (dot, lab) in dots.items():
        dot.set_visible(cursor >= y); lab.set_visible(cursor >= y)
    crude_lab.set_visible(final); aa_lab.set_visible(final)
    clock.set_text("" if final or not keep.any() else str(int(X[keep][-1])))
    fig.canvas.draw()
    return Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert("RGB").copy()


os.makedirs(OUT, exist_ok=True)
n = int(round(SECONDS * 1000 / FRAME_MS))
frames = [draw(X[0] + (X[-1] - X[0]) * i / (n - 1)) for i in range(n)]
last = draw(X[-1], final=True)
plt.close(fig)
pal = last.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames] + [pal]
path = os.path.join(OUT, "02-alcohol-death-rate.gif")
q[0].save(path, save_all=True, append_images=q[1:], duration=[FRAME_MS] * n + [int(HOLD * 1000)], loop=0, optimize=False, disposal=1)
last.save(os.path.join(OUT, "02-alcohol-death-rate-final-frame.png"))
print(f"{os.path.basename(path)}: {len(q)} frames, {last.size[0]}x{last.size[1]}, {n * FRAME_MS / 1000:.1f}s + {HOLD:.0f}s hold, "
      f"{os.path.getsize(path) / 1e6:.2f} MB")
