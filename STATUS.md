# Status

Project: SUD_V3 (Substance Use Treatment, State by State, 2001-2024)
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: none yet
Step: 1
Since: 2026-10-28

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | | |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Story leads

### 1. Fewer people with an alcohol disorder, more alcohol deaths (raised by Eric, 2026-10-29)

**What our data shows (same years, same states):**
- 2008-2009 to 2018-2019, alcohol use disorder (DSM-IV, 12+): the point estimate fell in all 51
  states; SAMHSA's test finds 37 significant decreases, 0 increases. US 7.42% to 5.34%.
- 2009 to 2019, alcohol-induced death rate (crude): rose in 50 of 51 states. US 8.0 to 11.9 per 100K.
- Not the same pattern for drugs: 2016 to 2019, drug disorder and overdose death rates both rose in
  most states. In 2022-2024 both alcohol measures and overdose deaths fell in most states. The Change
  view's 2019-2024 deaths vs 2022-2024 disorders compares different years, so it is not this lead.

**Age looks like the main thread (SAMHSA SAE dataset, national, point estimates, not tested):**
- 12-17: 4.8% to 1.6%. 18-25: 16.8% to 9.7%. 26+: 6.2% to 5.1%.
- Of the 4.0M drop in people with AUD, 2.3M was ages 18-25 and 0.8M ages 12-17; 26+ fell 0.9M.
- By state: AUD fell in all 51 states for 12-17 and 18-25, and in 47 for 26+.
- Alcohol-induced deaths are mostly chronic causes (alcoholic liver disease leads) and peak at ages
  55-64 (NCHS Data Brief 448). So the people whose disorder rates fell most are not the people who
  die of alcohol-induced causes. Deaths may reflect drinking over many years, not current prevalence.
  This is an explanation to test, not a finding.

**Outside research so far:**
- ASPE issue brief (2015-2018): AUD fell 36% for 12-17 and 7% for 18-25 (both significant); 6% for
  26+, not significant. https://www.aspe.hhs.gov/reports/age-group-differences-progress-toward-reducing-substance-use-disorders-2015-2018-issue-brief
- NCHS Data Brief 448: age-adjusted alcohol-induced rate up 26% 2019 to 2020; alcoholic liver disease
  6.4 to 7.9 per 100K; rates peak at 55-64. https://stacks.cdc.gov/view/cdc/121795
- Wong, Böttcher, Chou, D'Orsogna (2025), PLOS Global Public Health: crude rate 7.0 (1999) to 13.2
  (2024); liver disease the leading cause; largest relative rise among women 25-34; pandemic spike
  peaking 2021. https://journals.plos.org/globalpublichealth/article?id=10.1371%2Fjournal.pgph.0004623
- Reports (not yet checked against primary data) of heavy drinking rising among adults 50-64,
  2018-2024.

**Is it just an older population? Partly (checked 2026-10-29):**
- CDC's age-adjusted rate (2000 US standard population) removes the effect of age mix.
  2009: 7.4 per 100K (NVSR vol. 60 no. 3, "Deaths: Final Data for 2009", Table 16; crude 8.0, which
  matches our data). 2019: 10.4 (NCHS Data Brief 448).
- Crude rate +49% (8.0 to 11.9); age-adjusted +41% (7.4 to 10.4). Aging accounts for a small part;
  most of the rise remains after adjusting for age.
- 2009 age-specific rates peaked at 45-54 (18.8) and 55-64 (21.2) per 100K (NVSR Table 11).

**Is it a labeling change? No sign of one in the code list:** CDC's 2009 report lists the same 14
ICD-10 codes we use (E24.4, F10, G31.2, G62.1, G72.1, I42.6, K29.2, K70, K85.2, K86.0, R78.0, X45,
X65, Y15). Whether doctors write alcohol on death certificates more often now is a separate
question we have not checked; look for research on certifier practice.

