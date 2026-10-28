# Independent tie-out: alcohol-only views (2026-10-28)

Run by a fresh agent with the page, `DATASETS.md`, Eric's CDC WONDER exports, the earlier
agent's SAMHSA downloads (`raw_drug/`) and its own (`raw_alcohol/`, logged in PULLED.txt,
gitignored). It did not read `scripts/`, `data/clean/`, `data/build/`, `data/raw/nsduh/`,
`TIEOUT.md`, `STATUS.md` or git history. Scripts are in this folder.

## Numbers: 0 differences

| Check | Cells | Differences |
|---|---|---|
| Alcohol use disorder vs SAMHSA SAS datasets (ABODALC, UDYR5ALC), 6 fields x 52 geos x 24 years | 7,488 | 0 |
| vs published Excel tables (22 workbooks, 2010-2011 to 2023-2024) | 3,432 | 0 |
| vs published PDF/HTML (2014-2015 percents, 2009-2010 and 2010-2011) | 624 | 0 |
| Alcohol-induced deaths and rates vs WONDER | 2,496 | 0 |

- 21 windows; blank years are exactly 2002, 2020 and 2021; 2015 has a value. SAMHSA did
  publish 2014-2015 alcohol use disorder (Totals Table 10 and Percents PDF Table 10; the
  2014-2015 guide lists it among the 14 measures).
- 2010-2011 matches "(published)" in all 52 geos. The 12-20 underage table was not used.
- State counts sum to the national count within +/-4 thousand.
- No alcohol death cell is suppressed or unreliable; drug + alcohol = combined in all 1,224
  state-years; the WONDER exports use "Alcohol-induced causes".
- 2000-2001 to 2008-2009 were checked against the SAS dataset only.

## Wording

Confirmed: the CDC exclusion sentence (NCHS Data Brief 448), the code list, "alcoholic liver
disease or alcohol poisoning", the overlap claim (all 1,040 geo-windows), labels and notes.

## Issues raised and what was done

1. The static limitations said 2015 has no state estimates and that 2015 breaks
   comparability. Fixed: both now note the alcohol exception.
2. SAMHSA's 2014-2015 guide (A.6) says the 2015 change "did not affect estimates for alcohol
   use or alcohol use disorder." Fixed: the alcohol trend line is now drawn across 2015.
3. The sources line did not mention DSM-5 for alcohol from 2021-2022. Fixed.

Color scales: alcohol use disorder 3-11% (3 of 918 state-years above) and 7-17% (1 of 153
above); alcohol deaths 0-25 (47 of 1,224 above, mostly 2015 on).
