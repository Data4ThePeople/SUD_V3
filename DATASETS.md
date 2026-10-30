# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

Project rule: a suppressed or unpublished value stays missing. Nothing is
filled, interpolated, or estimated by us.

## Quarterly Census of Employment and Wages, QCEW (BLS)

**Not used on the page.** We pulled and checked QCEW, then set it aside for both
measures. Facilities come from N-SSATS / N-SUMHSS (see that section) and workers
from OEWS (see "Treatment workers and People per Worker"). This section stays as
the record of what we compared.

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
| 621420 | Outpatient Mental Health and Substance Abuse Centers | establishments and workers (compared, not used) |
| 621330 | Offices of Mental Health Practitioners (except Physicians) | workers only (compared, not used) |
| 621112 | Offices of Physicians, Mental Health Specialists | workers only (compared, not used) |

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

**What it is.** SAMHSA's model-based estimates of the share and number of
people aged 12 or older with a past-year substance use disorder (alcohol or
illicit drugs), by state. Each estimate pools 2 survey years (a "window", such
as 2022-2023). Our file is `data/clean/nsduh_sud.csv`: one row per window and
state (51 plus "United States"), with the percent, its 95% interval, the count
in thousands, its 95% interval, the measure name, the DSM edition, and the
source file.

**Where it comes from.** All from SAMHSA, saved unchanged in
`data/raw/nsduh/<window>/` and logged in `data/raw/nsduh/PULLED.txt`. Pulled
2026-10-28 by `scripts/fetch_nsduh.py` (list of files in
`scripts/nsduh_downloads.tsv`). Built by `scripts/build_nsduh_sud.py`, checked
by `scripts/check_nsduh_sud.py`.
- State releases page:
  https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/state-releases
- 2009-2010 to 2023-2024: the published prevalence and totals tables for each
  window (Excel, or HTML for 2009-2010 and the 2010-2011 totals).
- 2000-2001 and 2002-2003 to 2008-2009: those tables are no longer on
  samhsa.gov. We use SAMHSA's 1999-2019 state SAE dataset
  (`NSDUH_99_19_state_saes_final.sas7bdat`), which SAMHSA describes as holding
  "all of the state-level small area estimates, from the earliest (1999-2000) to
  the latest (2018-2019)" and says "does not provide any new information" beyond
  the published tables. Rows used: `OUTCOME = ABODILAL`, `AGEGRP = 0`.
- Cross-check: every window that has a table was compared with SAMHSA's two SAE
  datasets (1999-2019 and 2021-2024). All 1,040 rows match: percents to 2
  decimals, counts exactly.

**Windows.**

| Window | Any-SUD at state level | Measure name (12+) | DSM | Totals published | 95% intervals | Our source |
|---|---|---|---|---|---|---|
| 1999-2000 | No | none | | | | SAE dataset has no ABODILAL for this window |
| 2000-2001 | Yes | Dependence or Abuse of Illicit Drugs or Alcohol in the Past Year | IV | Yes | Yes | SAE dataset |
| 2001-2002 | Never produced | | | | | |
| 2002-2003 to 2008-2009 | Yes | same | IV | Yes | Yes | SAE dataset |
| 2009-2010 | Yes | same (Table B.20 / Table 20) | IV | Yes | Yes | HTML tables |
| 2010-2011 to 2013-2014 | Yes | same (Table 20) | IV | Yes | Yes | Excel (2010-2011 totals HTML) |
| 2014-2015 | No | none | | | | not produced |
| 2015-2016 to 2018-2019 | Yes | Substance Use Disorder in the Past Year (Table 22 or 23) | IV | Yes | Yes | Excel |
| 2019-2020 | Withdrawn | | | | | removed by SAMHSA |
| 2020-2021 | Never produced | | | | | |
| 2021-2022 | Yes | Substance Use Disorder in the Past Year (Table 22) | 5 | Yes | Yes | Excel |
| 2022-2023, 2023-2024 | Yes | same (Table 24) | 5 | Yes | Yes | Excel |

