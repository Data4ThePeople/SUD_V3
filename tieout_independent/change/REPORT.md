# Independent tie-out: Change view (fresh agent, 2026-10-29)

The agent could not write files itself; Claude saved its report here verbatim in substance.

**Values: 1,291 compared, 0 differences.**
- SAMHSA tests: 832 values (52 rows x 4 comparisons x from %, to %, p, result), 12+ columns, re-downloaded
  2026-10-29 into `tieout_independent/raw_change/` (git-ignored). Every "a" row has p < 0.05 and every
  p < 0.05 row has an "a". States marked "b" only (significant at 0.10) are shown as no significant change:
  Table 9 HI, LA, MA, NC, OR, WA; Table 21 IA, ME, MT; Table 22 CA, CO, HI, ID, LA, MI; Table 24 AR, CA,
  CO, GA, IL, IA, KS, LA, MN, NM, WV.
- Death-rate change: 306 rates (2019 and 2024) against Eric's WONDER exports and 153 percent changes, all
  exact. No state is blank in any grouping. Ranking lines: drug + alcohol 40 rose, 11 fell; drug only 33
  rose, 17 fell, 1 unchanged (Rhode Island, 29.0 both years); alcohol only 48 rose, 3 fell (OK, WV, NJ).
  Using deaths and population instead of CDC's printed rates moves the percent change by at most 0.81
  points; no state changes direction (Rhode Island drug only would be +0.2%).

**Wording supported:** the 0.05 / 0.10 markers; "p < 0.001" (Tables 21, 22, 24 say a printed 0.000 means
p < 0.001); no test across the 2021 redesign; no 2021-2022 vs 2023-2024 test; no long-term test for drug
use disorder or any SUD (2015-2019 long-term releases checked); sources line titles.

**Wording issues raised:**
1. Table 9 alcohol use disorder is DSM-IV dependence or abuse; the 2022-2024 tables are DSM-5. The cards
   show them side by side with no note.
2. "Too small to tell apart from survey error": SAMHSA's p values come from a model; fair plain language,
   not exact.
3. "Published this 10-year test only for alcohol use disorder": the release also tests marijuana, cocaine
   and alcohol use, so "only" could be misread.
4. "These are counts of deaths, not survey estimates" reads oddly next to a rate change.
5. WONDER's 2019 population is on a 2010 Census base and 2024 on the 2020 blended base; not mentioned.
6. The "fewer than 20 deaths" sentence is the 1999-2020 database rule; it never shows now, but would be
   wrong for 2018-2024 data.

**Display issues raised:**
1. The menu always reads "Substance use disorder, ..." when Drug only or Alcohol only is selected.
2. Virginia shows "+0%" (+0.37%); a value between -0.5% and 0 would show "-0%".
3. The death legend does not show the scale is capped (reads "-60" / "+60", no "%"); 9 values pass +60.

**Not verified:** the page was not rendered (display findings from reading the code); WONDER was not
pulled again; a one-off SAMHSA report outside the release pages cannot be ruled out; SAMHSA's model-based
p values were not reproduced.
