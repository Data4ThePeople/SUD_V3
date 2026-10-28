# Tie-out

## Claude's tie-out (2026-10-28)

`scripts/tieout.py` recomputes each value the dashboard shows and compares it with
`data/build/dashboard.json`:
- deaths come from the raw CDC exports, by a code path separate from `build.py`;
- workers (OEWS counselors and social workers) come from the clean OEWS file, which
  `build_oews.py` reads from the unchanged BLS zips;
- SUD values come from the NSDUH clean file, which `check_nsduh_sud.py` ties to SAMHSA's
  SAS datasets;
- facility counts come from the N-SSATS / N-SUMHSS clean file, which `check_nsumhss.py`
  ties to SAMHSA's published tables.

**Result (OEWS workers, 2026-10-28): 14,093 values checked, 0 mismatches.** Every metric
array has 24 years, and all 52 geographies are present.

`scripts/validate_sums.py` checks that the states add up to the national figure:

| Source | Result |
|---|---|
| NSDUH | 20 of 20 windows pass, within ±5 thousand |
| QCEW | every fully disclosed year passes (employment within ±7, establishments within ±11); partial years are listed |
| WONDER | deaths and population match exactly in all 24 years |

The page computes two values in the browser: establishments per 100K
(facilities ÷ population × 100,000) and People per Worker (SUD count ÷ workers).
`build.py` computes both with the same formulas into `panel.csv`.

`scripts/coverage.py` reports, for each year, how many states have each value
measured, withheld, or missing.

## Words on the page

| Claim on the page | Source | Status |
|---|---|---|
| No state estimates for windows ending 2002, 2015, 2020, 2021 | NSDUH SAE dataset and guides (DATASETS.md, NSDUH section) | Supported |
| SAMHSA withdrew 2019-2020 state estimates and published none for 2020-2021 | SAMHSA "older releases" text quoted in DATASETS.md | Supported |
| Estimates from 2021 on are not comparable with 2020 and earlier | 2023-2024 SAE guide, A.1 | Supported |
| 2001 (NHSDA) not comparable to 2003 and later | 2011-2012 SAE guide, A.2 | Supported |
| National 7.4% (2018-2019) and 17.0% (2021-2022) | Computed from the data at render time | Supported |
| Each window shown at its second year | Method choice, stated on the page | Supported (our convention) |
| Facility survey merged with the mental health facility survey in 2021 | N-SUMHSS 2021 codebook | Supported |
| Nonresponse 3% to 11% (2000-2020), 10% to 23% (2021-2024) | Response rates in DATASETS.md, N-SSATS section | Supported |
| NC 2023: over 900 overdose deaths recoded after the file closed | CDC WONDER export caveat | Supported |
| R99 anomalies in CA 2001, GA 2008-2009, NJ 2009 | CDC WONDER export caveats | Supported. CA's note covers 2000-2001; only 2001 is in our range |
| 2018-2020 databases agree exactly | `clean_wonder.py` check on every build | Supported |
| Worker count leaves out the self-employed and programs inside hospitals | QCEW scope; NAICS assigns by primary activity | Supported |
| Worker count leaves out federal facilities such as the VA | Ownership code 1 is excluded by design | Supported |
| NSDUH leaves out people in institutions and people experiencing homelessness who are not in shelters | NSDUH target population (civilian, noninstitutionalized) | Partly supported. The institutions part is in our files; the shelters wording has not been checked against a saved SAMHSA document |
| 988: call or text, free, confidential, 24/7 | 988lifeline.org: "Call, text, or chat... available 24/7/365. Your conversations are free and confidential." | Supported |
| FindTreatment.gov is SAMHSA's locator; enter a ZIP code | Eric's instruction; the site loads by script, so it could not be fetched. "Free and confidential" was removed because it could not be checked | Partly supported |

## Independent tie-out (fresh agent, 2026-10-28)

A fresh agent got the sources, `DATASETS.md`, and `dist/index.html`, but not our numbers
or code. It pulled QCEW, NSDUH, and N-SSATS/N-SUMHSS again from the publishers and
recomputed everything with its own scripts, which are in `tieout_independent/`. For CDC
WONDER it used Eric's raw exports, because the API refuses queries by state.

**Numbers: no differences.**

| Source | Values compared | Differences |
|---|---|---|
| WONDER | 11,136 | 0 |
| NSDUH | 7,488 | 0 beyond the 2-decimal rounding of the 2009-2010 window |
| QCEW | 9,984 (all 24 years) | 0 |
| Facilities | 561 (11 of 23 survey years) | 0 |
| Derived ratios | 2,496 | 0 |

**Words: fixed in response.**
- The hatched-states callout printed "0 states" in years with no SUD estimate. It now
  counts withheld worker cells directly, and it says so when no ratio can be computed.
- The R99 note now matches CDC's wording. Only New Jersey's note says other counts were
  lowered.
- "Not fully comparable" on the facility survey was our own inference. The page now
  states what happened instead.
- The demand source wording now names SAMHSA's small area estimation dataset for
  2000-2001 through 2008-2009.
- A method note now explains that each ratio divides a two-year SUD count by the worker
  count for the window's second year.
- The 2021 response rate in DATASETS.md now gives the substance-use basis (77.1%) that
  the page uses, and the overall rate (78.83%).

**Words that need Eric's decision (his text):** subtitle items 3, 4, and 5 in the agent's
table. They go to Eric as numbered proposals.

## Independent tie-out of OEWS workers (fresh agent, 2026-10-28)

A second fresh agent downloaded the 48 BLS OEWS zips itself and rebuilt the worker count and
People per Worker. Full report: `tieout_independent/oews/REPORT.md`.

**Numbers: no differences.** 1,248 geo-years blank vs not blank, 1,197 worker values, 996
People per Worker values, 1,173 state sampling-error notes: 0 differences.

**Fixed in response.**
- The US sampling-error note was blank. The build now reads the national PRSE, and the
  values match the agent's in all 24 years.
- "November for 2001-2002" is now stated as BLS describes it: fourth-quarter payrolls for
  2001, a November 2002 panel added for 2002, May from 2003.
- "Six panels over three years" now applies from 2003 on.
- "Small states can move a lot ... because of sampling alone" was our inference and is
  removed.

**Could not check:** BLS pages for the 2001 technical notes, the 2017 changes notice, and the
SOC 2010 and MB3 notes returned not-found. The same claims were confirmed from the FAQ and
the May 2017 technical note.

**Not checked by either tie-out:** facility years 2005-2011 and 2014-2018, which the
independent agent did not rebuild (the main tie-out covers every year), and SAMHSA's
published 2024 outpatient total of 13,328, which is 19 above our count. That gap is
still unexplained.
