# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

Project rule: a suppressed or unpublished value stays missing. Nothing is
filled, interpolated, or estimated by us.

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
- **People with SUD per Worker always uses any SUD.**

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

**State-to-national check.** Where nothing is withheld, state sums are within
±40 of the national figure.

## Treatment workers and People with SUD per Worker (decision 2026-10-28)

People with SUD per Worker = SAMHSA's count of people with SUD ÷ treatment workers.

**Treatment workers on the page are OEWS counselors and social workers.**
Substance abuse and mental health counselors (21-1011 + 21-1014 through 2016;
21-1018 from 2017) plus mental health and substance abuse social workers
(21-1023), in all settings and ownerships. A state-year has a value only when
every part is published. 1,173 of 1,224 state-years have a value, and every
year from 2022 on is complete. The 2020|2021 BLS method change is marked on the
worker trend line.

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

## Alcohol data for thought: national trend (added 2026-11-12)

Two charts for a short post on whether drinking is getting more deadly. Built by
`scripts/alcohol/build_series.py` (writes `data/build/alcohol/deaths_national.csv`
and `nsduh_national.csv`) and `scripts/alcohol/make_charts.py` (writes
`dist/alcohol/01-alcohol-death-rate.png` and `02-alcohol-change.png`).

**Deaths: alcohol-induced, underlying cause, U.S., 1999-2024.** Same 14 ICD-10
codes as the map (see the CDC WONDER section).
- 1999-2020: crude and age-adjusted rates as CDC publishes them, from the D76
  API pull `data/raw/wonder_api/aar.xml` (Year x Drug/Alcohol Induced).
- 2021-2024: D158 (2018-2024, single race) has no API access, so the
  age-adjusted rate is computed by us from Eric's export
  `data/raw/wonder/mcd_2018_2024_year_age_alcohol.csv` (UCD alcohol-induced,
  by year and ten-year age group). Method: direct age adjustment with the 2000
  U.S. standard population in CDC's 11 age groups (under 1, 1-4, 5-14, 15-24,
  ..., 85+). Deaths with age not stated are left out, as CDC does.
  Crude rate = deaths / population x 100,000.
- Suppressed cells (1-9 deaths, ages under 15 only) are counted as 0. If each
  were 9, the age-adjusted rate would rise by at most 0.003 per 100,000.
- Check: the same method applied to D76 age groups reproduces CDC's published
  age-adjusted rate within 0.06 per 100,000 in every year 1999-2020. D158
  2018-2020 computed rates match D76 within 0.05.
- Alcohol-induced deaths do not include drunk-driving crashes, falls or other
  injuries where alcohol played a part.

**Drinking and disorder: NSDUH state SAE datasets, national rows, ages 12+.**
- Past-month alcohol use: `ALCMON`, both SAE datasets.
- Alcohol use disorder: `ABODALC` (DSM-IV) through 2018-2019; `UDYR5ALC`
  (DSM-5) from 2021-2022.
- Two-year windows only, 2002-2003 on; 2010-2011 uses the "(published)" set.
  The same breaks as the map apply: 2002 baseline, and 2021-2022 on does not
  compare with 2020 and earlier.
- Binge drinking is not charted: the definition for women changed in 2015
  (and the outcome code changed), so the series breaks there.

**Chart 2 percent changes** compare the 2002-2003 window with 2018-2019, the
longest span the survey allows. The death rate is averaged over the same two
calendar years (2002 and 2003; 2018 and 2019) to match.
