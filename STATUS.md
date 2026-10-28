# Status

Project: SUD_V3 (Demand Without A Door: America's Substance-Use Treatment Gap)
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