The single-year 2022 and 2024 estimates in the 2021-2024 SAE dataset do not
include any-SUD. The any-SUD estimate in 2023-2024 uses both years; only the
treatment, mental health treatment and "illicit drug use other than marijuana"
measures used 2024 data alone.

Note: the 2015-2019 tables are titled "Substance Use Disorder" but their own
note says SUD "is defined as meeting criteria for illicit drug or alcohol
dependence or abuse. Dependence or abuse is based on definitions found in the
4th edition" (DSM-IV). DSM-5 starts with 2021-2022.

**Why windows are missing (SAMHSA's words).**
- 1999-2000: the SAE dataset documentation lists ABODILAL as "available for
  2000-2001 through 2013-2014".
- 2001-2002: "pooled NSDUH small area estimates were not produced using 2001
  and 2002 combined data because the 2002 data differed from the data from the
  1999 through 2001 surveys." (1999-2019 SAE dataset documentation,
  https://www.datafiles.samhsa.gov/sites/default/files/NSDUH_files/SAE/NSDUH-99-19-State-SAE-Documentation-01-25-21.docx)
- 2014-2015: the 2015 drug module changes "resulted in the need to revise the
  baseline for the following SAE outcomes: illicit drug use in the past month,
  nonmedical use of pain relievers in the past year, illicit drug use disorder,
  and needing but not receiving treatment for illicit drugs." And: "estimates
  for those measures could not be produced using 2014 and 2015 NSDUH data." The
  14 measures produced for 2014-2015 include alcohol use disorder and alcohol
  dependence but no combined SUD measure. The 2014-2015 totals workbook has 15
  tables, none for SUD. (2014-2015 guide, Sections A.6 and B.2,
  https://www.samhsa.gov/data/sites/default/files/NSDUHsaeMethodology2015/NSDUHsaeMethodology2015.htm)
- 2019-2020: "State estimates for these years are no longer available due to
  methodological concerns with combining 2019 and 2020 data." The page says
  further analysis with 2021 data showed the mode effect was not similar across
  groups, "it was determined that averages across the two years maybe
  misleading." (https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/state-releases/2019-2020,
  last updated 2/13/2025)
- 2020-2021: no release is listed. The 2021-2024 SAE dataset documentation
  says the 2020 gap in data collection "made the 2020 data not comparable with
  data from any other year" and "It is anticipated that the 2021-2022 small area
  estimates will become a new baseline."
  (https://www.samhsa.gov/data/sites/default/files/NSDUH_files/SAE/NSDUH-21-24-State-SAE-Documentation.docx)

**Changes over time (breaks in comparability).**
- **2002, NHSDA to NSDUH.** "In 2002, several changes were introduced to the
  survey. Incentive payments of $30 were given to respondents for the first
  time ... Other changes included a change in the survey name (i.e., from NHSDA
  to NSDUH), new data collection quality control procedures, and a shift from
  the 1990 decennial census to the 2000 census ... An unanticipated result of
  these changes was that the prevalence rates for 2002 were in general
  substantially higher than those for 2001 ... and thus are not comparable with
  estimates for 2001 and prior years. Therefore, the 2002 NSDUH was established
  as a new baseline for both the national and the State estimates." Also: "the
  rankings of States for 2002-2003 or later should not be compared with those
  for prior years." (2011-2012 guide, Section A.2,
  https://www.samhsa.gov/data/sites/default/files/NSDUHStateEst2011-2012/Methodology/Web/NSDUHsaeMethodology2012.htm)
  So 2000-2001 does not compare with 2002-2003 on. It was also not benchmarked:
  "for 1999-2000 and 2000-2001, the national estimate included in this dataset
  is a Bayes model-based estimate, not the national design-based estimate."
- **2010 census.** Weights for 2002-2010 used the 2000 census; from 2011 the
  2010 census. SAMHSA produced "2010-2011 published" and "2010-2011 updated"
  estimates; "the updated 2010-2011 estimates were produced only to be compared
  with the published estimates and not to replace them." We use the published
  set, as in the table.
- **2015 questionnaire redesign.** See 2014-2015 above. For 2015-2016 the
  guide says the changes "resulted in the need to revise the baseline using
  2015 and 2016 NSDUH data for several small area estimates showing overall
  illicit drug use (including use disorder and treatment)." The measure was
  renamed from ABODILAL to UDPYILAL. 2013-2014 and earlier do not compare with
  2015-2016 and later. (2015-2016 guide, Section A.6,
  https://www.samhsa.gov/data/sites/default/files/NSDUHsaeMethodology2016/NSDUHsaeMethodology2016.htm)
- **2020 multimode and DSM-5.** Web interviews were added in 2020 and used in
  every year since. SUD from 2021 on uses DSM-5, and "Beginning in 2021,
  NSDUH respondents who reported any use of prescription psychotherapeutic
  drugs ... (i.e., not just misuse of prescription drugs) were asked the
  respective SUD questions." (2021-2022 guide, Section B.11)
- **2021 and later do not compare with 2020 and earlier.** "Methodological
  investigations led to the conclusion that estimates based on multimode data
  collection since 2021 are not comparable with estimates from 2020 or prior
  years ... Thus, the 2021-2022, 2022-2023, and 2023-2024 small area estimates
  should not be compared to state estimates from 2020 and prior years. The
  2023-2024 state estimates are comparable with the 2021-2022 and 2022-2023
  estimates." (2023-2024 guide, Section A.1,
  https://www.samhsa.gov/data/sites/default/files/reports/rpt56959/2024-nsduh-sae-guide-state-meth/2024-nsduh-sae-guide-state-meth.htm)
  The national any-SUD rate goes from 7.41% (2018-2019, DSM-IV) to 17.00%
  (2021-2022, DSM-5). SAMHSA says these two cannot be compared, so the gap
  should not be read as a trend.
- **2021 weights were revised** to a 30% web / 70% in-person mode mix: "These
  adjusted 2021 analysis weights were used to produce the 2021-2022 small area
  estimates." (2021-2022 guide, Section A.7.1,
  https://www.samhsa.gov/data/sites/default/files/reports/rpt44483/2022-nsduh-sae-guide-state-meth/2022-nsduh-sae-guide-state-meth.htm)

Comparable runs: 2002-2003 to 2013-2014 (DSM-IV, 12 windows, with the 2010
census shift inside it); 2015-2016 to 2018-2019 (DSM-IV, 4 windows);
2021-2022 to 2023-2024 (DSM-5, 3 windows). Lines should break between runs.

**How the estimates are made, in plain words.** A state's NSDUH sample is too
small to stand alone, so SAMHSA blends two things: the state's own survey
answers (the direct estimate) and a prediction from a national model that uses
local data such as census, income, unemployment, arrests, deaths and treatment
rates. SAMHSA: "The mixed models produce estimates that are approximately
represented by a weighted combination of the direct estimate from the state data
and a regression estimate from the national model ... the weights are obtained
by minimizing the MSE (variance + squared bias)." States with large samples
lean more on their own data: the estimates "for states with large sample sizes
are close to the robust design-based estimates." Pooling 2 years means "the
impact of the national model on those States has been reduced significantly
relative to estimates based on a single year's data." The state estimates are
then shifted so their population-weighted average equals the national survey
estimate ("benchmarking", since 2002).

SAMHSA does not publish how much of each state's estimate comes from the model
and how much from its own sample. What we can show is sample size: in
2023-2024 the pooled 12+ sample ran from 1,520 completed interviews (Wyoming)
to 9,080 (California), median 2,080 (`NCOMP` in the SAE dataset). By SAMHSA's
description, the states with the smallest samples rely most on the model.

**Trap for this project.** The list of possible model predictors includes
county "Alcohol and Drug Treatment Rate" and "Drug Treatment Rate" from
N-SUMHSS (earlier N-SSATS), SAMHSA's treatment facility survey (2023-2024
guide, Section B.3). If a predictor like that was chosen for the SUD model,
the demand estimate is partly built from supply data. SAMHSA does not say
which predictors were picked for which measure. Not confirmed either way.

**Version and vintage.** Pinned to the 2026-10-28 pull. The 2021-2024 SAE
dataset documentation is dated February 2026.

**Revisions.** SAMHSA does not routinely re-release old windows, but it has
changed them:
- Data errors for Pennsylvania (2006-2010) and Maryland (2008-2009) led SAMHSA
  to update the 2005-2006, 2006-2007, 2007-2008 and 2008-2009 state estimates
  "and NSDUH tables on the Web were replaced." Because the model uses all
  states, "the model-based estimates in all States changed." The 2009-2010
  tables carry "Revised March 2012." (2011-2012 guide, Section A.7)
- 2019-2020 was published and later removed.
- 2010-2011 has a second ("updated") set that did not replace the published one.

**Units and rounding.** Percents are stored at different precision depending
on the source: 4 decimal places for 2000-2001 to 2008-2009 (SAE dataset), 2
for 2009-2010 (HTML), 8 for 2010-2011 to 2013-2014, and full precision from
2015-2016 on (Excel stores the unrounded proportion; we multiplied by 100 and
did not round). Counts are in thousands, rounded by SAMHSA. SAMHSA computes a
count as the unrounded rate times the state's population averaged over the 2
years, then rounds; multiplying a published rate by a published population may
not match exactly.

**State-to-national check.** SAMHSA: "Estimated numbers in the 'Total U.S.' row
are aggregates of estimated numbers across all states." The 51 state counts sum
to the national count within 5 thousand in every window (differences: -4 to
+5), which is rounding. The national percent and its interval are a direct
survey estimate, not a model estimate (except 2000-2001).

**Uncertainty.** Every state number has a 95% Bayesian interval. SAMHSA:
"These intervals indicate the uncertainty in the estimate due to both sampling
variability and model fit." Also: "When it is indicated that a state has the
highest or lowest estimate, it does not imply that the state's estimate is
significantly higher or lower than the next highest or lowest state's
estimate. Additionally, two significantly different state estimates ... may
have overlapping 95 percent confidence intervals." SAMHSA publishes p-value
tables for state-to-state and window-to-window tests; overlap of intervals is
not the test. Do not subtract one modeled measure from another at state level:
it "can give misleading results, perhaps even a 'negative' estimate."

**Coverage.** Household population aged 12 or older. Not included:
"individuals with no fixed household address (e.g., people experiencing
homelessness and not in shelters), military personnel on active duty, and
residents of institutional group quarters, such as jails and hospitals." Response rates are low and falling: overall weighted response rate
11.79% in 2023-2024.

**Known quirks.**
- On the "older" releases page, the "2013-2014 State Estimates" link points
  to the 2012-2013 page. The 2013-2014 page exists at
  https://www.samhsa.gov/data/report/2013-2014-nsduh-state-estimates-substance-use-and-mental-disorders.
- Windows overlap by a year, so neighboring windows share half their data.

**License and attribution.** Public domain (U.S. government work). Credit:
Substance Abuse and Mental Health Services Administration, National Survey on
Drug Use and Health, state small area estimates.

### Drug use disorder and alcohol use disorder ("Drug only" and "Alcohol only" views)

`scripts/build_nsduh_parts.py` writes `data/clean/nsduh_drug.csv` and
`nsduh_alcohol.csv` from SAMHSA's state SAE SAS datasets, ages 12+:

| Windows | SAMHSA outcome | Measure |
|---|---|---|
| Drug, 2000-2001 to 2013-2014 | ABODILL | Illicit drug dependence or abuse (DSM-IV) |
| Drug, 2015-2016 to 2018-2019 | UDPYILL | Illicit drug use disorder (DSM-IV) |
| Drug, 2021-2022 to 2023-2024 | UD5ILANY | Drug use disorder (DSM-5) |
| Alcohol, 2000-2001 to 2014-2015 | ABODALC | Alcohol dependence or abuse (DSM-IV) |
| Alcohol, 2015-2016 to 2018-2019 | ABODALC | Alcohol use disorder (DSM-IV; SAMHSA's table title) |
| Alcohol, 2021-2022 to 2023-2024 | UDYR5ALC | Alcohol use disorder (DSM-5) |

- **Alcohol has 21 windows, and drug has 20.** SAMHSA published alcohol for
  2014-2015 but not drug or any SUD, so the alcohol view has a 2015 value.
  SAMHSA's 2014-2015 guide (section A.6) says the 2015 questionnaire change "did
  not affect estimates for alcohol use or alcohol use disorder," so the alcohol
  trend line is drawn across 2015. It still breaks at 2002 and at the 2021
  redesign.
- **2010-2011:** the "(published)" estimates are used, the same as for any SUD.
- **Check against published tables:** for both measures, the script checks
  every window that has a published Excel table, percents to 2 decimals and
  counts exactly. There are 10 such windows (counts only for 2011-2012), with
  0 differences.
- **State-to-national check:** state counts sum to the national count within
  ±5 thousand in every window (`validate_sums.py`).
- **Overlap:** people can have both disorders. Each estimate includes people
  who also have the other disorder. Drug plus alcohol is more than any SUD in
  every state and window, so nothing is added or subtracted.
- **Color scales:** each view has its own fixed scale so that differences
  between states show.
  - Drug: 1-5% through 2019 and 6-16% from 2022.
  - Alcohol: 3-11% through 2019 and 7-17% from 2022.
  - Any SUD: 4-14% and 10-32%.
- **The drug measure changed in 2021-2022 beyond DSM-5.** SAMHSA's 2022 table
  notes say prescription drug use disorder questions were asked of everyone who
  used prescription drugs in the past year, whether or not they misused them.
  The earlier measures covered misuse only.
- **People per Worker always uses any SUD.**

### Tests of change ("Change" view)

`scripts/build_nsduh_change.py` writes `data/clean/nsduh_change.csv` from SAMHSA's own
change tables in `data/raw/nsduh_change/` (URLs in `PULLED.txt`), ages 12+:

| Comparison | Table | Measure |
|---|---|---|
| 2008-2009 vs 2018-2019 | Long-term change tables, Table 9 | Alcohol use disorder |
| 2022-2023 vs 2023-2024 | 2024 change tables, Table 21 | Substance use disorder (DSM-5) |
| 2022-2023 vs 2023-2024 | 2024 change tables, Table 22 | Alcohol use disorder (DSM-5) |
| 2022-2023 vs 2023-2024 | 2024 change tables, Table 24 | Drug use disorder (DSM-5) |

- **Significance:** SAMHSA marks a difference significant at the 0.05 level with "a"
  and at the 0.10 level with "b". The page uses 0.05 only (Eric, 2026-10-28). A state
  is "increased" or "decreased" only with an "a" marker; the script checks that the
  printed p value is below 0.05 whenever the marker is present. Everything else is "no
  significant change". Nothing is tested or computed by us.
- **p values** are shown as SAMHSA prints them, to 3 decimals. SAMHSA's notes to Tables 21,
  22 and 24 say a p value printed as 0.000 means p < 0.001; the page shows these as "p < 0.001".
- **What SAMHSA does not publish:** no test across the 2021 redesign, no test of
  2021-2022 vs 2023-2024, and no long-term test for drug use disorder or any SUD. The
  two 2022-2024 windows share 2023.
- **Check:** the estimates in the change tables match our level estimates for the same
  windows within 0.005 points in all 208 rows (`tieout.py`).
- **Death rate change, 2019 to 2024:** the page computes (2024 rate - 2019 rate) / 2019
  rate x 100 from CDC's published crude rates for the selected deaths (drug + alcohol,
  drug only, alcohol only). A state with no printed rate in either year has no value.
  The color scale runs from -60% to +60%; values beyond are drawn at the end color.

## N-SSATS (2000-2020) / N-SUMHSS (2021-2024) (SAMHSA)

**What it is.** An annual survey of every known substance use treatment
facility. Each record is one facility, which can be a program, a clinic or a
multi-site respondent. We count facilities that offer outpatient substance
use care, by state.

**Where it comes from.** Public-use files and codebooks,
https://www.samhsa.gov/data/data-we-collect/n-sumhss-national-substance-use-and-mental-health-services-survey/datafiles.
The URLs are listed in `data/raw/nssats/PULLED.txt`. The files themselves
are not in git because of their size. `scripts/build_nsumhss.py` builds
`data/clean/nsumhss_outpatient.csv`.

**Definition used.**
- **Outpatient:** `CTYPE1 == 1`, "offers OUTPATIENT substance abuse services."
  Not `CTYPEOP`: despite the name, that variable means day treatment or
  partial hospitalization only.
- **Which facilities count, 2021 on:** the substance-use report universe,
  `TSU21_SU == 1` in 2021 or `TSU_SU == 1` from 2022.
- **Which facilities count, 2000-2020:** every record in the file.

**Coverage.**
- 2000 and 2002-2024. **No survey in 2001.**
- The reference date is the end of March, except 2000 (October 1).
- **Response rates:** 89% to 97% through 2020. For substance-use facilities:
  77.1% in 2021, 86.8% in 2022, 83.8% in 2023 and 90.1% in 2024. The overall
  2021 rate across all facilities was 78.83%. The page uses the substance-use
  rates.
- **Nonrespondents are not counted and nothing is imputed for them**, so every
  count is a floor.
- Out of scope: halfway houses that offer no treatment, solo practices the state
  has not approved, and jail-only programs.
- Every ownership type is included (`OWNERSHP`): private for-profit, private
  nonprofit, state, local, tribal and federal.
- Opioid treatment programs are flagged from 2002 on.
- **No staff counts in any year.**

**Changes over time.** In 2021 this survey merged with the mental health
facility survey (N-MHSS). The new file covers mental-health-only facilities,
closed facilities and nonrespondents; the substance-use flag removes them.

Facilities that were on the mental health list only and said yes to both
substance-use treatment and outpatient care are left out of SAMHSA's
substance-use report. That was about 2,414 facilities in 2021, 1,703 in 2022,
50 in 2023 and 38 in 2024. They are kept in a separate column so they can be
checked.

The response rate also fell in 2021. **Treat 2021 as a series break.**

**Suppressed values.** None. The files are facility records.

**State-to-national check.**
- **2000-2020:** state counts match the published report tables exactly in
  every year checked (2011, 2013, 2015, 2017, 2019, 2020).
- **2024:** total facilities match in all 51 states. The outpatient count is
  13,309, which is 19 below the published 13,328. Twelve states are off by 1 to
  4. **This gap is not yet explained.**
- The 50 states plus DC fall 26 to 72 short of the whole-file total. The
  difference is Puerto Rico and the other territories.

**Uncertainty.** Counts depend on facilities responding. SAMHSA publishes
no error measure.

**License.** Public domain. Credit: Substance Abuse and Mental Health Services
Administration, N-SSATS and N-SUMHSS.

## OEWS (BLS)

**What it is.** A semiannual survey of employers, estimating jobs by
occupation and state. Each estimate pools six panels collected over three
years. We use it as a cross-check only.

**Where it comes from.** `https://www.bls.gov/oes/special-requests/`
(`oes01st.zip`, `oesmYYst.zip`). `scripts/build_oews.py` builds
`data/clean/oews_counselors.csv`.

**Changes over time.**
- **21-1011 (substance abuse counselors)** and **21-1014 (mental health
  counselors)** are separate through 2016.
- **From May 2017** they are combined into 21-1018, a code that exists only in
  OEWS, because "the survey does not have the information needed to
  distinguish between the occupations" (BLS, 2017 changes notice).
- **21-1023 (mental health and substance abuse social workers)** runs in
  every year.
- The 2001 estimates use a fourth-quarter (October to December) payroll. The
  2002 estimates pool the 1999-2001 annual samples with a November 2002 panel.
  From 2003 the reference month is May, and each estimate pools six panels
  over three years.

**Limits.** OEWS leaves out the self-employed. At the state level it can't
be split by industry or ownership, so its counts include hospitals,
residential programs, schools and prisons. BLS "does not encourage the use of
OEWS data for time-series analysis."

**Suppressed values.** `**` means the estimate is not available: 43 cells in
2001-2020. In 11 state-code-years the occupation has no row at all.

**Code history check.** We compared the BLS SOC crosswalks (saved in
`data/raw/oews/docs/`). 21-1011, 21-1014 and 21-1023 carry over one to one from
SOC 2000 to SOC 2010 to SOC 2018. 21-1018 is the sum of 21-1011 and 21-1014.
Other points to note:
- 2010-2011 and 2019-2020 are "hybrid" years, when BLS was moving between
  SOC versions. The codes we use did not change in those years.
- From May 2021, BLS changed its estimation method (MB3).
- The national total of the three codes moves smoothly across each of these
  points.

**Job mix inside the QCEW codes (national only; background, not on the page).** OEWS also publishes national
estimates by industry (`data/raw/oews_industry/`, built by
`scripts/build_oews_industry.py` and summarized by `scripts/oews_mix_summary.py`
into `data/build/oews_mix_summary.csv`). They cover 621420 and 621330, not
621112. These estimates are within 2% of QCEW private employment in every year,
2002-2024, so they describe the same private workers. In 2024:
- Counselors and mental health and substance abuse social workers (the Version
  1 codes) were 34% of jobs in 621420 and 35% in 621330.
- The rest were other community and social service jobs (15%), office and
  administrative support (14%), healthcare practitioners such as nurses and
  psychiatrists (14%), management (7%), psychologists (7%), healthcare support
  (3%), and all other jobs (6%), across the two codes combined.
- The 192,300 Version 1 clinicians in these two codes were 34% of all 566,290
  Version 1 clinicians in OEWS. The rest work in other settings.
- In 621330, Version 1 clinicians grew from 13,310 in 2010 to 85,640 in 2024,
  and their share of jobs there went from 21% to 35%.
Some groups are withheld in a few years (psychologists in 2009, 2010, 2013, 2021 and
2022 in one code or the other); those cells are left blank.

**State-to-national check.** Where nothing is withheld, state sums are within
±40 of the national figure.

## Treatment workers and People per Worker (decision 2026-10-28)

People per Worker = SAMHSA's count of people with SUD ÷ treatment workers.

**Treatment workers on the page are OEWS counselors and social workers.**
Substance abuse and mental health counselors (21-1011 + 21-1014 through 2016;
21-1018 from 2017) plus mental health and substance abuse social workers
(21-1023), in all settings and ownerships. A state-year has a value only when
every part is published. 1,173 of 1,224 state-years have a value, and every
year from 2022 on is complete. The 2020|2021 BLS method change is marked on the
worker trend line.

**Compared and set aside: QCEW private outpatient workers.** Private employment
in NAICS 621420 + 621330 + 621112, hatched where part of the private count was
withheld (100 state-years) or government workers were 20% or more of the
disclosed total (56 state-years). The OEWS job mix above shows that about a
third of the jobs in 621420 and 621330 are counselors and social workers. This
version is in git history at commit ad2d027.

QCEW columns stay in `data/build/panel.csv` for reference. They are not shown on
the page.

## County Business Patterns (Census)

**Not used on the page.** CBP was pulled only to support QCEW, which the page no
longer uses.

**What it is.** An annual count of establishments and employment by
industry and state, for the pay period that includes March 12. It leaves out
most government employers and the self-employed. Used only to tell a
suppressed QCEW cell from a true zero.

**Where it comes from.** `https://www2.census.gov/programs-surveys/cbp/datasets/`.
`scripts/build_cbp.py` builds `data/clean/cbp_621420.csv`. 2024 is not yet
published.

**Suppressed values.** Establishment counts are never withheld. Employment
is withheld in 46 state-years, all between 2001 and 2014. Data are noise
infused from 2007; that method is under review after a Commerce order.

**State-to-national check.** State establishments equal the U.S. total in
every year.

## NAICS index (Census)

- **621420's index entries are the same in 2002, 2007, 2012, 2017 and 2022.**
  They cover outpatient alcoholism, drug addiction, detox, substance abuse and
  mental health centers and clinics, except hospitals.
- **621420, 621330 and 621112** keep the same definitions, and every
  concordance maps each one to itself (2002 through 2022).
- **No edition has an index entry for methadone clinics, opioid treatment
  programs or medication-assisted treatment.** Placing them in 621420 is an
  inference from "drug addiction treatment centers... outpatient."
- Residential substance abuse programs are 623220. Detox hospitals are 622210.
- Nonresidential alcoholism counseling that is not medical treatment is
  624190, which we leave out.

Files: `data/raw/naics/`.

## CDC WONDER, Underlying Cause of Death 1999-2020 and 2018-2024 Single Race

**What it is.** Deaths of U.S. residents by state of residence and year,
from death certificates. We count deaths whose underlying cause is one of:
- **Drug overdose:** X40-X44 (unintentional), X60-X64 (suicide), X85 (assault)
  or Y10-Y14 (undetermined intent).
- **Alcohol-induced causes:** E24.4, F10, G31.2, G62.1, G72.1, I42.6, K29.2,
  K70, K85.2, K86.0, R78.0, X45, X65, Y15. Most of these are chronic causes
  such as alcoholic liver disease, not poisonings.

Each death has one underlying cause, so the two groups never overlap. Drug
plus alcohol equals the combined total in all 1,224 state-years.

**Where it comes from.**
- Ten exports, run by hand by Eric in the WONDER web tool on 2026-10-28:
  combined, drug only and alcohol only by state and year, plus combined by year
  (national), plus combined by state, year and cause, each from both
  databases.
- The WONDER API refuses any query grouped by state.
- Files are in `data/raw/wonder/`, with WONDER's query settings and notes at
  the bottom of each. `scripts/clean_wonder.py` builds `data/clean/wonder.csv`.

**Version and vintage.**
- **1999-2020 database:** released 2021, bridged-race population.
- **2018-2024 Single Race database:** released 2026.
- We use the first for 2001-2017 and the second for 2018-2024. In 2018-2020
  the two agree exactly on deaths and population for every state; this is
  checked on every build.

**Population (the rate denominator).** WONDER's own:
- 2001-2009: intercensal estimates.
- 2010: the April 1 census count.
- 2011-2020: postcensal estimates, a new vintage each year.
- 2021-2024: single-race estimates built on the 2020 Blended Base.

Vintages change from year to year, so the denominators are not one
consistent series.

**What alcohol-induced leaves out.** CDC's NCHS definition (the codes listed
above) "exclude[s] unintentional injuries, homicides, and other causes
indirectly related to alcohol use" (NCHS Data Brief 448). Color scales on the death map: 0-70 combined, 0-50
drug only, 0-25 alcohol only.

