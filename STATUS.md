# Status

Project: SUD_V3 (Substance Use Treatment, State by State, 2001-2024)
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: alcohol data for thought (slug set at 2a)
Step: 1 (exploration and analysis)
Since: 2026-11-12

Previous post: substance-use-treatment-viz, complete 2026-11-05.

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-11-04 | |
| 2a | Draft with brackets resolved | 2026-11-04 | |
| 2b | Eric's edit, Claude's look-over | 2026-11-04 | |
| 2c | Slice markup | 2026-11-04 | |
| 2d | Hero 1680x1080 + alt text | 2026-11-04 | |
| 2e | SEO | 2026-11-04 | |
| 2f | Pushed to Prismic (draft) | 2026-11-04 | |
| 2g | Mailchimp teaser | 2026-11-05 | Body written by Eric |

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

### 2. Why some states have more facilities and workers (raised by Eric, 2026-10-29)

**Where states stand, 2024 (our data):**
- Facilities per 100K, most: KY 11.4, AK 10.3, ME 9.8, VT 8.3, MT 8.2. Fewest: TX 1.6, SC 1.7,
  AL 2.2, CA 2.4, FL 2.5, GA 2.7. The low end has been stable: TX, SC, AL, MS ranked 45-51 on average
  in 2003-2019 too.
- Workers per 1,000 people with SUD, most: MA 20.3, UT 17.9, VA 17.5, PA 16.1, NH 16.0. Fewest:
  NV 5.6, AL 5.7, GA 6.2, SC 6.6, TX 6.8, NM 7.5, MS 7.8.
- Facility and worker rankings differ: CA and NY are low on facilities but high on workers
  (facility size and setting differ; OEWS counts every setting).

**Medicaid expansion (KFF, data/raw/kff/), medians across states:**
- Workers per 100K: expanded 2014-2015 (30 states) 106 in 2010, 188 in 2024; never expanded (10)
  69 in 2010, 116 in 2024. The worker gap existed before 2014, so expansion does not explain where
  it started.
- Facilities per 100K, change 2013 to 2019: +17% in states that expanded 2014-2015, +1% in states
  that never expanded.
- Exceptions: NV and NM expanded in 2014 and are near the bottom on workers.

**Party control (Ballotpedia, data/clean/trifectas.csv, 50 states, most common status 2001-2024):**
- 2024 workers per 1,000 with SUD: mostly D (15) 11.6, mostly R (19) 9.9, mostly divided (16) 12.6.
  Facilities barely differ (4.7-4.9 per 100K).
- Among the 40 expansion states the medians are close (D 11.6, R 11.2, divided 12.8). The low values
  are in the non-expansion states (median 7.3), 8 of which are mostly R. Party and expansion overlap
  too much to separate with 50 states. Publish on the policy (expansion), not the party.
- Mostly-R states near the top: UT 17.9, SD 13.7, OH 13.3, IN 13.0. Mostly-D states near the bottom:
  NM 7.5, NC 8.5.

