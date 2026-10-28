# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

Project rule: a suppressed or unpublished value stays missing. Nothing is
filled, interpolated, or estimated by us.

## Quarterly Census of Employment and Wages, QCEW (BLS)

**What it is.** A count of establishments and jobs covered by state
unemployment insurance (and federal UCFE), by county, state and nation, by
industry (NAICS) and ownership. We use the annual average for each state, year,
industry and ownership. Annual average employment is the mean of 12 monthly
job counts. The annual establishment count is the mean of the four quarterly
counts.

**Where it comes from.**
- 2014-2024: `https://data.bls.gov/cew/data/api/<year>/a/industry/<naics>.csv`.
- 2001-2013: `https://data.bls.gov/cew/data/files/<year>/csv/<year>_annual_by_industry.zip`, with only our codes kept.

No login is needed, but BLS wants a browser-like user agent with a contact
address. Raw rows are kept unchanged in `data/raw/qcew/qcew_<year>.csv`.
`scripts/fetch_qcew.py` pulls them and `scripts/clean_qcew.py` tidies them into
`data/clean/qcew.csv`. Pulled 2026-10-28.

**Industries pulled.**

| NAICS | Title | Role |
|---|---|---|
| 621420 | Outpatient Mental Health and Substance Abuse Centers | establishments and workers |
| 621330 | Offices of Mental Health Practitioners (except Physicians) | workers only (added for overcount) |
| 621112 | Offices of Physicians, Mental Health Specialists | workers only (added for overcount) |

Ownership codes: 1 federal, 2 state, 3 local, 5 private.

**Version and vintage.** Annual averages are final once published. BLS can
revise the most recent quarters. We pinned the 2026-10-28 pull.

**Coverage.** A near-census of jobs covered by unemployment insurance. It
leaves out self-employed people, unpaid family workers, and most religious
organizations that opt out of coverage. A counselor in solo practice with no
payroll is not counted. Each establishment is classified by its primary
activity, so a hospital's outpatient addiction clinic is counted under
hospitals, not 621420.

**Changes over time.**
- The files changed format at 2014. Before 2014 the establishment column is
  `annual_avg_estabs_count`; from 2014 it is `annual_avg_estabs`. The API files
  have no `area_title`.
- NAICS revisions (2002, 2007, 2012, 2017, 2022): whether any of them changed
  these three codes is being checked against the Census NAICS manuals.

**Suppressed, censored or masked values.** BLS withholds a cell
(`disclosure_code = N`) when publishing it could identify an employer.
- **Employment:** a withheld cell is written as 0. We set it to missing.
- **Establishments, 2001-2003:** every withheld row also shows 0
  establishments. We read that 0 as withheld and set it to missing.
- **Establishments, 2004 on:** the count is published even when employment is
  withheld. A few withheld rows in 2005, 2006, 2009, 2011, 2014 and 2020 still
  show 0 and are set to missing.
- **Rows that do not exist:** when a state has no establishments of a given
  ownership, BLS publishes no row. We read that as none.

Withheld state rows, 621420, by ownership:

| | Private | State government | Local government |
|---|---|---|---|
| 2001 | 7 of 51 | 4 of 8 | 15 of 21 |
| 2010 | 4 of 51 | 9 of 11 | 13 of 23 |
| 2019-2024 | 0 of 51 | 3 to 7 of 11 to 12 | 7 to 16 of 23 to 24 |

Full year-by-year tables are produced by `scripts/coverage.py`.

How much government employment is hidden: the U.S. total for state plus local
government in 621420 minus the sum of disclosed state cells. It runs from
4,219 workers (2001) to a peak of 16,097 (2009), and is 4,916 in 2024. As a
share of all 621420 workers that is 1.4% to 8.1%, depending on the year.

**State-to-national check.**
- **Employment:** in fully disclosed years, the 51 states sum to the U.S. total
  within ±7 workers. The gap comes from rounding each annual average.
- **Establishments:** the states sum within ±11 from 2004 on. They fall short
  by 235 to 352 in 2001-2003, which is the withheld counts above.
- **Puerto Rico and the Virgin Islands** are not in the U.S. total (adding them
  breaks the match). They are out of scope.

**Missing data.** No missing-value codes other than the above.

**Revisions.** Annual averages are rarely revised after publication.

**Units and rounding.** Establishments and jobs are counts. Annual averages
are rounded to whole numbers.

**Known quirks.**
- **621420 mixes mental health and substance use centers.** It can't be
  split, so it overstates substance-use capacity.
- **Government ownership is large in some states:**

  | State | Year | Government share of disclosed 621420 workers |
  |---|---|---|
  | Georgia | 2001 | 95% |
  | Georgia | 2024 | 57% |
  | North Carolina | 2001 | 85% |
  | Mississippi | 2024 | 82% |
  | South Carolina | 2024 | 73% |
  | Virginia | 2024 | 39% |
  | Connecticut | 2024 | 28% |

  These states run public behavioral health systems through state or local
  agencies. Private-only counts would make them look far worse than they are.
- **Government cells are withheld much more often than private ones.** See
  the table above.

**Uncertainty.** BLS publishes no error measure. QCEW is administrative and
not a sample, so the main errors are classification (which NAICS an employer
is coded to) and coverage (self-employed people are left out).

**License and attribution.** Public domain (U.S. government work). Credit:
U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages.

## NSDUH state small-area estimates (SAMHSA)

In progress.

## N-SSATS / N-SUMHSS (SAMHSA)

In progress.

## OEWS (BLS)

In progress.

## County Business Patterns (Census)

In progress.

## CDC WONDER, Underlying Cause of Death 1999-2020 and 2018-2024 Single Race

**Planned pull.** Drug overdose deaths (X40-X44, X60-X64, X85, Y10-Y14) plus
all alcohol-induced causes (E24.4, F10, G31.2, G62.1, G72.1, I42.6, K29.2,
K70, K85.2, K86.0, R78.0, X45, X65, Y15). Grouped by state of residence and
year, with crude rates per 100,000. Run in Eric's browser. The WONDER API
refuses any query grouped by state.

In progress.
