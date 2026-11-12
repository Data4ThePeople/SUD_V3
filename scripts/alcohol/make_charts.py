"""Two static charts (dark palette) for the alcohol data-for-thought post.
Reads data/build/alcohol/*.csv (from build_series.py); every number is computed here.
Usage: python3 scripts/alcohol/make_charts.py <out_dir>"""
import os, sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist", "alcohol")
os.makedirs(OUT, exist_ok=True)
BG, TXT, MUTED, GRID = "#181A1B", "#BBBDC0", "#7f8792", "#2c2f32"
DEATH, SURVEY = "#f0954a", "#7fa7d6"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TXT, "axes.labelcolor": TXT,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": GRID})

d = pd.read_csv(os.path.join(ROOT, "data/build/alcohol/deaths_national.csv"))
s = pd.read_csv(os.path.join(ROOT, "data/build/alcohol/nsduh_national.csv"))
assert not d.year.duplicated().any() and not s.duplicated(["outcome", "end_year"]).any()

def foot(fig, text):
    fig.text(0.04, 0.035, text, fontsize=10.5, color=MUTED, ha="left", va="bottom", linespacing=1.5)
    fig.text(0.96, 0.035, "Built by Data 4 The People", fontsize=10.5, color=MUTED, ha="right", va="bottom")

# ---------- Chart 1: crude vs age-adjusted death rate ----------
fig, ax = plt.subplots(figsize=(12, 7.2), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.07, right=0.82, top=0.80, bottom=0.17)
ax.plot(d.year, d.crude, color=MUTED, lw=1.6)
ax.plot(d.year, d.age_adjusted, color=DEATH, lw=2.6)
for y in (1999, 2019, 2021, 2024):
    v = d.set_index("year").age_adjusted[y]
    ax.plot(y, v, "o", ms=7, color=DEATH, mec=BG, mew=2)
    ax.annotate(f"{v:.1f}", (y, v), xytext={1999: (0, -20), 2019: (-16, 8)}.get(y, (0, 10)), textcoords="offset points",
                ha="right" if y == 2019 else "center", fontsize=12, color=TXT)
last = d.iloc[-1]
ax.text(2024.4, last.crude, "Crude rate", color=TXT, fontsize=12, va="center")
ax.text(2024.4, last.age_adjusted, "Age-adjusted rate", color=TXT, fontsize=12, va="center", fontweight="bold")
ax.set_ylim(0, 18); ax.set_xlim(1998.5, 2024.5)
ax.set_xticks(range(2000, 2025, 4))
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
ax.tick_params(length=0, labelsize=11)
fig.text(0.04, 0.93, "Alcohol-induced deaths per 100,000 people, U.S., 1999-2024", fontsize=19, fontweight="bold", color="#e6e7e9")
fig.text(0.04, 0.875, "The age-adjusted rate removes the effect of an older population. It rose too.",
         fontsize=13, color=TXT)
foot(fig, "Source: CDC WONDER, alcohol-induced as the underlying cause of death. Age-adjusted to the 2000 U.S. standard population; 1999-2020 as published by CDC,\n"
          "2021-2024 computed by Data 4 The People from CDC's age-group counts. Alcohol-induced causes include alcoholic liver disease\n"
          "and alcohol poisoning. They do not include drunk-driving crashes or other injuries where alcohol played a part.")
fig.savefig(os.path.join(OUT, "01-alcohol-death-rate.png"), facecolor=BG)
plt.close(fig)

# ---------- Chart 2: percent change, 2002-2003 to 2018-2019 ----------
def avg(col, y0, y1):
    return d.set_index("year")[col].loc[[y0, y1]].mean()
def pct(a, b): return (b / a - 1) * 100
sv = s.set_index(["outcome", "end_year"]).pct
n = pd.read_csv(os.path.join(ROOT, "data/build/alcohol/niaaa_national.csv"))
assert not n.duplicated(["year", "bev"]).any()
nv = n[n.bev == "all"].set_index("year").pc14  # NIAAA report #124 data file, ages 14+, fixed ABV
rows = [
    ("Share of people 12+ who drank\nalcohol in the past month", pct(sv["ALCMON", 2003], sv["ALCMON", 2019]), SURVEY),
    ("Pure alcohol sold per\nperson 14+", pct(nv.loc[[2002, 2003]].mean(), nv.loc[[2018, 2019]].mean()), SURVEY),
    ("Share of people 12+ with an\nalcohol use disorder", pct(sv["ABODALC", 2003], sv["ABODALC", 2019]), SURVEY),
    ("Alcohol-induced death rate,\nage-adjusted", pct(avg("age_adjusted", 2002, 2003), avg("age_adjusted", 2018, 2019)), DEATH),
]
fig, ax = plt.subplots(figsize=(12, 7.6), dpi=150)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
fig.subplots_adjust(left=0.30, right=0.93, top=0.79, bottom=0.21)
for i, (lab, v, c) in enumerate(rows):
    yy = len(rows) - 1 - i
    ax.barh(yy, v, height=0.52, color=c)
    ax.text(v + (1.5 if v >= 0 else -1.5), yy, f"{v:+.0f}%", va="center", ha="left" if v >= 0 else "right",
            fontsize=15, fontweight="bold", color=TXT)
    ax.text(-0.02, yy, lab, transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=13, color=TXT)