**To do before writing:**
- Pull WONDER alcohol-induced deaths by age group and state (Eric's browser) to test the age
  explanation directly.
- Pull SAMHSA's AUD by age for 2021-2024 (DSM-5 dataset).
- Check the 50-64 heavy-drinking study at its primary source.
- Note: AUD measures who has the disorder in a year; it does not measure how much people with it
  drink, so rising deaths with falling prevalence can both be true.

## Log

- 2026-10-28 Step 1 opened. Topic: state-by-state SUD prevalence vs outpatient treatment capacity, 2001-2024, as an interactive dashboard. Clean restart: no code, numbers or methods from earlier D4TP SUD repos.
- 2026-10-28 Decisions: add NAICS 621330 and 621112 to the worker count (establishments stay 621420); measure the state and local government share before deciding ownership; Claude runs the CDC WONDER exports in Eric's browser; compare N-SUMHSS and OEWS against QCEW as candidate supply sources.
- 2026-10-28 Data pulled and validated: QCEW 2001-2024, NSDUH (20 windows), N-SSATS/N-SUMHSS, OEWS, CBP, NAICS index, CDC WONDER (10 exports run by Eric). State-to-national sums pass for every fully disclosed year.
- 2026-10-28 Decisions: establishments map uses N-SSATS/N-SUMHSS outpatient SUD facilities (all ownerships; 2001 blank; 2021 break). Workers = QCEW 621420 + 621330 + 621112, private + state + local government. Where a withheld cell makes the worker total a floor, the Gap Score shows as "at most" and is hatched.
- 2026-10-28 Revised: with 621330/621112 added, about 30 states a year (12 in 2024) have a withheld worker cell. Gap Score map colors only complete states; floor states are hatched gray and show "at most" in hover and ranking. Where workers stand alone (card, trend line) a switch shows all ownership or private only.
- 2026-10-28 Eric: rename "Gap Score" to "People per Worker"; keep scales 0-150+ (2001-2019) and 25-200+ (2022-2024).
- 2026-10-28 Eric: People per Worker was choppy (483 of 1,020 complete under QCEW private + state + local). Built two versions for comparison: V1 OEWS clinicians (dist/v1-oews/) and V2 QCEW private, hatched when withheld or government is 20%+ (dist/v2-qcew-private/, 156 state-years hatched). OEWS code history checked against SOC crosswalks. Tie-out: 28,186 values, 0 mismatches.
- 2026-10-28 Pulled OEWS national industry job mix 2002-2024: counselors and MHSA social workers are about a third of jobs in 621420 and 621330.
- 2026-10-28 Eric: go with Version 1 (OEWS counselors and social workers). Single page at dist/index.html. Tie-out: 14,093 values, 0 mismatches. Second independent tie-out of the worker series started.
- 2026-10-28 Independent OEWS tie-out: 0 differences; US sampling-error note and 2001-2002 reference-month wording fixed.
- 2026-10-28 Eric approved legend end labels and direction captions; drug-only switch for deaths (ND drug rates under 20 deaths blank, CDC publishes none); drug-only switch extended to the SUD map with wording items 1-12. People per Worker stays on any SUD. Tie-out: 22,829 values, 0 mismatches.
- 2026-10-28 Eric: new neutral title "Substance Use Treatment / State by State, 2001-2024", new subtitle and tab title (proposals 1-3 accepted).
- 2026-10-28 Independent drug-only tie-out: 0 differences in 13,768 cells; 3 wording/display fixes.
- 2026-10-28 Eric: add Alcohol only (items 1-13 accepted; item 10 worded to CDC's definition), separate color scales per view, switch kept on the legend row. Tie-out: 29,745 values, 0 mismatches.
- 2026-10-28 Independent alcohol tie-out: 0 differences; alcohol trend line now drawn across 2015 (SAMHSA: the 2015 change did not affect alcohol use disorder); static notes fixed.
- 2026-10-28 Checked SAMHSA change tests: alcohol use disorder 2008-2009 vs 2018-2019 (long-term); SUD, drug, alcohol 2022-2023 vs 2023-2024 (short-term). Change view proposed, waiting on Eric.
- 2026-10-29 Eric: Change view wording items 1-9 accepted. Built: CHANGE button with three comparisons (alcohol 10-year test, 2022-2023 vs 2023-2024 tests, death rate 2019 to 2024). Tie-out: 30,577 values, 0 mismatches. Independent check of the Change view running.
- 2026-10-29 Independent Change-view tie-out: 1,291 values, 0 differences. Eric accepted items 1-13: "Learn more about the 2021 survey change" panel in the Survey redesign box, DSM-IV label on the 10-year test, Change-view wording fixes, menu follows the switch.
