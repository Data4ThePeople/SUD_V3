# Independent tie-out: OEWS treatment workers and People per Worker (2026-10-28)

Run by a fresh agent with the page (`dist/index.html`), `DATASETS.md`, and its own downloads
of 48 BLS zips (`oes01st`/`oes01nat` through `oesm24st`/`oesm24nat`). It did not read
`scripts/`, `data/clean/`, `data/build/`, `data/raw/oews/`, `TIEOUT.md`, `STATUS.md` or git
history. Scripts: `fetch.py`, `fetch_docs.py`, `build.py`, `compare.py`, `grepdocs.py`,
`xwalk.py`. Outputs: `oews_rows.csv`, `diffs.csv`, `compare_output.txt`. Raw zips and saved
BLS pages are in `tieout_independent/raw_oews/` (gitignored).

## 1. Workers (50 states + DC + US, 2001-2024)

| Check | Compared | Differences |
|---|---|---|
| Blank vs not blank | 1,248 geo-years | 0 |
| Worker value (tolerance 0.5) | 1,197 | 0 |
| `workers_note` (largest EMP_PRSE among parts), states | 1,173 | 0 |
| `workers_note`, US | 24 | 24 (blank on the page) |
| `workers_flag` set | 1,248 | 0 (none set) |

- 1,173 of 1,224 state-years have a value and 51 are blank, as DATASETS.md says.
- 43 `**` cells, all in 2001-2020. 11 state-code-years have no row: AK 2007, NJ 2003, NJ
  2008, ND 2008, ND 2009, RI 2004, SC 2002, SC 2003, SC 2013, VT 2009, WA 2005.
- 2021-2024 are complete. The last blank state-year is DC 2020.
- US matches in all 24 years, from 219,720 in 2001 to 566,290 in 2024.

## 2. People per Worker

996 geo-years have a value on both sides, with 0 differences. Blank vs not blank: 0
differences. Each worker year is paired with the NSDUH window ending that year.

## 3. Page wording

Confirmed from saved BLS pages: the 2017 21-1018 combination; all settings and ownerships
(state files are cross-industry, own_code 1235); the self-employed are excluded; BLS's
time-series caution; the SOC 2000→2010 and 2010→2018 crosswalks map 21-1011, 21-1014 and
21-1023 one to one; hybrid years May 2010-2011 and May 2019-2020; MB3 from May 2021; the
"BLS method change" mark at 2020.5; the workers card text and the blank rule.

Partly confirmed: "November" for 2001-2002. BLS says the 2001 survey used a fourth-quarter
(October to December) payroll, and the 2002 estimates pool the 1999-2001 annual samples
with a November 2002 panel. "Six panels over three years" holds from 2003 on.

Not a BLS statement: "small states can move a lot from one year to the next because of
sampling alone."

## Could not check

BLS returned not-found pages for the 2001 technical notes, the 2017 changes notice (the same
wording is in the May 2017 technical note), and the SOC 2010 and MB3 pages (the FAQ covers
both claims).