ax.axvline(0, color=MUTED, lw=1.2)
ax.set_xlim(-45, 62); ax.set_yticks([]); ax.set_ylim(-0.6, len(rows) - 0.4)
ax.set_xticks(range(-40, 61, 20)); ax.set_xticklabels([f"{t:+d}%" if t else "0" for t in range(-40, 61, 20)])
ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
for sp in ("top", "right", "left", "bottom"): ax.spines[sp].set_visible(False)
ax.tick_params(length=0, labelsize=11)
fig.text(0.04, 0.92, "The share who drink held steady. Alcohol sold and deaths rose.", fontsize=19, fontweight="bold", color="#e6e7e9")
fig.text(0.04, 0.865, "Percent change from 2002-2003 to 2018-2019, U.S.", fontsize=13, color=TXT)
foot(fig, "Sources: SAMHSA, NSDUH state small-area estimates, national rows (2-year pooled estimates; alcohol use disorder is DSM-IV).\n"
          "CDC WONDER, alcohol-induced deaths, age-adjusted rate, averaged over the same two-year spans. The survey changed\n"
          "methods in 2020-2021, so later years cannot be compared with these. NIAAA Surveillance Report #124: pure alcohol\n"
          "in beer, wine and spirits sold or shipped, per person 14+, averaged over the same years. Sales, not measured drinking.")
fig.savefig(os.path.join(OUT, "02-alcohol-change.png"), facecolor=BG)
plt.close(fig)
for lab, v, _ in rows: print(lab.replace("\n", " "), round(v, 1))

# ---------- Chart 3: beer to spirits, and stronger drinks overall ----------
nt = n.set_index(["bev", "year"])
yrs = list(range(2002, 2025))
fig = plt.figure(figsize=(12, 7.6), dpi=150); fig.patch.set_facecolor(BG)
axL = fig.add_axes([0.07, 0.24, 0.50, 0.50]); axR = fig.add_axes([0.70, 0.24, 0.26, 0.50])
TYPES = [("spirits", "Spirits", "#7fa7d6"), ("beer", "Beer", "#e3b85a"), ("wine", "Wine", "#c48fc0")]
for b, lab, c in TYPES:
    v = [nt.pc14_timevarying_abv[b, y] for y in yrs]
    axL.plot(yrs, v, color=c, lw=2.4)
    for y, val in ((yrs[0], v[0]), (yrs[-1], v[-1])):
        axL.plot(y, val, "o", ms=6, color=c, mec=BG, mew=1.5)
        axL.annotate(f"{val:.2f}", (y, val), xytext=(-8 if y == yrs[0] else 8, 0), textcoords="offset points",
                     ha="right" if y == yrs[0] else "left", va="center", fontsize=11, color=TXT)
    axL.text(2013, v[yrs.index(2013)] + 0.06, lab, color=TXT, fontsize=12, ha="center", fontweight="bold")
axL.set_ylim(0, 1.5); axL.set_xlim(1999.5, 2026.5); axL.set_xticks(range(2004, 2025, 5))
axL.set_title("Pure alcohol sold per person 14+, by type (gallons)", loc="left", fontsize=12.5, color=TXT, pad=10)
strength = [100 * nt.pc14_timevarying_abv["all", y] / nt.beverage_gal_pc14["all", y] for y in yrs]
axR.plot(yrs, strength, color="#d6d9de", lw=2.4)
for y, val in ((yrs[0], strength[0]), (yrs[-1], strength[-1])):
    axR.plot(y, val, "o", ms=6, color="#d6d9de", mec=BG, mew=1.5)
    axR.annotate(f"{val:.1f}%", (y, val), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=11, color=TXT)
axR.set_ylim(0, 10); axR.set_xlim(2000, 2026); axR.set_xticks([2004, 2014, 2024])
axR.set_yticks(range(0, 11, 2)); axR.set_yticklabels([f"{t}%" for t in range(0, 11, 2)])
axR.set_title("Average alcohol content of\nall drinks sold", loc="left", fontsize=12.5, color=TXT, pad=10)
for ax in (axL, axR):
    ax.set_facecolor(BG); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.tick_params(length=0, labelsize=11)
gal0, gal1 = nt.beverage_gal_pc14["all", 2002], nt.beverage_gal_pc14["all", 2024]
fig.text(0.04, 0.925, "Less beer, more spirits, and more alcohol in each gallon sold", fontsize=19, fontweight="bold", color="#e6e7e9")
fig.text(0.04, 0.87, f"U.S., 2002-2024. Gallons of drinks sold per person 14+ fell from {gal0:.1f} to {gal1:.1f}, but each gallon held more alcohol.",
         fontsize=13, color=TXT)
foot(fig, "Source: NIAAA Surveillance Report #124 data file. Sales and shipments, not measured drinking. Alcohol content uses NIAAA's year-by-year\n"
          "estimates for each drink type (Alcohol Research Group). Average content = pure alcohol divided by gallons of beer, wine and\n"
          "spirits sold. NIAAA's headline series assumes fixed content; it shows a larger rise in spirits after 2019.")
fig.savefig(os.path.join(OUT, "03-beer-to-spirits.png"), facecolor=BG)
plt.close(fig)
print("chart 3 strength", round(strength[0], 2), round(strength[yrs.index(2019)], 2), round(strength[-1], 2), "gal", round(gal0, 2), round(gal1, 2))
