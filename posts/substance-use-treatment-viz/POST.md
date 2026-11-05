---
title: "Substance Use Treatment, State by State: An Interactive Map, 2001 to 2024"
subtitle: A free, interactive map of substance use disorder rates, outpatient treatment establishments, treatment workers, people with SUD per worker, and overdose and alcohol-induced deaths in all 50 states and DC, each year from 2001 to 2024.
slug: substance-use-treatment-viz
date: 2026-11-04
updated: 2026-11-04
section: Visualization
hero: images/substance-use-treatment-viz-hero-1680x1080.png
hero_alt: Map of the United States on a dark background, titled People with SUD per treatment worker, 2024. States are shaded from pale orange (25) to dark orange (200 or more). Nevada, Alabama, Georgia, South Carolina and Texas are darkest; Massachusetts, Utah and Virginia are palest. Beside it: Substance Use Treatment, State by State. 85 people with a substance use disorder for each treatment worker in the U.S., 2024. Nevada: 177. Massachusetts: 49. Data 4 The People. Sources: SAMHSA, BLS.
meta_title: "Substance Use Treatment by State: Map, 2001-2024"
description: "Free interactive map of substance use disorder rates, treatment facilities and workers, and overdose and alcohol deaths in every state, 2001 to 2024."
keywords: substance use disorder by state, addiction treatment by state, substance abuse treatment facilities by state, behavioral health workforce shortage by state, overdose deaths by state map, alcohol deaths by state, how many people have a substance use disorder, NSDUH state estimates
schema_type: dataset
dataset_name: Substance use disorder, outpatient treatment establishments, treatment workers, and drug overdose and alcohol-induced deaths, U.S. states and DC, 2001 to 2024
dataset_description: "SAMHSA National Survey on Drug Use and Health state estimates of people 12 and older with a substance use disorder, drug use disorder or alcohol use disorder (two-year windows, 2000-2001 to 2023-2024); SAMHSA N-SSATS and N-SUMHSS counts of facilities offering outpatient substance use treatment; BLS Occupational Employment and Wage Statistics employment of substance abuse and mental health counselors and social workers; and CDC WONDER drug overdose and alcohol-induced deaths by state of residence. Values not published by the source are left blank."
temporal: 2001/2024
spatial: United States
measured: Substance use disorder prevalence, ages 12 and older|percent; People with a substance use disorder|count; Outpatient substance use treatment establishments|count; Establishments per 100,000 residents|rate; Substance abuse and mental health counselors and social workers|count; People with a substance use disorder per treatment worker|ratio; Drug overdose and alcohol-induced deaths|count; Death rate|deaths per 100,000 residents
sources: https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health|https://www.samhsa.gov/data/data-we-collect/n-sumhss-national-substance-use-and-mental-health-services-survey|https://www.bls.gov/oes/|https://wonder.cdc.gov/
distribution: text/html|https://data4thepeople.github.io/SUD_V3/;text/csv|https://github.com/Data4ThePeople/SUD_V3/tree/main/data/build
measurement_technique: Published state estimates and counts joined by state and year with no imputation. People with SUD per worker divides SAMHSA's two-year SUD count by the BLS worker count for the window's second year. Death rates are CDC crude rates per 100,000.
credit: Data 4 The People, from SAMHSA, the U.S. Bureau of Labor Statistics and CDC
license: https://www.data4thepeople.com/terms-of-use
app_url: https://data4thepeople.github.io/SUD_V3/
app_name: "Substance Use Treatment, State by State: interactive map, 2001 to 2024"
app_category: EducationalApplication
app_description: Free interactive map of substance use disorder rates, outpatient treatment establishments, treatment workers, people with SUD per worker, and overdose and alcohol-induced deaths in all 50 states and DC, each year from 2001 to 2024.
app_features: All 50 states and DC, 2001 to 2024|Play through the years|Four map views: SUD prevalence, establishments per 100K, people with SUD per worker, death rate|Drug + alcohol, drug only or alcohol only|Cards with each state's numbers and 95% intervals|Ranking of all states for the map shown|Trend chart for each state with survey changes marked|Link to FindTreatment.gov and the 988 Lifeline
drop_cap: false
heading_spacer: 20px
caption_spacer: 20px
dividers: false
---

# Substance Use Treatment, State by State: An Interactive Map, 2001 to 2024

<iframe src="https://data4thepeople.github.io/SUD_V3/?v=20261104b#embed=1" width="100%" height="1420" loading="lazy" style="border:0" title="Substance Use Treatment, State by State: interactive map, 2001 to 2024"></iframe>

::: spacer 40px

