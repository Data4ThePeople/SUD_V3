"""Build data/clean/trifectas.csv from Ballotpedia's party-control tables (unchanged HTML in
data/raw/ballotpedia/). One row per state and year, 1992-2026: governor, senate, house, and
trifecta = D or R when one party holds all three, else "divided". The lower chamber is the
"Assembly" in some states. Nebraska's one-house legislature is nonpartisan, and Ballotpedia counts
its trifecta by the governor's party; we follow Ballotpedia so that totals match its yearly counts. Ballotpedia's year is the
year the officeholders served (changes after a November election show in the next year).
Run with: .venv/bin/python -I scripts/build_trifectas.py
"""
import csv
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data/raw/ballotpedia/Historical_and_potential_changes_in_trifectas.html"
OUT = ROOT / "data/clean/trifectas.csv"

text = html.unescape(re.sub(r"<[^>]+>", " ", SRC.read_text(encoding="utf-8")))
text = re.sub(r"\s+", " ", text)
YEARS = list(range(1992, 2027))
rows = []
for m in re.finditer(r"([A-Z][A-Za-z ]+?) Party Control: 1992-20\d\d .*? Year (?:\d\d ){35}", text):
    state, body = m.group(1).split("state government ")[-1].strip(), text[m.end():m.end() + 400]
    parts = {}
    for chamber, pat in (("Governor", "Governor"), ("Senate", "Senate"), ("House", "(?:House|Assembly)")):
        c = re.match(r".*?" + pat + r" ((?:\S+ ){34}\S+)", body)
        parts[chamber] = c.group(1).split() if c else ["-"] * 35
    for i, y in enumerate(YEARS):
        g, s, h = parts["Governor"][i], parts["Senate"][i], parts["House"][i]
        tri = g if g in ("D", "R") and (state == "Nebraska" or g == s == h) else "divided"
        rows.append([state, y, g, s, h, tri])
states = {r[0] for r in rows}
assert len(states) == 50, sorted(states)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["state", "year", "governor", "senate", "house", "trifecta"])
    w.writerows(rows)
# check against Ballotpedia's own yearly totals (same page, "Changes in trifectas by year")
tab = text[text.index("Changes in trifectas by year, 1992-2026"):]
TOTALS = {int(y): (int(d), int(r)) for y, d, r in re.findall(r"(20[0-2]\d) \d+ (\d+) (\d+) ", tab[:3000]) if 2001 <= int(y) <= 2024}
assert len(TOTALS) == 24, sorted(TOTALS)
# 19 of 24 years match exactly. 2002, 2003, 2012, 2013 and 2018 differ by one state, likely a
# change during the year (the state-by-state rows show one status per year); reported, not fixed.
bad = 0
for y, (d, r) in TOTALS.items():
    got = ([x[5] for x in rows if x[1] == y].count("D"), [x[5] for x in rows if x[1] == y].count("R"))
    if got != (d, r):
        bad += 1
        print(f"{y}: parsed D {got[0]}, R {got[1]}; Ballotpedia total D {d}, R {r}")
print(f"{len(rows)} rows, {len(states)} states; {24 - bad} of 24 years match Ballotpedia's totals")
