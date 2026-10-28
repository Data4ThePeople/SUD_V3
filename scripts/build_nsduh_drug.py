"""Build data/clean/nsduh_drug.csv: NSDUH state small area estimates of past-year drug use
disorder, ages 12+, one row per window x state. Used for the page's "Drug only" view.

SAMHSA's measure changes with the survey:
  2000-2001 to 2013-2014   ABODILL   illicit drug dependence or abuse (DSM-IV)
  2015-2016 to 2018-2019   UDPYILL   illicit drug use disorder (DSM-IV)
  2021-2022 to 2023-2024   UD5ILANY  drug use disorder (DSM-5)
No window ending in 2002, 2015, 2020 or 2021, as for any SUD.

Source: SAMHSA's state SAE SAS datasets (unchanged under data/raw/nsduh/), the same files
build_nsduh_sud.py uses for its early windows. For 2010-2011 the "(published)" estimates are
used, matching the any-SUD series. Every window that also has a published Excel table is
checked against that table: percent to 2 decimals, counts exactly. Nothing is filled.

Run with: .venv/bin/python -I scripts/build_nsduh_drug.py
"""
import csv
import pathlib
import re

import openpyxl
import pandas as pd

from build_nsduh_sud import KEEP, RAW, TABLES, count_str, norm_state, pct_from_prop

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "clean" / "nsduh_drug.csv"
SOURCES = [("sae_dataset_1999-2019/NSDUH_99_19_state_saes_final.sas7bdat", {"ABODILL": ("IV", "Illicit Drug Dependence or Abuse in the Past Year"),
                                                                          "UDPYILL": ("IV", "Illicit Drug Use Disorder in the Past Year")}),
           ("sae_dataset_2021-2024/state_saes_final_2124.sas7bdat", {"UD5ILANY": ("5", "Drug Use Disorder in the Past Year")})]
# a drug table title, and not any-SUD, pain reliever, opioid, or dependence-only tables
DRUG_TITLE = re.compile(r"^Table \d+\.?\s*(Illicit Drug Dependence or Abuse|Illicit Drug Use Disorder|Drug Use Disorder) in the Past Year")


def published(path):
    """{state: (est, lo, hi)} from the drug table's 12+ columns in a published workbook."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for sn in wb.sheetnames:
        rows = list(wb[sn].iter_rows(values_only=True))
        if rows and rows[0] and rows[0][0] and DRUG_TITLE.search(str(rows[0][0]).strip()):
            h = next(i for i, r in enumerate(rows) if r and r[0] == "Order")
            return str(rows[0][0]).strip(), {norm_state(r[1]): r[2:5] for r in rows[h + 1:] if r[1] is not None}
    return None, None  # some workbooks hold only the any-SUD table


def main():
    rows = []
    for f, outcomes in SOURCES:
        d = pd.read_sas(RAW / f, encoding="latin1")
        d.columns = [c.lower() for c in d.columns]
        d = d[d.outcome.isin(outcomes) & (d.agegrp == 0) & d.pyearnm.str.contains("-")
              & ~d.pyearnm.str.contains("updated")]
        for _, r in d.iterrows():
            s = norm_state(r.stname)
            if s not in KEEP:
                continue
            window = r.pyearnm.replace(" (published)", "")
            dsm, name = outcomes[r.outcome]
            rows.append(dict(window=window, end_year=int(window[-4:]), state=s,
                             pct=pct_from_prop(r.bsae), pct_lo=pct_from_prop(r.low_sae), pct_hi=pct_from_prop(r.up_sae),
                             count_thousands=count_str(r.est_total), count_lo=count_str(r.low_total),
                             count_hi=count_str(r.up_total), measure_name=name, dsm=dsm,
                             source_file=f"{f} [OUTCOME={r.outcome}, AGEGRP=0]"))
    out = pd.DataFrame(rows)
    assert (out.groupby("window").size() == 52).all() and not out.duplicated(["window", "state"]).any()

    # check against SAMHSA's published workbooks
    bad, checked = [], []
    for window, ((pk, pp), (ck, cp)) in TABLES.items():
        if pk != "xlsx" or ck != "xlsx":
            continue
        _, pct = published(RAW / pp)
        _, cnt = published(RAW / cp)
        w = out[out.window == window].set_index("state")
        for s in KEEP:
            for col, v in zip(("pct", "pct_lo", "pct_hi"), pct[s] if pct else ()):
                if round(float(w.at[s, col]), 2) != round(v * 100, 2) and abs(float(w.at[s, col]) - v * 100) > 0.0051:
                    bad.append((window, s, col, w.at[s, col], v * 100))
            for col, v in zip(("count_thousands", "count_lo", "count_hi"), cnt[s] if cnt else ()):
                if float(w.at[s, col]) != float(v):
                    bad.append((window, s, col, w.at[s, col], v))
        checked.append(window + ("" if pct else " (counts only)") + ("" if cnt else " (percents only)"))
    print("checked against published tables:", checked)
    print("mismatches:", len(bad))
    for b in bad[:20]:
        print("  ", b)
    if bad:
        raise SystemExit(1)
    out.sort_values(["end_year", "state"]).to_csv(OUT, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"wrote {OUT} ({len(out)} rows, {out.window.nunique()} windows)")


if __name__ == "__main__":
    main()
