# Independent tie-out: drug-only views (2026-10-28)

Run by a fresh agent with the page (`dist/index.html`), `DATASETS.md`, Eric's CDC WONDER
exports, and its own downloads from samhsa.gov and wonder.cdc.gov (57 files, logged in
`tieout_independent/raw_drug/PULLED.txt`, gitignored). It did not read `scripts/`,
`data/clean/`, `data/build/`, `data/raw/nsduh/`, `TIEOUT.md`, `STATUS.md` or git history.
Scripts and intermediate files are in this folder.

## Numbers: 13,768 cells, 0 differences

| Check | Cells | Differences |
|---|---|---|
| Drug use disorder vs SAMHSA SAS datasets (ABODILL, UDPYILL, UD5ILANY), 6 fields x 52 geos x 24 years | 7,488 | 0 |
| vs published Excel tables (2010-2011 to 2023-2024) | 3,276 | 0 |
| vs published HTML tables (2009-2010, 2010-2011) | 468 | 0 |
| Drug overdose deaths and rates vs WONDER | 2,496 | 0 |

- 2002, 2015, 2020 and 2021 are blank, and nothing else is.
- 2010-2011 matches SAMHSA's "(published)" estimates in all 52 geos.
- State counts sum to the national count within -5 to +3 thousand.
- The six "Unreliable" North Dakota drug rates (2001, 2002, 2004, 2005, 2006, 2011) are blank;
  the US count is the sum of states and the US rate is that sum / national population.
- Windows 2000-2001 and 2002-2003 to 2008-2009 were checked against the SAS dataset only;
  no published tables were found.

## Wording confirmed

Measure names and windows; DSM-5 from 2021-2022; WONDER cause codes X40-X44, X60-X64, X85,
Y10-Y14; People per Worker uses any SUD. Drug plus alcohol exceeds any SUD in all 1,040
state-windows (smallest gap 0.38 points, Maine 2012-2013); the implied national overlap is
28% to 37% of the drug estimate.

## Issues raised and what was done

1. The drug-only map used the any-SUD color scale, so most states were the lightest color.
   Fixed: each view now has its own scale (Eric asked for the same change).
2. "CDC publishes no rate when there are fewer than 20 deaths" holds for the 1999-2020
   database, which supplies every flagged cell, but the 2018-2024 database now uses a
   confidence-interval rule. Fixed: the page says CDC does not print a rate based on fewer
   than 20 deaths "in these years"; DATASETS.md now says "fewer than 20" and describes the
   2018-2024 rule.
3. From 2021-2022 the drug measure also counts prescription drug use disorder among all
   past-year users, not only misusers. Added to DATASETS.md.