::: blurb
**[Open the full visualization](https://data4thepeople.github.io/SUD_V3/)** **for the title and the full notes.**
:::

::: spacer

## Purpose

::: spacer 5px

Substance use is one of the most important health topics in the country. This visualization isn't meant to put substance use in a good or bad spotlight; its purpose is to provide factual information so you can see where we stand as a country on substance use disorder and treatment. For every state and DC, from 2001 to 2024, you can view how many people have a substance use disorder (SUD), how many outpatient treatment establishments there are, how many people with SUD there are for each treatment worker, and how many people die of a drug overdose or alcohol-induced cause. It is built from four sources listed below. Where a source did not publish a number for a state and year, the map leaves it blank. We do not fill in, estimate or smooth any missing value. It is free to use and needs no sign-in.

This tool has several underlying stories within it that later posts will look at more closely to describe what the data shows. The visualization gets its own post because it holds all the data without a big headline taking away from its true value: to inform and help others. This map lets you play around with the years to discover headlines and see how our country has been affected by substance use over time. In addition to making the audience aware of substance use, it offers help by linking to FindTreatment.gov, a site where you can type in your ZIP code and find the nearest treatment facility for anyone who may need it. Spreading awareness and helping others are the main purposes of this map. The underlying data and code are free to download on [GitHub](https://github.com/Data4ThePeople/SUD_V3).

::: blurb Read this first
People with SUD per Worker is a rough measure of how many people need care for each person trained to give it. It is not a caseload. The worker count includes counselors and social workers in every setting, including hospitals, schools and prisons, and it includes mental health work. Many people with a disorder never seek treatment. Read it as a way to compare states, not as the number of patients each worker sees. Also, SAMHSA changed its survey and its definition of a disorder in 2021, so disorder rates from 2021-2022 on cannot be compared with earlier years. The map marks this change.
:::

## Using the visualization

::: spacer 5px

**1. Pick a year.** Drag the slider, or click Play to move through every year from 2001 to 2024.

**2. Pick a map.** The buttons above the map switch between SUD %, establishments per 100,000 residents, People with SUD per Worker, and the death rate from drug overdoses and alcohol-induced causes.

**3. Pick the substances.** Drug + alcohol, Drug only, or Alcohol only. This changes the SUD and death numbers everywhere on the page.

**4. Hover or click a state.** The cards beside the map show that state's numbers. Clicking a state keeps it selected, highlights it in the ranking, and shows its history in the trend chart below the map.

**5. Read the trend chart.** The buttons under the chart switch between the five measures. Gaps and shaded bands mark years that cannot be compared.

### How to read it

- **Darker states** have more of whatever the map shows.
- **Gray states** have no published number for that year.
- **Each SUD number covers two years.** SAMHSA's state estimates pool two survey years. The map shows each one at its second year, so "2024" is 2023-2024.
- **Some years have no SUD estimate.** SAMHSA published no state estimates for the windows ending in 2002, 2015, 2020 and 2021.
- **The color scale for SUD and the ratio changes in 2022,** because estimates from 2021-2022 on are much higher under the new survey.

### What it shows right now

In 2023-2024, SAMHSA estimates that 48.4 million people 12 and older had a substance use disorder, 16.9% of that age group. BLS counted 566,290 substance use and mental health counselors and social workers in 2024. That is 85 people with SUD per worker, down from 105 in 2022. The number of workers rose 131% from 2003 to 2024.

There were 126,098 drug overdose and alcohol-induced deaths in 2024: 79,384 from drug overdoses and 46,714 from alcohol-induced causes. That is 22% below the peak of 160,957 in 2021, and 219% above 2001.

### States with the most and fewest people with SUD per worker

In 2024, the states with the most people with SUD for each treatment worker:

1. Nevada (177)
2. Alabama (175)
3. Georgia (162)
4. South Carolina (152)
5. Texas (147)

The states with the fewest:

1. Massachusetts (49)
2. Utah (56)
3. Virginia (57)
4. Pennsylvania (62)
5. New Hampshire (63)

The 2024 death rate for drug overdose and alcohol-induced causes was highest in Alaska and New Mexico (73.8 per 100,000) and lowest in Nebraska (23.9).

## What this page is

::: spacer 5px

Every chart we publish should be something you can check, question and rebuild yourself. This page gives a short summary of how we built this one. The full documentation, with every source, definition, survey change and check, is in the public repository: [DATASETS.md](https://github.com/Data4ThePeople/SUD_V3/blob/main/DATASETS.md) for the method and [TIEOUT.md](https://github.com/Data4ThePeople/SUD_V3/blob/main/TIEOUT.md) for the checks.

## The data sources

::: spacer 5px

**National Survey on Drug Use and Health (NSDUH), state estimates, SAMHSA.** The share and number of people 12 and older with a substance use disorder, a drug use disorder or an alcohol use disorder, by state.

**National Survey of Substance Abuse Treatment Services (N-SSATS) and National Substance Use and Mental Health Services Survey (N-SUMHSS), SAMHSA.** The number of facilities in each state that offer outpatient substance use treatment.

**Occupational Employment and Wage Statistics (OEWS), U.S. Bureau of Labor Statistics.** The number of substance use and mental health counselors and social workers in each state.

**CDC WONDER, Underlying Cause of Death, CDC.** Drug overdose and alcohol-induced deaths and population, by state of residence.

## How we built it, in short

::: spacer 5px

- **We use each publisher's numbers as published.** Nothing is filled in. When a source withheld a number, or published none, the map shows it as blank.
- **SUD.** We use SAMHSA's published state estimates and their confidence ranges. We do not compare estimates across the 2002, 2015 and 2021 survey changes. The trend line breaks at each one.
- **Establishments.** We count every facility that said it offers outpatient substance use care. Facilities that did not answer the survey are not counted, so each count is a minimum. In 2021 the facility survey merged with SAMHSA's mental health facility survey.
- **Workers.** We add substance use and mental health counselors to mental health and substance use social workers. BLS combined the two counselor groups into one in 2017, so we count both in every year to keep one definition. When BLS did not publish one of the groups for a state, that state's worker count and ratio are blank for that year.
- **Deaths.** We count deaths whose underlying cause was a drug overdose or an alcohol-induced cause. Each death has one underlying cause, so no death is counted twice. Rates are per 100,000 residents.
- **People with SUD per Worker** is SAMHSA's count of people with SUD divided by the worker count for the second year of the survey window.
- **We check the numbers.** A script recomputes every number on the map from the source files and compares them. Separate checks, written from scratch without our code, pulled the data again and found no differences. We also check that the states add up to the national total.

## Updating

::: spacer 5px

We plan to add each new year when SAMHSA, BLS and CDC release it.

## Honest notes and limitations

::: spacer 5px

These are the main limits. The full list is in [DATASETS.md](https://github.com/Data4ThePeople/SUD_V3/blob/main/DATASETS.md) and in the notes at the bottom of the map.

- **Survey changes break the SUD trend.** SAMHSA changed its survey in 2002, 2015 and 2021. From 2021, it uses a newer definition of a disorder (DSM-5) and lets people answer online, and its estimates are not comparable with earlier years.
- **The survey leaves some people out.** NSDUH covers people living in households. It does not cover people in jails, prisons or other institutions.
- **Survey numbers have a margin of error.** The SUD and worker numbers are estimates. Small differences between states may not be real.
- **The worker count is broad.** It covers all work settings and includes mental health work. It leaves out the self-employed. BLS changed how it makes its estimates in 2021.
- **Establishment counts are minimums.** Facilities that did not respond are not counted, and response rates were lower from 2021 on.
- **Death counts follow CDC's records.** CDC notes some state coding problems, such as more than 900 North Carolina overdose deaths in 2023 that were recoded after the data closed. The map's notes list them.

## Reproduce it yourself

::: spacer 5px

The code, the data and the full method are at [github.com/Data4ThePeople/SUD_V3](https://github.com/Data4ThePeople/SUD_V3). Every step is in the scripts, in order. If you get a different number from us, tell us, and we will look.

::: divider

## Common questions

::: spacer 5px

### How many people in the U.S. have a substance use disorder?

SAMHSA estimates 48.4 million people 12 and older in 2023-2024, or 16.9%. This uses the newer DSM-5 definition, so it cannot be compared with estimates from 2020 or earlier.

### Which state has the highest rate of substance use disorder?

In 2023-2024, the District of Columbia had the highest rate, 23.8% of people 12 and older, followed by Maine and Colorado (22.4%). Utah had the lowest, 12.6%.

### Why did the number of people with a substance use disorder more than double in 2022?

SAMHSA changed its survey and its definition of a disorder starting in 2021. SAMHSA says the estimates from 2021 on are not comparable with earlier years, so the jump should not be read as a change in how many people had a disorder.

### Which state has the fewest treatment workers for the people who need them?

In 2024, Nevada had the most people with SUD per treatment worker, 177, followed by Alabama (175) and Georgia (162). Massachusetts had the fewest, 49.

### What counts as a treatment worker?

Substance use and mental health counselors, plus mental health and substance use social workers, as counted by the Bureau of Labor Statistics. It includes every work setting. It does not include doctors, nurses, peer support workers or the self-employed.

### Which state has the fewest treatment facilities per person?

In 2024, Texas had the fewest outpatient substance use treatment establishments for its population, 1.6 per 100,000 residents, followed by South Carolina (1.7) and Alabama (2.2). Kentucky had the most, 11.4.

### Which state has the highest overdose and alcohol death rate?

In 2024, Alaska and New Mexico, at 73.8 deaths per 100,000 residents.

### Why is my state gray?

The source did not publish a number for that state and year. We leave it blank and do not estimate one.

### Why are some years missing from the SUD map?

SAMHSA published no state estimates for the survey windows ending in 2002, 2015, 2020 and 2021.

### Where can I find treatment?

Call or text 988 for the Suicide & Crisis Lifeline, or search [FindTreatment.gov](https://findtreatment.gov/), SAMHSA's treatment locator, by ZIP code.

### Where does the data come from?

SAMHSA's National Survey on Drug Use and Health and its treatment facility surveys, the Bureau of Labor Statistics' Occupational Employment and Wage Statistics, and CDC WONDER death records.

### Is the map free to use?

Yes. It is free to use and needs no sign-in.
