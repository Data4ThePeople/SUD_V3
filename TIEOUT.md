# Tie-out

## Claude's tie-out (2026-10-28)

`scripts/tieout.py` recomputes each value the dashboard shows and compares it with
`data/build/dashboard.json`:
- workers come straight from the raw BLS rows, and deaths from the raw CDC exports,
  each by a code path separate from `build.py`;
- SUD values come from the NSDUH clean file, which `check_nsduh_sud.py` ties to SAMHSA's
  SAS datasets;
- facility counts come from the N-SSATS / N-SUMHSS clean file, which `check_nsumhss.py`
  ties to SAMHSA's published tables.

**Result: 16,589 values checked, 0 mismatches.** Every metric array has 24 years, and all
52 geographies are present.

`scripts/validate_sums.py` checks that the states add up to the national figure:

| Source | Result |
|---|---|
| NSDUH | 20 of 20 windows pass, within ±5 thousand |
| QCEW | every fully disclosed year passes (employment within ±7, establishments within ±11); partial years are listed |
| WONDER | deaths and population match exactly in all 24 years |

The page computes two values in the browser: establishments per 100K
(facilities ÷ population × 100,000) and the Gap Score (SUD count ÷ workers).
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