**Research (agent report 2026-10-29; (a) = a study measured a change after a policy, (b) = descriptive):**
- Medicaid expansion: (a) specialty SUD treatment episodes +28% vs non-expansion states (Maclean
  et al., Health Affairs 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12616645/). Facility and
  workforce effects weak or mixed: no significant change in SUD-sector hiring (Scrivner et al.,
  PLOS One 2020, https://arxiv.org/pdf/1908.00216); modest facility gains in one study (Laurito &
  Cantor 2024, https://pubmed.ncbi.nlm.nih.gov/39515239).
- 1115 SUD waivers: (a) facility Medicaid acceptance rose vs non-waiver states in CA, VA, WV; no
  change in MD, MA (RTI for CMS 2025, https://www.medicaid.gov/medicaid/section-1115-demonstrations/downloads/sud-rcr-oy3-nssats-medicaid-moud.pdf).
  Confirm current waiver list on Medicaid.gov before publishing.
- Virginia ARTS (April 2017: higher rates, full ASAM continuum, peer support): (b) Medicaid-billing
  outpatient SUD practitioners 1,087 to 2,965 in year one (VCU,
  https://healthpolicy.vcu.edu/media/school-of-population-health/hbp-2023/ARTSone-yearreport_8.9.18_ACC.pdf).
  Our data: VA facilities 193 (2017) to 341 (2024), +77%; US +19% over the same years. VA also
  expanded Medicaid in 2019, so the two cannot be separated.
- Kentucky: (b) 2014 new Behavioral Health Services Organization license, exempt from certificate
  of need, let more organizations bill Medicaid (https://hallrender.com/2014/07/22/kentucky-emergency-regulations-create-two-new-licenses-for-health-facilities/).
  Our data: KY facilities 248 (2010) to 524 (2024), the most per resident in 2024. No evaluation
  isolates the license's effect.
- Vermont Hub and Spoke: (b) OUD medication capacity 3.76 to 10.56 per 1,000 residents, 2012-2016
  (Brooklyn & Sigmon 2017, https://pmc.ncbi.nlm.nih.gov/articles/5537005). About medication capacity,
  not counselors.
- CCBHCs: (b) clinics report the payment model let them raise salaries and hire (ASPE Report to
  Congress 2025). Medicaid rates alone: weak (psychiatrist fees did not track supply).
- Low-ranking states: TX has 246 of 254 counties in mental health shortage areas (Texas Tribune /
  Hogg Foundation); GA's commission named workforce the core barrier.

**Practices low-ranking states could adopt, by evidence strength:**
1. Expand Medicaid: strong for Medicaid-paid treatment; weak or mixed for facility and worker counts.
2. Cover the full ASAM continuum and raise SUD rates together (Virginia): moderate.
3. A facility license that lets more organizations bill Medicaid (Kentucky): weak, descriptive.
4. Join the CCBHC program: weak to moderate, self-reported.
5. Loan repayment for behavioral health workers: moderate for retention, limited for supply.

**Check before writing:**
- Vermont (checked 2026-10-29): our count fell from 2,640 (2019) to 1,520 (2024). Both codes fell
  (21-1018 counselors 1,810 to 1,150; 21-1023 social workers 830 to 370), starting in 2020, before
  the 2021 BLS method change. Over the same years Vermont's "community and social service
  specialists, all other" (21-1099) rose from 530 to 2,540, and the total of all 21-10xx/21-109x
  codes changed much less (about 10,400 to 9,300). This looks at least partly like employers
  reporting the same jobs under a different code. Do not use Vermont's worker trend as a finding;
  if it matters, ask BLS or the Vermont Department of Labor. Vermont's facility count rose
  (42 in 2019 to 54 in 2024).

**The Medicaid angle going forward (Eric, 2026-10-29):**
- H.R. 1 (2025 reconciliation law): work requirements for expansion adults ages 19-64 start no
  later than December 31, 2026. States must exempt people "participating in a substance use
  disorder treatment program" (KFF).
- Law text checked 2026-10-29 (Public Law 119-21, sec. 71119, 139 STAT. 312-313; saved in
  data/raw/law/). Two separate exemptions cover SUD:
  - (V) "medically frail or otherwise has special medical needs (as defined by the Secretary),
    including an individual ... (bb) with a substance use disorder". This covers people with SUD
    whether or not they are in treatment.
  - (VII) "participating in a drug addiction or alcoholic treatment and rehabilitation program (as
    defined in section 3(h) of the Food and Nutrition Act of 2008)".
  - Both are "as determined by the State (in accordance with standards specified by the
    Secretary)". Under (xx)(5) the State verifies exemptions using "reliable information available
    to the State (such as payroll data or payments or encounter data ...)" without requiring, "where
    possible", the person to submit more information. If the State cannot verify, the person gets a
    notice and 30 days to show compliance.
  - The open question for a story (inference, not yet checked): a State's records show SUD only for
    people who were diagnosed or billed for it. People with an untreated SUD may have to prove the
    exemption themselves. Check SAMHSA's share of people with SUD who received treatment, and CMS's
    interim rule or guidance on how States define and verify the SUD exemption.
- Eric's angle (2026-10-29, from his knowledge in Ohio): Ohio JFS is already overwhelmed with calls
  and cannot keep pace. From January 1 eligibility calls and questions will rise sharply, and people
  the law says should qualify (including the SUD exemptions) may sit in a backlog without coverage.
  Needs public evidence before it goes in a post. Sources to check: CMS's monthly state Medicaid call
  center data from the 2023-2024 unwinding (call volume, average wait, abandonment rate, Ohio vs
  other states); the unwinding share of disenrollments that were procedural; Arkansas 2018 work
  requirement results; Georgia Pathways; Ohio's own implementation plan and staffing.
- CBO, as summarized by KFF: the law reduces federal health spending by over $1 trillion and adds
  10 million uninsured; the work requirement alone cuts federal Medicaid spending $326 billion over
  10 years and adds 5.3 million uninsured in 2034. Provider tax limits for expansion states start
  falling October 1, 2027; state-directed payment cuts start January 1, 2028.
- KFF's summary does not call it the largest Medicaid cut ever. Find a source before using that
  phrase, or use CBO's dollar figure instead.
- The tie to our data: the states that grew facilities fastest after 2014 were early expansion
  states, and the work requirements apply to the expansion group. Research shows expansion raised
  Medicaid-paid treatment strongly; its effect on facility and worker counts is weak or mixed. So
  the supported framing is "Medicaid now pays for much of this treatment," not "Medicaid built
  these facilities."
- Sources: https://www.kff.org/medicaid/health-provisions-in-the-2025-federal-budget-reconciliation-law/ ;
  https://www.kff.org/medicaid/the-impact-of-h-r-1-on-two-medicaid-eligibility-rules/
- OEWS leaves out the self-employed, so states with more private-practice counselors are undercounted.
- Most research measures Medicaid-billing providers or service use, not total capacity.

### 3. Why overdose and alcohol death rates rose everywhere (raised by Eric, 2026-10-30)

National tests (CDC WONDER API, `data/raw/wonder_api/`; Eric's exports
`data/raw/wonder/mcd_*`). Totals tie to our national counts, except cells CDC suppresses.

- **Aging:** 2001-2019, alcohol crude +68% vs age-adjusted +49%; drug crude +216% vs
  age-adjusted +218%. Rates rose within age groups for both (alcohol 25-34 +162%, 55-64 +78%;
  drug 55-64 +547%, 25-34 +314%). Aging is a small part of alcohol and none of drugs.
- **Drug type (multiple cause; one death can count under several drugs):** deaths involving
  synthetic opioids other than methadone (T40.4, mostly fentanyl) went from 957 (2001) and
  3,105 (2013) to 73,838 (2022) and 47,735 (2024). Overdoses without T40.4: 18,437 (2001),
  40,877 (2013), 34,271 (2019), 34,103 (2022), 31,649 (2024). The rise after 2013 is in
  T40.4-involved deaths. T40.4 share of overdoses: 7% (2013), 51% (2019), 68% (2022), 60% (2024).
  2022-2024: all overdoses -28,557; T40.4-involved -26,103. Heroin and prescription opioid
  deaths peaked in 2017. Cocaine 3,833 -> 29,449 (2023); psychostimulants 563 -> 34,855 (2023).
  Not checked: deaths with no specific drug named (T50.9), more common in early years, so
  early drug-type counts are likely low.
- **2019-2024 by age:** drug rates fell for ages 15-34 but rose for 55-64 (+27%) and 65-74
  (+71%). Alcohol rates peaked in 2021 in most age groups; 2024 still above 2019 in every
  group 25 and older.
- **Cirrhosis coding (1999-2020 only):** age-adjusted K70 alcoholic liver disease +49%, other
  cirrhosis K73-K74 -4%, both together +20% (2001-2019). Fits a partial coding shift but
  K73-K74 also moves with hepatitis C and fatty liver disease. Unresolved.
- **Still open:** NIAAA per-capita alcohol by state; state timing of fentanyl arrival (needs
  state multiple-cause exports); fentanyl co-involvement with stimulants.

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
- 2026-10-30 Eric: removed the Change view and its analysis from the page, build, tie-out and docs (it helped understanding but complicates the page). QCEW, CBP and NAICS index also removed from docs, code and data. Tie-out now 29,745 values, 0 mismatches.
- 2026-11-04 Eric: first post is a visualization-only page; analysis comes in later posts. Draft at posts/substance-use-treatment-viz/POST.md (method and how-to sections summarized, linking to DATASETS.md and TIEOUT.md). Repo made public with README; GitHub Pages live at https://data4thepeople.github.io/SUD_V3/. Shareable artifact: https://claude.ai/artifact/DMCdyMH4X9xCU1MJkNjnHp
- 2026-11-04 Eric: Step 1 done. Step 2a open for posts/substance-use-treatment-viz.
- 2026-11-04 Eric: Step 2a done. Step 2b open.
- 2026-11-04 Eric: Step 2b done (look-over items 1-13 accepted). Step 2c open.
- 2026-11-04 Eric: Step 2c done (subtitle item 1 accepted). Step 2d open: hero from the 2024 People with SUD per Worker map (scripts/make_hero.py).
- 2026-11-04 Eric: Step 2d done. Step 2e open: meta, keywords and dataset schema drafted from Claude's suggested searches, pending Eric's.
- 2026-11-04 Eric: Step 2e done (items 1-3 accepted). Step 2f open.
- 2026-11-04 Pushed to Prismic as a draft in the Migration Release: document auvIrBIAAC4AbnVB, 69 slices, hero uploaded. Tags and author empty.
- 2026-11-04 Eric: Step 2f done (schema author Jameson Mehaffey, time 7:15 pm Eastern). Step 2g open.
- 2026-11-04 Created cloud routine 'SUD map: new source data monitor' (trig_01VgF9wi3mBK1MrE5hHQ2vtY): Mondays 9am ET, checks NSDUH SAE, N-SUMHSS, OEWS, WONDER for vintages newer than the map's, emails eric@asaltollc.com once per new release. Report only, no rebuilds. https://claude.ai/code/routines/trig_01VgF9wi3mBK1MrE5hHQ2vtY
- 2026-11-04 Eric: rejecting the 2g email draft; he will write his own on 2026-11-05. Claude puts it into EMAIL.md verbatim in the same structure, no edits unless asked.
- 2026-11-05 Eric's email body placed in EMAIL.md; name spelling, age group, Medicaid work requirements wording and look-over items 1-3 accepted.
- 2026-11-05 Eric: Step 2g done. Post substance-use-treatment-viz complete.
- 2026-11-05 Embed: Find Treatment button hidden in the embed (the site's HTML embed slice frames it with sandbox="allow-scripts", which blocks links); kept on the full page. Cache-buster 20261105a; Prismic draft re-pushed.
- 2026-11-05 Social posts drafted from Eric's email (SOCIAL.md: X, Bluesky, LinkedIn) with a GIF cycling the four 2024 map views (scripts/make_social_gif.py).
- 2026-11-12 Step 1 opened for a short data-for-thought post (Eric): is drinking getting more deadly while fewer people drink? Two charts in dist/alcohol/ (scripts/alcohol/). Age-adjusted alcohol-induced death rate 1999-2024 (2021-2024 age-adjusted by us from CDC age groups; method reproduces CDC's 1999-2020 rates within 0.06). Percent change 2002-2003 to 2018-2019: past-month drinking +1%, alcohol use disorder -30%, age-adjusted death rate +46%. Independent tie-out started.
- 2026-11-12 Independent tie-out (tieout_independent/alcohol/): every chart number matches, 0 differences; 2021 and 2022 age-adjusted rates and counts equal NCHS NVSR. Three wording fixes applied: source named as underlying cause, "injuries where alcohol played a part", "2-year pooled estimates"; DATASETS names the 2018-2024 export's database correctly. Not checkable yet: 2023-2024 against NCHS (2023 final data public 2026-11-17).