**Rates.** Crude rate per 100,000, as published, with no age adjustment.
States with older populations have higher alcohol-induced rates partly for
that reason.

**Suppressed values.** WONDER suppresses counts of 1 to 9. In the 1999-2020
database it marks rates based on fewer than 20 deaths as unreliable and does
not print them. North Dakota 2013, with exactly 20 drug deaths, has a printed
rate. That database's export caveat says "20 or less", but its help page and
the data say fewer than 20. Since February 2026 the 2018-2024 database flags a
rate when the width of its 95% confidence interval is more than 160% of the
rate. No 2018-2024 cell in our data is flagged.
- **None** of the combined, drug-only or alcohol-only state-year cells are
  suppressed.
- **Six drug-only rates** (North Dakota in 2001, 2002, 2004, 2005, 2006 and
  2011) are flagged unreliable. Those rates are left blank, as WONDER leaves
  them.
- In the by-cause files many single-cause cells are suppressed (for example
  202 state-years for X85). We use those files for nothing that needs a total.
  We never subtract to recover a suppressed value.

**State-to-national check.** The 51 states equal the national figure exactly
for deaths and population in all 24 years.

**Known quirks (CDC's own notes).**
- **North Carolina 2023:** more than 900 death certificates were recoded to
  overdose after the file closed. CDC puts the real 2023 overdose count above
  4,400 and says the final file will not be updated.
- **R99 ("ill-defined causes") excess** in California (2000-2001), Georgia
  (2008-2009) and New Jersey (2009) lowers counts in other codes. CDC names
  unintentional poisoning for New Jersey.
- 125 deaths in 2014 had their underlying cause revised in 2017.

**License.** Public domain. Citation: Centers for Disease Control and
Prevention, National Center for Health Statistics, National Vital Statistics
System, Mortality 1999-2020 and 2018-2024 on CDC WONDER Online Database.
