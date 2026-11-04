# Substance Use Treatment, State by State, 2001 to 2024

An interactive map that puts four things side by side for every state and DC, each year from 2001 to 2024: how many people have a substance use disorder (SUD), how many outpatient treatment facilities there are, how many treatment workers there are, and how many people die of a drug overdose or an alcohol-induced cause. It also shows People with SUD per Worker: SAMHSA's count of people with SUD divided by the number of treatment workers.

Where a source did not publish a number for a state and year, the map leaves it blank. Nothing is filled in, estimated or smoothed.

## Live links

- Interactive map: https://data4thepeople.github.io/SUD_V3/

## What's here

- `dist/index.html`: the built map, one self-contained page with no outside libraries. GitHub Pages publishes this folder on every push to `main` (`.github/workflows/pages.yml`).
- `scripts/`: the build pipeline, the page template (`template.html`) and the checks.
- `data/raw/`: source files saved unchanged, each folder with a `PULLED.txt` that gives the URL, date and settings. The OEWS zips and the facility survey files are not in git because of their size; their URLs are in `PULLED.txt`.
- `data/clean/`: one tidy table per source.
- `data/build/`: the joined panel (`panel.csv`), the data the page reads (`dashboard.json`), coverage and tie-out results.
- `tieout_independent/`: independent checks, written from scratch without this repo's code, with their reports.
- `posts/`: the post that goes with the map.
- `DATASETS.md`: a full description of each source, its definitions, coverage, changes over time and known quirks.
- `TIEOUT.md`: every check run on the numbers and the words on the page, and what each found.

## Data sources

| Agency | Dataset | Used for |
|---|---|---|
| SAMHSA | National Survey on Drug Use and Health (NSDUH), state small area estimates | Share and number of people 12 and older with a substance use disorder, a drug use disorder or an alcohol use disorder |
| SAMHSA | N-SSATS (2000 to 2020) and N-SUMHSS (2021 to 2024) public-use files | Facilities that offer outpatient substance use treatment |
| U.S. Bureau of Labor Statistics | Occupational Employment and Wage Statistics (OEWS), state files | Substance use and mental health counselors and social workers |
| CDC | CDC WONDER, Underlying Cause of Death, 1999-2020 and 2018-2024 Single Race | Drug overdose and alcohol-induced deaths, and population |

All sources are public domain.

## How to rebuild

Requirements: Python with pandas, openpyxl, pypdf and requests. The CDC WONDER exports were run by hand in the WONDER web tool, because the WONDER API refuses queries grouped by state. Their settings are saved at the bottom of each file in `data/raw/wonder/`.

Run from the repo root, with `-I`:

```
python -I scripts/build_nsduh_sud.py    # SUD estimates by state and survey window
python -I scripts/check_nsduh_sud.py    # tie them to SAMHSA's SAS datasets
python -I scripts/build_nsduh_parts.py  # drug and alcohol use disorder
python -I scripts/build_nsumhss.py      # outpatient facility counts
python -I scripts/check_nsumhss.py      # tie them to the published frequencies
python -I scripts/build_oews.py         # counselors and social workers
python -I scripts/clean_wonder.py       # deaths and population
python -I scripts/build_geo.py          # state shapes
python -I scripts/build.py              # join into panel.csv and dashboard.json
python -I scripts/render.py             # write dist/index.html
python -I scripts/validate_sums.py      # states add up to the national figure
python -I scripts/tieout.py             # recompute every number on the page
python -I scripts/coverage.py           # how many states have each value, by year
```

`fetch_nsduh.py` downloads NSDUH files into `data/raw/nsduh/`.

## Method notes

- **SUD.** SAMHSA's state estimates pool two survey years. Each one is shown at its second year, so 2024 is 2023-2024. SAMHSA published no state estimates for the windows ending in 2002, 2015, 2020 and 2021. Estimates are not compared across SAMHSA's 2002, 2015 and 2021 survey changes. From 2021 SAMHSA uses the DSM-5 definition of a disorder, and its estimates are not comparable with earlier years.
- **Facilities.** A facility counts if it said it offers outpatient substance use care. Facilities that did not answer the survey are not counted, so each count is a minimum. There was no survey in 2001. In 2021 the survey merged with SAMHSA's mental health facility survey.
- **Workers.** Substance abuse and mental health counselors (SOC 21-1011 and 21-1014 through 2016; 21-1018, which combines them, from 2017) plus mental health and substance abuse social workers (21-1023), in all settings and ownerships. The self-employed are not included. A state-year has a value only when every part is published. BLS changed its estimation method with the May 2021 estimates.
- **Deaths.** Underlying cause of death: drug overdose (X40-X44, X60-X64, X85, Y10-Y14) or alcohol-induced (E24.4, F10, G31.2, G62.1, G72.1, I42.6, K29.2, K70, K85.2, K86.0, R78.0, X45, X65, Y15). Each death has one underlying cause, so no death is counted twice. Rates are crude rates per 100,000.
- **People with SUD per Worker** divides a two-year SUD count by the worker count for the window's second year. It is not a caseload. The worker count covers every setting and includes mental health work.
- **Checks.** `tieout.py` recomputes every value on the page. `validate_sums.py` checks that the states add up to the national figure. Independent checks are in `tieout_independent/`. Results are in `TIEOUT.md`.
